"""
Data Management: dataclay, cimi...
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

import usermgnt.mF2C.cimi as cimi
import usermgnt.mF2C.volume as vol
from common.logs import LOG
import config


###############################################################################
# COMMON

# FUNCTION: get_current_device_id
def get_current_device_id():
    LOG.info("USRMNGT: Data: get_current_device_id: Getting 'my' device ID from 'agent' resource ...")
    # get from local volume
    device_id = vol.read_device_id()
    if device_id is not None:
        LOG.debug("USRMNGT: Data: get_current_device_id: (LOCAL VOLUME) device_id = " + device_id)
        return device_id
    # get from AGENT resource
    else:
        agent = cimi.get_agent_info()
        LOG.debug("USRMNGT: Data: get_current_device_id: agent=" + str(agent))
        if not agent is None and agent != -1:
            LOG.info("USRMNGT: Data: get_current_device_id: Returning 'my' device ID = " + agent['device_id'])
            return agent['device_id']
        else:
            return -1


# FUNCTION: get_current_device_ip
def get_current_device_ip():
    LOG.info("USRMNGT: Data: get_current_device_ip: Getting 'my' device IP address from 'agent' resource ...")
    # get from AGENT resource
    agent = cimi.get_agent_info()
    LOG.debug("USRMNGT: Data: get_current_device_ip: agent = " + str(agent))
    if not agent is None and agent != -1:
        LOG.info("USRMNGT: Data: get_current_device_ip: Returning 'my' device IP address = " + str(agent['device_ip']))
        return agent['device_ip']
    else:
        return -1


# FUNCTION: get_leader_device_ip
def get_leader_device_ip():
    LOG.info("USRMNGT: Data: get_leader_device_ip: Getting 'leader' ID from 'agent' resource ...")
    # get from AGENT resource
    agent = cimi.get_agent_info()
    LOG.debug("USRMNGT: Data: get_leader_device_ip: agent = " + str(agent))
    if not agent is None and agent != -1:
        LOG.info("USRMNGT: Data: get_leader_device_ip: Returning 'leader' ID = " + str(agent['leader_id']))
        return agent['leader_id']
    else:
        return -1


# FUNCTION: get_agent_info
def get_agent_info():
    LOG.info("USRMNGT: Data: get_agent_info: Getting 'agent' resource ...")
    # get from AGENT resource
    agent = cimi.get_agent_info()
    LOG.debug("USRMNGT: Data: get_agent_info: agent = " + str(agent))
    if not agent is None and agent != -1:
        return agent
    else:
        return -1


# FUNCTION: exist_device: check if 'device id' exists
def exist_device(device_id):
    return cimi.exist_device(device_id)


###############################################################################
# USER


# FUNCTION: get_user_info: gets user info
def get_user_info(user_id):
    user_id = user_id.replace('user/', '')
    LOG.debug("USRMNGT: Data: get_user_info: " + user_id)
    # check user's permissions on current device
    current_user_id = vol.read_user_id()
    current_user_id = current_user_id.replace('user/', '')
    if current_user_id == user_id:
        return cimi.get_resource_by_id("user/" + user_id)
    else:
        return -1


# FUNCTION: delete_user: deletes user
def delete_user(user_id):
    user_id = user_id.replace('user/', '')
    LOG.debug("USRMNGT: Data: delete_user: " + user_id)

    # 1. check user's permissions on current device
    current_user_id = vol.read_user_id()
    current_user_id = current_user_id.replace('user/', '')
    if current_user_id == user_id:
        # TODO 2. delete profiles and sharing models from devices

        # 3. delete user
        return cimi.delete_resource("user/" + user_id)
    else:
        return -1


###############################################################################
# SHARING MODEL

# FUNCTION: get_user_profile_by_id
def get_sharing_model_by_id(sharing_model_id):
    sharing_model_id = sharing_model_id.replace('sharing-model/', '')
    LOG.debug("USRMNGT: Data: get_sharing_model_by_id: " + sharing_model_id)

    sharing_model = cimi.get_resource_by_id("sharing-model/" + sharing_model_id)
    #if not sharing_model['status'] is None and sharing_model['status'] == 404:
    #    return -1
    return sharing_model  # cimi.get_resource_by_id("sharing-model/" + sharing_model_id)


# Get shared resources
def get_sharing_model(device_id):
    LOG.info("USRMNGT: Data: get_sharing_model: " + device_id)
    return cimi.get_sharing_model(device_id)


# Initializes shared resources values
def init_sharing_model(data):
    LOG.info("USRMNGT: Data: init_sharing_model: " + str(data))
    return cimi.add_resource(config.dic['CIMI_SHARING_MODELS'], data)


# Updates shared resources values
def update_sharing_model_by_id(sharing_model_id, data):
    sharing_model_id = sharing_model_id.replace('sharing-model/', '')
    LOG.info("USRMNGT: Data: update_sharing_model_by_id: " + sharing_model_id + ", " + str(data))
    resp = cimi.get_resource_by_id("sharing-model/" + sharing_model_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# delete_sharing_model_by_id: Deletes  shared resources values
def delete_sharing_model_by_id(sharing_model_id):
    sharing_model_id = sharing_model_id.replace('sharing-model/', '')
    LOG.info("USRMNGT: Data: delete_sharing_model_by_id: " + sharing_model_id)
    resp = cimi.get_resource_by_id("sharing-model/" + sharing_model_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None


# FUNCTION: get_current_sharing_model: Get current SHARING-MODEL
def get_current_sharing_model():
    LOG.debug("USRMNGT: Data: get_current_sharing_model: Getting information about current user and device ...")

    device_id = get_current_device_id()  # get 'my' device_id from 'agent' resource
    LOG.debug("USRMNGT: Data: get_current_sharing_model: device_id=" + device_id)

    if device_id == -1:
        LOG.warning("USRMNGT: Data: get_current_sharing_model: No device found; Returning None ...")
        return None
    else:
        return cimi.get_sharing_model(device_id)


###############################################################################
# USER-PROFILE

# get_user_profile_by_id
def get_user_profile_by_id(profile_id):
    profile_id = profile_id.replace('user-profile/', '')
    LOG.debug("USRMNGT: Data: get_user_profile_by_id: " + profile_id)
    return cimi.get_resource_by_id("user-profile/" + profile_id)


# get_user_profile: Get user profile
def get_user_profile(device_id):
    LOG.debug("USRMNGT: Data: get_user_profile: device_id=" + device_id)
    return cimi.get_user_profile(device_id)


# update_user_profile_by_id: Updates a profile
def update_user_profile_by_id(profile_id, data):
    profile_id = profile_id.replace('user-profile/', '')
    LOG.debug("USRMNGT: Data: update_user_profile_by_id: " + profile_id + ", " + str(data))
    resp = cimi.get_resource_by_id("user-profile/" + profile_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# Deletes users profile
def delete_user_profile_by_id(profile_id):
    profile_id = profile_id.replace('user-profile/', '')
    LOG.debug("USRMNGT: Data: delete_user_profile_by_id: Delete Profile [" + profile_id + "]")
    resp = cimi.get_resource_by_id("user-profile/" + profile_id)
    if resp and resp == -1:
        return None
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None


# Initializes users profile
def register_user(data):
    LOG.debug("USRMNGT: Data: register_user: Creating new Profile for user [data=" + str(data) + "] ...")
    return cimi.add_resource(config.dic['CIMI_PROFILES'], data)


# setAPPS_RUNNING
def setAPPS_RUNNING(apps=0):
    config.APPS_RUNNING = config.APPS_RUNNING + apps
    if config.APPS_RUNNING < 0:
        config.APPS_RUNNING = 0


# FUNCTION: get_current_user_profile: Get Current USER-PROFILE
def get_current_user_profile():
    LOG.debug("USRMNGT: Data: get_current_user_profile: Getting information about current user and device ...")

    device_id = get_current_device_id() # get 'my' device_id from 'agent' resource
    LOG.debug("USRMNGT: Data: get_current_user_profile: device_id=" + device_id)

    if device_id == -1:
        LOG.warning("USRMNGT: Data: get_current_user_profile: No device found; Returning None ...")
        return None
    else:
        return cimi.get_user_profile(device_id)


###############################################################################
## AGENT INFO
## power, apps running ...

# TODO
# FUNCTION: get_total_services_running: Get services running
def get_total_services_running():
    LOG.debug("USRMNGT: Data: get_total_services_running: Total of services running in device = " + str(config.APPS_RUNNING))
    return config.APPS_RUNNING


# FUNCTION: get_power: Get battery level from DEVICE_DYNAMIC
def get_power():
    device_id = get_current_device_id() # get 'my' device_id
    LOG.info("USRMNGT: Data: get_power: Getting power status from device [" + device_id + "] ...")
    return cimi.get_power(device_id)


###############################################################################
## LOCAL VOLUME
## Used to store / read 'user_id' and 'device_id'

# FUNCTION: save_device_id
def save_device_id(device_id):
    vol.save_device_id(device_id)


# FUNCTION: read_device_id
def read_device_id():
    vol.read_device_id()
