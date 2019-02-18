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

# get_device_id
def get_device_id():
    LOG.info("User-Management: Data: get_device_id: Getting 'my' device ID ...")

    device = cimi.get_device_info()
    LOG.debug("User-Management: Data: get_device_id: device = " + str(device))

    if not device is None and device != -1:
        LOG.info("User-Management: Data: get_device_id: Returning 'my' device ID = " + str(device['id']))
        return device['id']
    else:
        return "-1"


###############################################################################
# SHARING MODEL
#
# {
#       ----------------"user_id": "user/1230958abdef",
# 	    "max_apps": integer,
# 	    "gps_allowed": boolean,
# 	    "max_cpu_usage": integer,
# 	    "max_memory_usage": integer,
# 	    "max_storage_usage": integer,
# 	    "max_bandwidth_usage": integer,
# 	    "battery_limit": integer
# }

# Get user profile
def get_sharing_model_user_device(user_id, device_id):
    LOG.debug("User-Management: Data: get_sharing_model_user_device: " + user_id + ", " + device_id)
    return cimi.get_user_sharing_model(user_id, device_id)


# Get shared resources
def get_sharing_model(user_id, device_id):
    LOG.info("User-Management: Data: get_sharing_model_values: " + str(user_id))
    return cimi.get_user_sharing_model(user_id, device_id)


# Initializes shared resources values
def init_sharing_model(data):
    LOG.info("User-Management: Data: init_sharing_model: " + str(data))
    return cimi.add_resource(config.dic['CIMI_SHARING_MODELS'], data)


# Updates shared resources values
def update_sharing_model(data):
    LOG.info("User-Management: Data: update_sharing_model_values: " + str(data))
    resp = cimi.get_user_sharing_model(data['user_id'], data['device_id'])
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# Deletes  shared resources values
def delete_sharing_model(user_id, device_id):
    LOG.info("User-Management: Data: delete_sharing_model_values: " + user_id + ", " + device_id)
    resp = cimi.get_user_sharing_model(user_id, device_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None


###############################################################################
# PROFILING
#
#  {
#       "user_id": "user/0000000000u",
#       "device_id": "device/11111111d",
#  	    "max_apps": 1,
#  	    "service_consumer": boolean,
#  	    "resource_contributor": boolean
#  }


# Get user profile
def get_profile_user_device(user_id, device_id):
    LOG.debug("User-Management: Data: get_profile_user_device: " + user_id + ", " + device_id)
    return cimi.get_user_profile(user_id, device_id)


# Updates users profile
def update_profile_user_device(user_id, device_id, data):
    LOG.debug("User-Management: Data: update_profile_user_device: " + user_id + ", " + device_id + ", " + str(data))

    resp = cimi.get_user_profile(user_id, device_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# Get user profile
def get_profiling(user_id):
    LOG.debug("User-Management: Data: get_profiling: " + user_id)

    # get 'my' device_id
    device_id = get_device_id()
    LOG.debug("User-Management: Data: get_profiling: Get Profile from user [" + user_id + "] and device [" + device_id + "]")

    return cimi.get_user_profile(user_id, device_id)


# Get allowed services
def get_services(user_id):
    LOG.debug("User-Management: Data: get_services: " + user_id)

    # TODO CIMI
    # ...

    return ['service_id_1', 'service_id_2', 'service_id_3']


# Initializes users profile
def register_user(data):
    LOG.debug("User-Management: Data: register_user: " + str(data))
    # get 'my' device_id
    device_id = get_device_id()
    LOG.debug("User-Management: Data: register_user: Create new Profile for user [" + data['user_id'] + "] and device [" + device_id + "]")

    data['device_id'] = device_id
    LOG.debug("User-Management: Data: register_user: Storing data in cimi [data=" + str(data) + "] ...")

    return cimi.add_resource(config.dic['CIMI_PROFILES'], data)


# Updates users profile
def update_profile(user_id, device_id, data):
    LOG.debug("User-Management: Data: update_profile: Update Profile for user [" + data['user_id'] + "] and device [" + device_id + "]")
    resp = cimi.get_user_profile(user_id, device_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# Deletes users profile
def delete_profile(user_id, device_id):
    LOG.debug("User-Management: Data: delete_profile: Delete Profile from user [" + user_id + "] and device [" + device_id + "]")

    resp = cimi.get_user_profile(user_id, device_id)
    if resp and resp == -1:
        return None
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None


###############################################################################
# DEVICE DYNAMIC

# Get battery level
def get_power(user_id, device_id):
    LOG.info("User-Management: Data: get_power: " + user_id + ", " + device_id)
    return cimi.get_power(user_id, device_id)


# Get parent
def get_parent(user_id, device_id):
    LOG.info("User-Management: Data: get_parent: " + user_id + ", " + device_id)
    return cimi.get_parent(user_id, device_id)

###############################################################################
# NUMBER OF APPLICATIONS RUNNING IN DEVICE

# Get applications running
def get_num_apps_running(user_id, device_id):
    LOG.info("User-Management: Data: get_num_apps_running: " + user_id + ", " + device_id)
    return cimi.get_num_apps_running(user_id, device_id)