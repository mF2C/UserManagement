"""
User Management Assesment module operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 28 march 2019

@author: Roi Sucasas - ATOS
"""

from usermgnt.common.logs import LOG
from usermgnt.common import common as common
from usermgnt.mF2C import data as datamgmt


message = ""

# __up_policies
def __up_policies():
    global message
    try:
        LOG.debug("[usermgnt.modules.policies] [__up_policies] Checking policies ...")

        # get current profile
        user_profile = datamgmt.get_current_user_profile()
        if user_profile is None:
            LOG.error('[usermgnt.modules.policies] [__up_policies] user_profile not found / error')
        elif user_profile == -1:
            LOG.warning('[usermgnt.modules.policies] [__up_policies] user_profile not found')
        else:
            LOG.debug('[usermgnt.modules.policies] [__up_policies] user_profile found. checking values ...')
            if user_profile['resource_contributor']:
                message = message + "ALLOWED: resource_contributor is set to TRUE"
                return True
            message = message + "NOT ALLOWED: resource_contributor is set to FALSE"
    except:
        LOG.exception('[usermgnt.modules.policies] [__up_policies] Exception')
    return False


# sm_policies
def __sm_policies():
    global message
    try:
        LOG.debug("[usermgnt.modules.policies] [__sm_policies] Checking policies ...")

        # get current sharing model
        sharing_model = datamgmt.get_current_sharing_model()
        if sharing_model is None:
            LOG.error('[usermgnt.modules.policies] [__sm_policies] sharing_model not found / error')
        elif sharing_model == -1:
            LOG.warning('[usermgnt.modules.policies] [__sm_policies] sharing_model not found')
        else:
            LOG.debug('[usermgnt.modules.policies] [__sm_policies] sharing_model found. checking values ...')
            # 1. battery_level
            battery_level = datamgmt.get_power()
            LOG.debug("[usermgnt.modules.policies] [__sm_policies] 1. [battery_level=" + str(battery_level) + "] ... [sharing_model('battery_limit')=" +
                      str(sharing_model['battery_limit']) + "]")
            if battery_level is None or battery_level == -1 or battery_level > sharing_model['battery_limit']:
                # 2. total services running
                apps_running = datamgmt.get_total_services_running()
                LOG.debug("[usermgnt.modules.policies] [__sm_policies] 2. [apps_running=" + str(apps_running) + "] ... [sharing_model('max_apps')=" +
                          str(sharing_model['max_apps']) + "]")
                if apps_running >= sharing_model['max_apps']:
                    message = message + "NOT ALLOWED: apps_running >= max_apps"
                    return False
                return True
            else:
                message = message + "NOT ALLOWED: battery_level < battery_limit"
                return False
    except:
        LOG.exception('[usermgnt.modules.policies] [__sm_policies] Exception')
    return False


# check_policies
def check_policies():
    global message
    message = ""
    if __up_policies() and __sm_policies():
        return common.gen_response_ok("User Management Policies", "result", True, "message", message)
    return common.gen_response_ok("User Management Policies", "result", False, "message", message)
