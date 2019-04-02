"""
User Management Assesment module operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 28 march 2019

@author: Roi Sucasas - ATOS
"""


from common.logs import LOG
import common.common as common
import usermgnt.mF2C.data as datamgmt


message = ""

# up_policies
def up_policies():
    global message
    try:
        LOG.debug("USRMNGT: Policies: up_policies: Checking policies ...")

        # get current profile
        user_profile = datamgmt.get_current_user_profile()
        if user_profile is None:
            LOG.error('USRMNGT: Policies: up_policies: user_profile not found / error')
        elif user_profile == -1:
            LOG.warning('USRMNGT: Policies: up_policies: user_profile not found')
        else:
            LOG.debug('USRMNGT: Policies: up_policies: user_profile found. checking values ...')
            # check... TODO
            if user_profile['resource_contributor']:
                apps_running = datamgmt.get_total_services_running() # total services running
                if apps_running >= user_profile['max_apps']:
                    message = message + "NOT ALLOWED: apps_running >= max_apps"
                    return False
                return True

            message = message + "NOT ALLOWED: resource_contributor is set to FALSE"
    except:
        LOG.exception('USRMNGT: Policies: up_policies: Exception')
    return False


# sm_policies
def sm_policies():
    global message
    try:
        LOG.debug("USRMNGT: Policies: sm_policies: Checking policies ...")

        # get current sharing model
        sharing_model = datamgmt.get_current_sharing_model()
        if sharing_model is None:
            LOG.error('USRMNGT: Policies: sm_policies: sharing_model not found / error')
        elif sharing_model == -1:
            LOG.warning('USRMNGT: Policies: sm_policies: sharing_model not found')
        else:
            LOG.debug('User-Management: Policies: sm_policies: sharing_model found. checking values ...')
            # check ... TODO
            battery_level = datamgmt.get_power()
            battery_level = 50  # TODO
            if battery_level is None or battery_level == -1 or battery_level > sharing_model['battery_limit']:
                return True

    except:
        LOG.exception('USRMNGT: Policies: sm_policies: Exception')
    return False


# check_policies
def check_policies():
    global message
    message = ""
    if up_policies() and sm_policies():
        return common.gen_response_ok("User Management Policies", "result", True, "message", message)
    return common.gen_response_ok("User Management Policies", "result", False, "message", message)
