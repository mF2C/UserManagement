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
#       "device_id": "device/11111111d",
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


# Initializes users profile
def create_user_profile(data):
    LOG.info("USRMNGT: Profiling module: register_user: " + str(data))

    # check if profile exists
    device_id = data['device_id']
    user_profile = datamgmt.get_user_profile(device_id)
    datamgmt.save_device_id(device_id)

    if user_profile == -1 or user_profile is None:
        # register user/profile
        user_profile = datamgmt.register_user(data)
        if user_profile is None:
            return None
        else:
            return user_profile
    else:
        return user_profile


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


# delete_user_profile: Deletes users profile
def delete_user_profile_by_id(profile_id):
    LOG.info("USRMNGT: Profiling module: delete_user_profile_by_id: " + profile_id)
    # delete profile
    if datamgmt.delete_user_profile_by_id(profile_id) is None:
        return common.gen_response(500, 'Error', 'profile_id', profile_id)
    else:
        return common.gen_response_ok('Profile deleted', 'profile_id', profile_id)


