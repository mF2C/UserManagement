"""
User Management Assesment module operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 11 april 2019

@author: Roi Sucasas - ATOS
"""

from usermgnt.data import data_adapter as data_adapter
from usermgnt.common.logs import LOG
from usermgnt.common import common as common


# FUNCTION: __getCurrent:
def __getCurrentUser():
    LOG.info("[usermgnt.modules.current] [__getCurrentUser] Getting current user ...")
    user_profile = data_adapter.get_current_user_profile()
    if user_profile is None:
        return common.gen_response(500, 'Error', 'cause', 'not found / error', 'user', '')
    elif user_profile == -1:
        return common.gen_response_ko('Warning: User profile not found', 'cause', 'not found / error', 'user', '')
    else:
        return common.gen_response_ok('User found', 'user_profile', user_profile, 'user_id', user_profile['acl']['owner']['principal'])


# FUNCTION: __getCurrent:
def __getCurrentDevice():
    LOG.info("[usermgnt.modules.current] [__getCurrentDevice] Getting current device ...")
    user_profile = data_adapter.get_current_user_profile()
    if user_profile is None:
        return common.gen_response(500, 'Error', 'cause', 'not found / error', 'device', '')
    elif user_profile == -1:
        return common.gen_response_ko('Warning: User profile not found', 'cause', 'not found / error', 'device', '')
    else:
        return common.gen_response_ok('User found', 'user_profile', user_profile, 'device', user_profile['device_id'])


# FUNCTION: __getCurrentAll:
def __getCurrentAll():
    LOG.info("[usermgnt.modules.current] [__getCurrentAll] Getting current device ...")
    user_profile = data_adapter.get_current_user_profile()
    sharing_model = data_adapter.get_current_sharing_model()
    agent = data_adapter.get_agent_info()
    if user_profile is None:
        return common.gen_response(500, 'Error', 'cause', 'not found / error', 'info', {})
    elif user_profile == -1:
        return common.gen_response_ko('Warning: user_profile / sharing_model / agent not found', 'cause', 'not found / error', 'info', {})
    else:
        return common.gen_response_ok('User found', 'info', {"user_profile":user_profile,
                                                             "sharing_model":sharing_model,
                                                             "agent":agent})


# FUNCTION: getCurrent:
def getCurrent(val):
    LOG.info("[usermgnt.modules.current] [getCurrent] Getting current " + val + " ...")
    if val == "user":
        return __getCurrentUser()
    elif val == "device":
        return __getCurrentDevice()
    elif val == "all":
        return __getCurrentAll()
    else:
        return common.gen_response(404, "Error", "parameter", val, "message", "Parameter '" + val + "' not allowed")