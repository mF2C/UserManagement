"""
Initial configuration
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 02 may 2018

@author: Roi Sucasas - ATOS
"""


import config
import common.common as common
import threading
import time
from common.logs import LOG
import usermgnt.modules.um_profiling as um_profiling
import usermgnt.modules.um_sharing_model as um_sharing_model
import usermgnt.mF2C.data as datamgmt


# FUNCTION: init: initializes all global properties from config file and environment variables
def init():
    try:
        # get CIMI from environment values:
        LOG.info('USRMNGT: init_config: init: Reading values from ENVIRONMENT...')

        common.set_value_env('HOST_IP')
        common.set_value_env('CIMI_COOKIES_PATH')
        common.set_value_env('CIMI_USER')
        common.set_value_env('CIMI_PASSWORD')
        common.set_value_env('UM_WORKING_DIR_VOLUME') # UM_WORKING_DIR_VOLUME from environment values:
        common.set_value_env('CIMI_URL')

        LOG.info('USRMNGT: init_config: init: Reading User-Profile and Sharing-Model values from ENVIRONMENT...')
        common.set_value_env('SERVICE_CONSUMER')
        common.set_value_env('RESOURCE_CONTRIBUTOR')
        common.set_value_env('MAX_APPS')
        common.set_value_env('BATTERY_LIMIT')
        common.set_value_env('GPS_ALLOWED')
        common.set_value_env('MAX_CPU_USAGE')
        common.set_value_env('MAX_MEM_USAGE')
        common.set_value_env('MAX_STO_USAGE')
        common.set_value_env('MAX_BANDWITH_USAGE')

        LOG.info('USRMNGT: init_config: init: Checking configuration...')

        # CIMI URL
        if "/api" not in config.dic['CIMI_URL'] and not config.dic['CIMI_URL'].endswith("/api"):
            LOG.debug("Adding '/api' to CIMI_URL ...")
            if config.dic['CIMI_URL'].endswith("/"):
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "api"
            else:
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "/api"
            LOG.debug('USRMNGT: [CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        else:
            LOG.debug("USRMNGT: CIMI_URL ... " + config.dic['CIMI_URL'])

        LOG.info('USRMNGT: [CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        LOG.info('USRMNGT: [CIMI_COOKIES_PATH=' + config.dic['CIMI_COOKIES_PATH'] + ']')
        LOG.info('USRMNGT: [CIMI_USER=' + config.dic['CIMI_USER'] + ']')
        LOG.info('USRMNGT: [CIMI_PASSWORD=' + config.dic['CIMI_PASSWORD'] + ']')
        LOG.info('USRMNGT: [UM_WORKING_DIR_VOLUME=' + config.dic['UM_WORKING_DIR_VOLUME'] + ']')
        LOG.info('USRMNGT: [SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
        LOG.info('USRMNGT: [API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
        LOG.info('USRMNGT: [CERT_CRT=' + config.dic['CERT_CRT'] + ']')
        LOG.info('USRMNGT: [CERT_KEY=' + config.dic['CERT_KEY'] + ']')
        LOG.info('USRMNGT: [HOST_IP=' + config.dic['HOST_IP'] + ']')

        LOG.info('USRMNGT: init_config: init: User-Profile and Sharing-Model configuration...')
        LOG.info('USRMNGT: [SERVICE_CONSUMER=' + str(config.dic['SERVICE_CONSUMER']) + ']')
        LOG.info('USRMNGT: [RESOURCE_CONTRIBUTOR=' + str(config.dic['RESOURCE_CONTRIBUTOR']) + ']')
        LOG.info('USRMNGT: [MAX_APPS=' + str(config.dic['MAX_APPS']) + ']')
        LOG.info('USRMNGT: [BATTERY_LIMIT=' + str(config.dic['BATTERY_LIMIT']) + ']')
        LOG.info('USRMNGT: [GPS_ALLOWED=' + str(config.dic['GPS_ALLOWED']) + ']')
        LOG.info('USRMNGT: [MAX_CPU_USAGE=' + str(config.dic['MAX_CPU_USAGE']) + ']')
        LOG.info('USRMNGT: [MAX_MEM_USAGE=' + str(config.dic['MAX_MEM_USAGE']) + ']')
        LOG.info('USRMNGT: [MAX_STO_USAGE=' + str(config.dic['MAX_STO_USAGE']) + ']')
        LOG.info('USRMNGT: [MAX_BANDWITH_USAGE=' + str(config.dic['MAX_BANDWITH_USAGE']) + ']')
    except:
        LOG.exception('USRMNGT: init_config: init: Exception: Error while initializing application')


# THREAD: create_user_profile: (thread) create a default user-profile based on environment variables or default values
def __thr_create_user_profile(data):
    try:
        LOG.info("USRMNGT: init_config: (thread) thr_create_user_profile: Creating USER-PROFILE [" + str(data) + "] in current device ...")
        created = False
        while not created:
            LOG.debug('USRMNGT: init_config: << thr_create_user_profile: daemon >> executing ...')

            # get device_id
            device_id = datamgmt.get_current_device_id()
            if device_id == -1:
                time.sleep(30)
            else:
                # create user-profile
                data['device_id'] = device_id
                up = um_profiling.create_user_profile(data)
                if up is not None:
                    LOG.info('USRMNGT: init_config: << thr_create_user_profile: daemon >> user-profile created! ...')
                    created = True
                else:
                    LOG.error('USRMNGT: init_config: << thr_create_user_profile: daemon >> user-profile not created! ')
    except:
        LOG.exception('USRMNGT: init_config: (thread) thr_create_user_profile: Exception: Error while initializing application')


# FUNCTION: create_user_profile: create a default user-profile based on environment variables or default values
def create_user_profile():
    try:
        LOG.info('USRMNGT: init_config: create_user_profile: Creating USER-PROFILE in current device ...')
        data = {
            "service_consumer": config.dic['SERVICE_CONSUMER'],
            "resource_contributor": config.dic['RESOURCE_CONTRIBUTOR'],
            "device_id": ""
        }
        d = threading.Thread(target=__thr_create_user_profile, args=(data,))
        d.setDaemon(True)
        d.start()
    except:
        LOG.exception('USRMNGT: init_config: create_user_profile: Exception: Error while initializing application')


# THREAD: create_sharing_model: (thread) create a default usharing-model based on environment variables or default values
def __thr_create_sharing_model(data):
    try:
        LOG.info("USRMNGT: init_config: (thread) thr_create_sharing_model: Creating SHARING-MODEL [" + str(data) + "] in current device ...")
        created = False
        while not created:
            LOG.debug('USRMNGT: init_config: << thr_create_sharing_model: daemon >> executing ...')

            # get device_id
            device_id = datamgmt.get_current_device_id()
            if device_id == -1:
                time.sleep(30)
            else:
                # create sharing-model
                data['device_id'] = device_id
                up = um_sharing_model.init_sharing_model(data)
                if up is not None:
                    LOG.info('USRMNGT: init_config: << thr_create_sharing_model: daemon >> sharing-model created! ...')
                    created = True
                else:
                    LOG.error('USRMNGT: init_config: << thr_create_sharing_model: daemon >> sharing-model not created! ')

    except:
        LOG.exception('USRMNGT: init_config: (thread) thr_create_sharing_model: Exception: Error while initializing application')


# THREAD: create_sharing_model: (thread) create a default usharing-model based on environment variables or default values
def create_sharing_model():
    try:
        LOG.info('USRMNGT: init_config: create_sharing_model: Creating SHARING-MODEL in current device ...')
        data = {
            "gps_allowed": config.dic['GPS_ALLOWED'],
            "max_cpu_usage": config.dic['MAX_CPU_USAGE'],
            "max_memory_usage": config.dic['MAX_MEM_USAGE'],
            "max_storage_usage": config.dic['MAX_STO_USAGE'],
            "max_bandwidth_usage": config.dic['MAX_BANDWITH_USAGE'],
            "battery_limit": config.dic['BATTERY_LIMIT'],
            "max_apps": config.dic['MAX_APPS'],
            "device_id": ""
        }
        d = threading.Thread(target=__thr_create_sharing_model, args=(data,))
        d.setDaemon(True)
        d.start()
    except:
        LOG.exception('USRMNGT: init_config: create_sharing_model: Exception: Error while initializing application')