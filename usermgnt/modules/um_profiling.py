"""
Profiling operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import usermgnt.mF2C.data as datamgmt
import common.common as common
from common.logs import LOG


# Profile content:
#  {
#       "user_id": "user/0000000000u",
#       "device_id": "device/11111111d",
#  	    "max_apps": 1,
#  	    "service_consumer": boolean,
#  	    "resource_contributor": boolean
#  }

# get_user_profile_by_id: Get user profile by ID
def get_user_profile_by_id(profile_id):
    LOG.debug("USRMNGT: Profiling module: get_user_profile_by_id: " + str(profile_id))
    user_profile = datamgmt.get_user_profile_by_id(profile_id)
    if user_profile is None:
        return common.gen_response(500, 'Error', 'profile_id', profile_id, 'profile', {})
    elif user_profile == -1:
        return common.gen_response_ko('Warning: User profile not found', 'profile_id', profile_id, 'profile', {})
    else:
        return common.gen_response_ok('User found', 'profile_id', profile_id, 'profile', user_profile)


# get_user_profile: Get user profile
def get_user_profile(user_id, device_id):
    LOG.debug("USRMNGT: Profiling module: get_user_profile: " + str(user_id) + ", " + str(device_id))
    user_profile = datamgmt.get_user_profile(user_id, device_id)
    if user_profile is None:
        return common.gen_response(500, 'Error', 'user_id', user_id, 'device_id', device_id)
    elif user_profile == -1:
        return common.gen_response_ko('Warning: User profile not found', 'user_id', user_id, 'device_id', device_id)
    else:
        return common.gen_response_ok('User found', 'user_id', user_id, 'profile', user_profile)


# get_current_user_profile: Get current user profile
def get_current_user_profile():
    LOG.info("USRMNGT: Profiling module: get_current_user_profile: getting current user-device value ...")
    user_profile = datamgmt.get_current_user_profile()
    if user_profile is None:
        return common.gen_response(500, 'Error', 'user_profile', 'not found / error', 'profile', {})
    elif user_profile == -1:
        return common.gen_response_ko('Warning: User profile not found', 'user_profile', 'not found / error', 'profile', {})
    else:
        return common.gen_response_ok('User found', 'user_profile', user_profile)


# setAPPS_RUNNING
def updateUM(data):
    LOG.info("USRMNGT: Profiling module: register_user: " + str(data))
    if 'apps_running' in data:
        datamgmt.setAPPS_RUNNING(data['apps_running'])


# Initializes users profile
def create_user_profile(data):
    LOG.info("USRMNGT: Profiling module: register_user: " + str(data))
    if 'user_id' not in data or 'device_id' not in data or 'service_consumer' not in data or 'resource_contributor' not in data or 'max_apps' not in data:
        LOG.warning('USRMNGT: Profiling module: register_user: parameter not found: user_id / device_id / service_consumer'
                    ' / resource_contributor / max_apps')
        return common.gen_response(405, 'parameter not found: user_id / device_id / service_consumer / resource_contributor / max_apps', 'data', str(data))

    # check if user exists
    if not datamgmt.exist_user(data['user_id']):
        return common.gen_response(404, "Error", "user_id", data['user_id'], "message", "User ID not found")

    # check if device exists
    if not datamgmt.exist_device(data['device_id']):
        return common.gen_response(404, "Error", "device_id", data['device_id'], "message", "Device ID not found")

    # check if profile exists
    user_id = data['user_id']
    device_id = data['device_id']
    user_profile = datamgmt.get_user_profile(user_id, device_id)

    if user_profile == -1 or user_profile is None:
        # register user/profile
        user_profile = datamgmt.register_user(data)
        if user_profile is None:
            return common.gen_response(500, 'Error', 'profile', {})
        else:
            return common.gen_response_ok('User Profile registered', 'user_id', user_id, 'profile', user_profile)
    else:
        return common.gen_response_ko('Warning: User Profile already exists', 'user_id', user_id, 'profile', user_profile)


# update_user_profile: Updates users profile
def update_user_profile_by_id(profile_id, data):
    LOG.debug("USRMNGT: Profiling module: profile_id: " + str(profile_id) + ", " + str(data))
    # update user
    user_profile = datamgmt.update_user_profile_by_id(profile_id, data)
    if user_profile is None:
        return common.gen_response(500, 'Error', 'profile_id', profile_id, 'profile', {})
    elif user_profile == -1:
        return common.gen_response_ko('Warning: User profile not found', 'profile_id', profile_id, 'profile', {})
    else:
        return common.gen_response_ok('User updated', 'profile_id', profile_id, 'profile', user_profile)


# update_user_profile: Updates users profile
def update_user_profile(user_id, device_id, data):
    LOG.debug("USRMNGT: Profiling module: update_user_profile: " + str(user_id) + ", " + str(device_id) + ", " + str(data))
    # update user
    user_profile = datamgmt.update_user_profile(user_id, device_id, data)
    if user_profile is None:
        return common.gen_response(500, 'Error', 'profile', {})
    elif user_profile == -1:
        return common.gen_response_ko('Warning: User profile not found', 'user_id', user_id, 'device_id', device_id)
    else:
        return common.gen_response_ok('User updated', 'user_id', user_id, 'profile', user_profile)


# delete_user_profile: Deletes users profile
def delete_user_profile_by_id(profile_id):
    LOG.info("USRMNGT: Profiling module: delete_user_profile_by_id: " + profile_id)
    # delete profile
    if datamgmt.delete_user_profile_by_id(profile_id) is None:
        return common.gen_response(500, 'Error', 'profile_id', profile_id)
    else:
        return common.gen_response_ok('Profile deleted', 'profile_id', profile_id)


# delete_user_profile: Deletes users profile
def delete_user_profile(user_id, device_id):
    LOG.info("USRMNGT: Profiling module: delete_user_profile: " + user_id + ", " + device_id)
    # delete profile
    if datamgmt.delete_user_profile(user_id, device_id) is None:
        return common.gen_response(500, 'Error', 'user_id', user_id)
    else:
        return common.gen_response_ok('Profile deleted', 'user_id', user_id)


