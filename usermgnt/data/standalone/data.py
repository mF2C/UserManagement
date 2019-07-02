"""
Data Management: dataclay, cimi...
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

from usermgnt.data.app import volume as vol
from usermgnt.data.standalone import db as db
from usermgnt.common.logs import LOG
import config


###############################################################################
# COMMON

# FUNCTION: get_current_device_id
def get_current_device_id():
    LOG.info("[usermgnt.data.standalone.data] [get_current_device_id] Getting 'my' device ID ...")
    # get from local volume
    device_id = vol.read_device_id()
    if device_id is not None and not device_id == "" and len(device_id) > 0:
        LOG.debug("[usermgnt.data.standalone.data] [get_current_device_id] (LOCAL VOLUME) device_id = " + device_id)
        return device_id
    # get from config.dic['HOST_IP']
    else:
        return config.dic['HOST_IP']


###############################################################################
# USER

# FUNCTION: get_user_info: gets user info
# def get_user_info(user_id):


# FUNCTION: delete_user: deletes user
# def delete_user(user_id):


###############################################################################
# SHARING MODEL

# FUNCTION: get_sharing_model_by_id
def get_sharing_model_by_id(sharing_model_id):
    LOG.debug("[usermgnt.data.standalone.data] [get_sharing_model_by_id] " + sharing_model_id)
    return db.get_from_SHARING_MODEL_by_id(sharing_model_id)


# Get shared resources
def get_sharing_model(device_id):
    LOG.info("[usermgnt.data.standalone.data] [get_sharing_model] " + device_id)
    return db.get_from_SHARING_MODEL_by_device_id(device_id)


# Initializes shared resources values
def init_sharing_model(data):
    LOG.info("[usermgnt.data.standalone.data] [init_sharing_model] " + str(data))
    return db.save_to_SHARING_MODEL(config.dic['DEVICE_USER'], config.dic['HOST_IP'], data['max_apps'], data['battery_limit'])


# Updates shared resources values
def update_sharing_model_by_id(sharing_model_id, data):
    LOG.info("[usermgnt.data.standalone.data] [update_sharing_model_by_id] " + sharing_model_id + ", " + str(data))
    return db.update_SHARING_MODEL(sharing_model_id, data['max_apps'], data['battery_limit'])


# delete_sharing_model_by_id: Deletes  shared resources values
def delete_sharing_model_by_id(sharing_model_id):
    LOG.info("[usermgnt.data.standalone.data] [delete_sharing_model_by_id] " + sharing_model_id)
    return db.del_from_SHARING_MODEL_by_id(sharing_model_id)


# FUNCTION: get_current_sharing_model: Get current SHARING-MODEL
def get_current_sharing_model():
    LOG.debug("[usermgnt.data.standalone.data] [get_current_sharing_model] Getting information about current user and device ...")
    return db.get_current_SHARING_MODEL()


###############################################################################
# USER-PROFILE

# get_user_profile_by_id
def get_user_profile_by_id(profile_id):
    LOG.debug("[usermgnt.data.standalone.data] [get_user_profile_by_id] " + profile_id)
    return db.get_from_USER_PROFILE_by_id(profile_id)


# get_user_profile: Get user profile
def get_user_profile(device_id):
    LOG.debug("[usermgnt.data.standalone.data] [get_user_profile] device_id=" + device_id)
    return db.get_from_USER_PROFILE_by_device_id(device_id)


# update_user_profile_by_id: Updates a profile
def update_user_profile_by_id(profile_id, data):
    LOG.debug("[usermgnt.data.standalone.data] [update_user_profile_by_id] " + profile_id + ", " + str(data))
    return db.update_USER_PROFILE(profile_id, data['service_consumer'], data['resource_contributor'])


# Deletes users profile
def delete_user_profile_by_id(profile_id):
    LOG.debug("[usermgnt.data.standalone.data] [delete_user_profile_by_id] Delete Profile [" + profile_id + "]")
    return db.del_from_USER_PROFILE_by_id(id)


# Initializes users profile
def register_user(data):
    LOG.debug("[usermgnt.data.standalone.data] [register_user] Creating new Profile for user [data=" + str(data) + "] ...")
    return db.save_to_USER_PROFILE(config.dic['DEVICE_USER'], config.dic['HOST_IP'], data['service_consumer'], data['resource_contributor'])


# setAPPS_RUNNING
def setAPPS_RUNNING(apps=0):
    config.APPS_RUNNING = config.APPS_RUNNING + apps
    if config.APPS_RUNNING < 0:
        config.APPS_RUNNING = 0


# FUNCTION: get_current_user_profile: Get Current USER-PROFILE
def get_current_user_profile():
    LOG.debug("[usermgnt.data.standalone.data] [get_current_user_profile] Getting information about current user and device ...")
    return db.get_current_USER_PROFILE()


###############################################################################
## AGENT INFO
## power, apps running ...

# FUNCTION: get_total_services_running: Get services running
def get_total_services_running():
    LOG.debug("[usermgnt.data.standalone.data] [get_total_services_running] Total of services running in device = " + str(config.APPS_RUNNING))
    return config.APPS_RUNNING


# FUNCTION: get_power: Get battery level from DEVICE_DYNAMIC
def get_power():
    LOG.warning("[usermgnt.data.standalone.data] [get_power] not implemented. Getting power status from device. Returning 100 ...")
    return 100


###############################################################################
## LOCAL VOLUME
## Used to store / read 'user_id' and 'device_id'

# FUNCTION: save_device_id
def save_device_id(device_id):
    vol.save_device_id(device_id)


# FUNCTION: read_device_id
def read_device_id():
    vol.read_device_id()
