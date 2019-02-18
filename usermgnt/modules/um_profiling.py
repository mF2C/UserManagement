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


# Get user profile
def get_profiling(user_id, device_id):
    if not user_id is None and not device_id is None:
        LOG.debug("User-Management: Profiling module: get_profiling: " + str(user_id) + ", " + str(device_id))

        user_profile = datamgmt.get_profile_user_device(user_id, device_id)
        if user_profile is None:
            return common.gen_response(500, 'Error', 'user_id', user_id, 'device_id', device_id)
        elif user_profile == -1:
            return common.gen_response_ko('Warning: User profile not found', 'user_id', user_id, 'device_id', device_id)
        else:
            return common.gen_response_ok('User found', 'user_id', user_id, 'profile', user_profile)

    else:
        # TODO!!!
        LOG.info("User-Management: Profiling module: get_profiling: getting current user-device value ...")

        # get device
        device_id = ""
        # get user
        user_id = ""
        user_profile = datamgmt.get_profiling(user_id)

        if user_profile is None:
            return common.gen_response(500, 'Error', 'user_id', user_id, 'profile', {})
        elif user_profile == -1:
            return common.gen_response_ko('Warning: User profile not found', 'user_id', user_id, 'profile', {})
        else:
            return common.gen_response_ok('User found', 'user_id', user_id, 'profile', user_profile)


# Get user allowed services
def get_services(user_id):
    LOG.info("User-Management: Profiling module: get_services: " + str(user_id))

    # get user
    services = datamgmt.get_services(user_id)
    if services is None:
        return common.gen_response(500, 'Error', 'user_id', user_id, 'services', {})
    else:
        return common.gen_response_ok('Services found', 'user_id', user_id, 'services', services)


# Initializes users profile
def register_user(data):
    LOG.info("User-Management: Profiling module: register_user: " + str(data))
    if 'user_id' not in data or 'device_id' not in data or 'service_consumer' not in data or 'resource_contributor' not in data or 'max_apps' not in data:
        LOG.warning('User-Management: Profiling module: register_user: parameter not found: user_id / device_id / service_consumer'
                    ' / resource_contributor / max_apps')
        return common.gen_response(405, 'parameter not found: user_id / device_id / service_consumer / resource_contributor / max_apps', 'data', str(data))

    # check if profile exists
    user_id = data['user_id']

    user_profile = datamgmt.get_profiling(user_id)
    if user_profile == -1 or user_profile is None:
        # register user/profile
        user_profile = datamgmt.register_user(data)
        if user_profile is None:
            return common.gen_response(500, 'Error', 'profile', {})
        else:
            return common.gen_response_ok('User registered', 'user_id', user_id, 'profile', user_profile)
    else:
        return common.gen_response_ko('Warning: User profile already exists', 'user_id', user_id, 'profile', user_profile)


# Updates users profile
#   data: {'user_id':'', 'email':'', 'service_consumer': '', 'resource_contributor': ''}
def update_profile(user_id, device_id, data):
    LOG.debug("User-Management: Profiling module: update_profile: " + str(user_id) + ", " + str(device_id) + ", " + str(data))
    # update user
    user_profile = datamgmt.update_profile(user_id, device_id, data)
    if user_profile is None:
        return common.gen_response(500, 'Error', 'profile', {})
    elif user_profile == -1:
        return common.gen_response_ko('Warning: User profile not found', 'user_id', user_id, 'device_id', device_id)
    else:
        return common.gen_response_ok('User updated', 'user_id', user_id, 'profile', user_profile)


# Deletes users profile
#   data: {'user_id':''}
def delete_profile(user_id, device_id):
    LOG.info("User-Management: Profiling module: delete_profile: " + user_id + ", " + device_id)
    # delete profile
    if datamgmt.delete_profile(user_id, device_id) is None:
        return common.gen_response(500, 'Error', 'user_id', user_id)
    else:
        return common.gen_response_ok('Profile deleted', 'user_id', user_id)


