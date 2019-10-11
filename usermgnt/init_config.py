"""
Initial configuration
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 02 may 2018

@author: Roi Sucasas - ATOS
"""

import config
import threading, time, os
from usermgnt.common import common as common
from usermgnt.common.logs import LOG
from usermgnt.modules import um_profiling as um_profiling
from usermgnt.modules import um_sharing_model as um_sharing_model
from usermgnt.data import data_adapter as data_adapter
from usermgnt.data.standalone import db as db
from usermgnt.common.common import TRACE


# FUNCTION: init: initializes all global properties from config file and environment variables
def init():
    try:
        # get CIMI from environment values:
        LOG.info('[usermgnt.init_config] [init] Reading values from ENVIRONMENT...')

        # UM_MODE
        common.set_value_env('UM_MODE')

        common.set_value_env('HOST_IP')
        common.set_value_env('DEVICE_USER')
        common.set_value_env('UM_WORKING_DIR_VOLUME') # UM_WORKING_DIR_VOLUME from environment values:
        common.set_value_env('CIMI_URL')

        LOG.info('[usermgnt.init_config] [init] Reading User-Profile and Sharing-Model values from ENVIRONMENT...')
        common.set_value_env_bool('SERVICE_CONSUMER', config.dic['SERVICE_CONSUMER'])
        common.set_value_env_bool('RESOURCE_CONTRIBUTOR', config.dic['RESOURCE_CONTRIBUTOR'])
        common.set_value_env_int('MAX_APPS', config.dic['MAX_APPS'])
        common.set_value_env_int('BATTERY_LIMIT', config.dic['BATTERY_LIMIT'])
        common.set_value_env_bool('GPS_ALLOWED', config.dic['GPS_ALLOWED'])
        common.set_value_env_int('MAX_CPU_USAGE', config.dic['MAX_CPU_USAGE'])
        common.set_value_env_int('MAX_MEM_USAGE', config.dic['MAX_MEM_USAGE'])
        common.set_value_env_int('MAX_STO_USAGE', config.dic['MAX_STO_USAGE'])
        common.set_value_env_int('MAX_BANDWITH_USAGE', config.dic['MAX_BANDWITH_USAGE'])

        LOG.info('[usermgnt.init_config] [init] Checking configuration...')
        LOG.info('[usermgnt.init_config] [init] [UM_MODE=' + config.dic['UM_MODE'] + ']')

        # CIMI URL
        if "/api" not in config.dic['CIMI_URL'] and not config.dic['CIMI_URL'].endswith("/api"):
            LOG.debug("[usermgnt.init_config] [init] Adding '/api' to CIMI_URL ...")
            if config.dic['CIMI_URL'].endswith("/"):
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "api"
            else:
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "/api"
            LOG.debug('[usermgnt.init_config] [init] [CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        else:
            LOG.debug("[usermgnt.init_config] [init] CIMI_URL ... " + config.dic['CIMI_URL'])

        LOG.info('[usermgnt.init_config] [init] [CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        LOG.info('[usermgnt.init_config] [init] [DEVICE_USER=' + config.dic['DEVICE_USER'] + ']')
        LOG.info('[usermgnt.init_config] [init] [UM_WORKING_DIR_VOLUME=' + config.dic['UM_WORKING_DIR_VOLUME'] + ']')
        LOG.info('[usermgnt.init_config] [init] [DB_SHARING_MODEL=' + config.dic['DB_SHARING_MODEL'] + ']')
        LOG.info('[usermgnt.init_config] [init] [DB_USER_PROFILE=' + config.dic['DB_USER_PROFILE'] + ']')
        LOG.info('[usermgnt.init_config] [init] [SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
        LOG.info('[usermgnt.init_config] [init] [API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
        LOG.info('[usermgnt.init_config] [init] [HOST_IP=' + config.dic['HOST_IP'] + ']')

        LOG.info('[usermgnt.init_config] [init] User-Profile and Sharing-Model configuration...')
        LOG.info('[usermgnt.init_config] [init] [SERVICE_CONSUMER=' + str(config.dic['SERVICE_CONSUMER']) + ']')
        LOG.info('[usermgnt.init_config] [init] [RESOURCE_CONTRIBUTOR=' + str(config.dic['RESOURCE_CONTRIBUTOR']) + ']')
        LOG.info('[usermgnt.init_config] [init] [MAX_APPS=' + str(config.dic['MAX_APPS']) + ']')
        LOG.info('[usermgnt.init_config] [init] [BATTERY_LIMIT=' + str(config.dic['BATTERY_LIMIT']) + ']')
        LOG.info('[usermgnt.init_config] [init] [GPS_ALLOWED=' + str(config.dic['GPS_ALLOWED']) + ']')
        LOG.info('[usermgnt.init_config] [init] [MAX_CPU_USAGE=' + str(config.dic['MAX_CPU_USAGE']) + ']')
        LOG.info('[usermgnt.init_config] [init] [MAX_MEM_USAGE=' + str(config.dic['MAX_MEM_USAGE']) + ']')
        LOG.info('[usermgnt.init_config] [init] [MAX_STO_USAGE=' + str(config.dic['MAX_STO_USAGE']) + ']')
        LOG.info('[usermgnt.init_config] [init] [MAX_BANDWITH_USAGE=' + str(config.dic['MAX_BANDWITH_USAGE']) + ']')

        LOG.info('[usermgnt.init_config] [init] Checking volume files ...')
        if os.path.exists(config.dic['UM_WORKING_DIR_VOLUME'] + "device_id.txt"):
            os.remove(config.dic['UM_WORKING_DIR_VOLUME'] + "device_id.txt")
            LOG.info("[usermgnt.init_config] [init] File deleted: " + config.dic['UM_WORKING_DIR_VOLUME'] + "device_id.txt")
        else:
            LOG.info("[usermgnt.init_config] [init] The file does not exist: " + config.dic['UM_WORKING_DIR_VOLUME'] + "device_id.txt. Creating new path ...")
            os.makedirs(config.dic['UM_WORKING_DIR_VOLUME'], exist_ok = True)

        if os.path.exists(config.dic['UM_WORKING_DIR_VOLUME'] + "user_id.txt"):
            os.remove(config.dic['UM_WORKING_DIR_VOLUME'] + "user_id.txt")
            LOG.info("[usermgnt.init_config] [init] File deleted: " + config.dic['UM_WORKING_DIR_VOLUME'] + "user_id.txt")
        else:
            LOG.info("[usermgnt.init_config] [init] The file does not exist: " + config.dic['UM_WORKING_DIR_VOLUME'] + "user_id.txt. Creating new path ...")
            os.makedirs(config.dic['UM_WORKING_DIR_VOLUME'], exist_ok = True)

        data_adapter.init(config.dic['UM_MODE'])
    except:
        LOG.exception('[usermgnt.init_config] [init] Exception: Error while initializing application')


# THREAD: create_user_profile: (thread) create a default user-profile based on environment variables or default values
def __thr_create_user_profile(data):
    time.sleep(70)
    try:
        LOG.info("[usermgnt.init_config] [__thr_create_user_profile] << User Profile Creation Thread >> Creating USER-PROFILE [" + str(data) + "] in current device ...")
        created = False
        while not created:
            LOG.log(TRACE, '[usermgnt.init_config] [__thr_create_user_profile] << User Profile Creation Thread >> executing ...')

            # get device_id
            device_id = data_adapter.get_current_device_id()
            if device_id == -1:
                LOG.log(TRACE, '[usermgnt.init_config] [__thr_create_user_profile] << User Profile Creation Thread >> trying again in 45s ...')
                time.sleep(45)
            else:
                # create user-profile
                data['device_id'] = device_id
                up = um_profiling.create_user_profile(data)
                if up is not None:
                    LOG.info('[usermgnt.init_config] [__thr_create_user_profile] << User Profile Creation Thread >> user-profile created! ...')
                    created = True
                else:
                    LOG.error('[usermgnt.init_config] [__thr_create_user_profile] << User Profile Creation Thread >> user-profile not created! Trying again in 60s ...')
                    time.sleep(30)
        LOG.info('[usermgnt.init_config] [__thr_create_user_profile] << User Profile Creation Thread >> thread finishes')
    except:
        LOG.exception('[usermgnt.init_config] [__thr_create_user_profile] << User Profile Creation Thread >> Exception: Error while initializing application')


# FUNCTION: create_user_profile: create a default user-profile based on environment variables or default values
def create_user_profile():
    if config.dic['UM_MODE'] == "MF2C":
        try:
            LOG.log(TRACE, '[usermgnt.init_config] [create_user_profile] Creating USER-PROFILE [MF2C] in current device ...')
            data = {
                "service_consumer": config.dic['SERVICE_CONSUMER'],
                "resource_contributor": config.dic['RESOURCE_CONTRIBUTOR'],
                "device_id": ""
            }
            d = threading.Thread(target=__thr_create_user_profile, args=(data,))
            d.setDaemon(True)
            d.start()
        except:
            LOG.exception('[usermgnt.init_config] [create_user_profile] Exception: Error while initializing application')
    else:
        LOG.info('[usermgnt.init_config] [create_user_profile] Creating USER-PROFILE [STANDALONE] in current device ...')
        db.save_to_SHARING_MODEL(config.dic['DEVICE_USER'], "localhost", 5, 50)


# THREAD: create_sharing_model: (thread) create a default usharing-model based on environment variables or default values
def __thr_create_sharing_model(data):
    time.sleep(65)
    try:
        LOG.info("[usermgnt.init_config] [__thr_create_sharing_model] << Sharing Model Creation Thread >> Creating SHARING-MODEL [" + str(data) + "] in current device ...")
        created = False
        while not created:
            LOG.log(TRACE, '[usermgnt.init_config] [__thr_create_sharing_model] << Sharing Model Creation Thread >> executing ...')

            # get device_id
            device_id = data_adapter.get_current_device_id()
            if device_id == -1:
                LOG.log(TRACE, '[usermgnt.init_config] [__thr_create_sharing_model] << Sharing Model Creation Thread >> trying again in 45s ...')
                time.sleep(45)
            else:
                # create sharing-model
                data['device_id'] = device_id
                up = um_sharing_model.init_sharing_model(data)
                if up is not None:
                    LOG.info('[usermgnt.init_config] [__thr_create_sharing_model] << Sharing Model Creation Thread >> sharing-model created! ...')
                    created = True
                else:
                    LOG.error('[usermgnt.init_config] [__thr_create_sharing_model] << Sharing Model Creation Thread >> sharing-model not created! Trying again in 60s ...')
                    time.sleep(30)
        LOG.info('[usermgnt.init_config] [__thr_create_sharing_model] << Sharing Model Creation Thread >> thread finishes')
    except:
        LOG.exception('[usermgnt.init_config] [__thr_create_sharing_model] << Sharing Model Creation Thread >> Exception: Error while initializing application')


# THREAD: create_sharing_model: (thread) create a default usharing-model based on environment variables or default values
def create_sharing_model():
    if config.dic['UM_MODE'] == "MF2C":
        try:
            LOG.log(TRACE, '[usermgnt.init_config] [create_sharing_model] Creating SHARING-MODEL in current device ...')
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
            LOG.exception('[usermgnt.init_config] [create_sharing_model] Exception: Error while initializing application')
    else:
        LOG.info('[usermgnt.init_config] [create_sharing_model] Creating USER-PROFILE [STANDALONE] in current device ...')
        db.save_to_USER_PROFILE(config.dic['DEVICE_USER'], "localhost", True, True)