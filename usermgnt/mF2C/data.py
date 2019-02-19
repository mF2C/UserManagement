"""
Data Management: dataclay, cimi...
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

import usermgnt.mF2C.cimi as cimi
from common.logs import LOG
import config


###############################################################################
# COMMON

# TODO get this information from new RESOURCE: AGENT
# get_current_device_id
def get_current_device_id():
    LOG.info("User-Management: Data: get_device_id: Getting 'my' device ID ...")

    device = cimi.get_current_device_info()
    LOG.debug("User-Management: Data: get_device_id: device = " + str(device))

    if not device is None and device != -1:
        LOG.info("User-Management: Data: get_device_id: Returning 'my' device ID = " + str(device['id']))
        return device['id']
    else:
        return -1


# exist_user: check if 'user id' exists
def exist_user(user_id):
    return cimi.exist_user(user_id)


# exist_device: check if 'device id' exists
def exist_device(device_id):
    return cimi.exist_device(device_id)


###############################################################################
# SHARING MODEL
#
# {
#       "user_id": "user/0000000000u",
#       "device_id": "device/11111111d",
# 	    "gps_allowed": boolean,
# 	    "max_cpu_usage": integer,
# 	    "max_memory_usage": integer,
# 	    "max_storage_usage": integer,
# 	    "max_bandwidth_usage": integer,
# 	    "battery_limit": integer
# }

# get_user_profile_by_id
def get_sharing_model_by_id(sharing_model_id):
    sharing_model_id = sharing_model_id.replace('sharing-model/', '')
    LOG.debug("User-Management: Data: get_sharing_model_by_id: " + sharing_model_id)

    sharing_model = cimi.get_resource_by_id("sharing-model/" + sharing_model_id)
    if not sharing_model['status'] is None and sharing_model['status'] == 404:
        return -1
    return sharing_model  # cimi.get_resource_by_id("sharing-model/" + sharing_model_id)


# Get user profile
def get_sharing_model_user_device(user_id, device_id):
    LOG.debug("User-Management: Data: get_sharing_model_user_device: " + user_id + ", " + device_id)
    return cimi.get_sharing_model(user_id, device_id)


# Get shared resources
def get_sharing_model(user_id, device_id):
    LOG.info("User-Management: Data: get_sharing_model_values: " + str(user_id))
    return cimi.get_sharing_model(user_id, device_id)


# Initializes shared resources values
def init_sharing_model(data):
    LOG.info("User-Management: Data: init_sharing_model: " + str(data))
    return cimi.add_resource(config.dic['CIMI_SHARING_MODELS'], data)


# Updates shared resources values
def update_sharing_model_by_id(sharing_model_id, data):
    sharing_model_id = sharing_model_id.replace('sharing-model/', '')
    LOG.info("User-Management: Data: update_sharing_model_by_id: " + sharing_model_id + ", " + str(data))
    resp = cimi.get_resource_by_id("sharing-model/" + sharing_model_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# Updates shared resources values
def update_sharing_model(data):
    LOG.info("User-Management: Data: update_sharing_model_values: " + str(data))
    resp = cimi.get_sharing_model(data['user_id'], data['device_id'])
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# delete_sharing_model_by_id: Deletes  shared resources values
def delete_sharing_model_by_id(sharing_model_id):
    sharing_model_id = sharing_model_id.replace('sharing-model/', '')
    LOG.info("User-Management: Data: delete_sharing_model_by_id: " + sharing_model_id)
    resp = cimi.get_resource_by_id("sharing-model/" + sharing_model_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None


# Deletes  shared resources values
def delete_sharing_model(user_id, device_id):
    LOG.info("User-Management: Data: delete_sharing_model_values: " + user_id + ", " + device_id)
    resp = cimi.get_sharing_model(user_id, device_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None


###############################################################################
## Current SHARING-MODEL

# TODO get this information from new RESOURCE: AGENT
# Get user profile
def get_current_sharing_model():
    LOG.debug("User-Management: Data: get_current_sharing_model: Getting information about current user and device...")
    # get 'my' device_id
    device_id = get_current_device_id()
    if device_id == -1:
        return None
    else:
        sharing_model = cimi.get_sharing_model_by_device(device_id)
        if sharing_model is None or sharing_model == -1:
            return None
        else:
            user_id = sharing_model['user_id']
            LOG.debug("User-Management: Data: get_current_sharing_model: Get Sharing Model for user [" + user_id + "] and device [" + device_id + "]")
            return cimi.get_sharing_model(user_id, device_id)


###############################################################################
# USER-PROFILE
#
#  {
#       "user_id": "user/0000000000u",
#       "device_id": "device/11111111d",
#  	    "max_apps": 1,
#  	    "service_consumer": boolean,
#  	    "resource_contributor": boolean
#  }

# get_user_profile_by_id
def get_user_profile_by_id(profile_id):
    profile_id = profile_id.replace('user-profile/', '')
    LOG.debug("User-Management: Data: get_user_profile_by_id: " + profile_id)

    profile = cimi.get_resource_by_id("user-profile/" + profile_id)
    if not profile['status'] is None and profile['status'] == 404:
        return -1
    return profile # cimi.get_resource_by_id("user-profile/" + profile_id)


# get_user_profile: Get user profile
def get_user_profile(user_id, device_id):
    LOG.debug("User-Management: Data: get_profile_user_device: " + user_id + ", " + device_id)
    return cimi.get_user_profile(user_id, device_id)


# update_user_profile_by_id: Updates a profile
def update_user_profile_by_id(profile_id, data):
    profile_id = profile_id.replace('user-profile/', '')
    LOG.debug("User-Management: Data: update_user_profile_by_id: " + profile_id + ", " + str(data))
    resp = cimi.get_resource_by_id("user-profile/" + profile_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# update_user_profile: Updates users profile
def update_user_profile(user_id, device_id, data):
    LOG.debug("User-Management: Data: update_user_profile: Update Profile for user [" + data['user_id'] + "] and device [" + device_id + "]")
    resp = cimi.get_user_profile(user_id, device_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# Deletes users profile
def delete_user_profile_by_id(profile_id):
    profile_id = profile_id.replace('user-profile/', '')
    LOG.debug("User-Management: Data: delete_user_profile_by_id: Delete Profile [" + profile_id + "]")
    resp = cimi.get_resource_by_id("user-profile/" + profile_id)
    if resp and resp == -1:
        return None
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None


# Deletes users profile
def delete_user_profile(user_id, device_id):
    LOG.debug("User-Management: Data: delete_user_profile: Delete Profile from user [" + user_id + "] and device [" + device_id + "]")

    resp = cimi.get_user_profile(user_id, device_id)
    if resp and resp == -1:
        return None
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None


# Initializes users profile
def register_user(data):
    LOG.debug("User-Management: Data: register_user: " + str(data))
    LOG.debug("User-Management: Data: register_user: Creating new Profile for user [" + data['user_id'] + "] and device [" + data['device_id'] + "] ...")
    return cimi.add_resource(config.dic['CIMI_PROFILES'], data)


###############################################################################
## Current USER-PROFILE

# TODO get this information from new RESOURCE: AGENT
# Get user profile
def get_current_user_profile():
    LOG.debug("User-Management: Data: get_current_user_profile: Getting information about current user and device...")
    # get 'my' device_id
    device_id = get_current_device_id()
    if device_id == -1:
        return None
    else:
        user_profile = cimi.get_user_profile_by_device(device_id)
        if user_profile is None or user_profile == -1:
            return None
        else:
            user_id = user_profile['user_id']
            LOG.debug("User-Management: Data: get_current_user_profile: Get Profile from user [" + user_id + "] and device [" + device_id + "]")
            return cimi.get_user_profile(user_id, device_id)


###############################################################################
## Services Running on current device

# TODO
# get_total_services_running: Get services running
def get_total_services_running(device_id):
    LOG.debug("User-Management: Data: get_total_services_running: Getting total of services running in device [" + device_id + "] ...")

    # TODO CIMI
    # ...

    return 1


###############################################################################
# DEVICE DYNAMIC

# TODO
# Get battery level
def get_power(device_id):
    LOG.info("User-Management: Data: get_power: " + device_id)
    return cimi.get_power(device_id)


# TODO
# Get parent
def get_parent(user_id, device_id):
    LOG.info("User-Management: Data: get_parent: " + user_id + ", " + device_id)
    return cimi.get_parent(user_id, device_id)
