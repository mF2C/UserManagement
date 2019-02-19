"""
User Management Assesment process / daemon
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import time
import threading
import usermgnt.mF2C.mf2c as mf2c
import usermgnt.mF2C.data as datamgmt
from common.logs import LOG


execute = True
d = None


# check_resources_used: checks if the resources used by mF2C apps, match the user's profiling and sharing model properties
# TODO
def check_resources_used(user_profile, sharing_model, battery_level, total_services):
    try:
        LOG.debug("User-Management: << Assessment Process: check_resources_used >> [battery_level=" + str(battery_level) + "], "
                  "[total_services=" + str(total_services) + "]")

        result = {}
        if battery_level > sharing_model['battery_limit']:
            result['battery_limit_violation'] = True
        if total_services <= user_profile['max_apps']:
            result['max_apps_violation'] = True
    except:
        LOG.error('User-Management: << Assessment Process: check_resources_used >> check_resources_used >> Exception')
    return result


# daemon process
def daemon():
    global execute
    try:
        while execute:
            LOG.debug('User-Management: << Assessment Process: daemon >> executing ...')

            device_id = None
            user_id = None

            # 1. get current profile
            user_profile = datamgmt.get_current_user_profile()
            if user_profile is None:
                LOG.error('User-Management: << Assessment Process: daemon >> user_profile not found / error')
            elif user_profile == -1:
                LOG.warning('User-Management: << Assessment Process: daemon >> user_profile not found')
            else:
                user_id = user_profile['user_id']
                device_id = user_profile['device_id']
                LOG.debug('User-Management: << Assessment Process: daemon >> executing ...')

            # 2. get current sharing model
            sharing_model = datamgmt.get_current_sharing_model()
            if sharing_model is None:
                LOG.error('User-Management: << Assessment Process: daemon >> sharing_model not found / error')
            elif sharing_model == -1:
                LOG.warning('User-Management: << Assessment Process: daemon >> sharing_model not found')
            else:
                user_id = sharing_model['user_id']
                device_id = sharing_model['device_id']
                LOG.debug('User-Management: << Assessment Process: daemon >> executing ...')

            if not user_id is None and not device_id is None:
                LOG.debug('User-Management: << Assessment Process: daemon >> checking values ...')
                # 3. Get information:
                #   - battery
                battery_level = datamgmt.get_power(device_id)
                battery_level = 50 # TODO
                #   - total services running
                total_services = datamgmt.get_total_services_running(device_id)

                # 4. check information and send warning to Lifecycle if needed
                result = check_resources_used(user_profile, sharing_model, battery_level, total_services)
                LOG.debug("User-Management: << Assessment Process: daemon >> result: " + str(result))
                if not result:
                    LOG.debug('User-Management: << Assessment Process: daemon >> generating warning / sending notification ...')
                    mf2c.send_warning(user_id, device_id, user_profile, sharing_model, result)
            else:
                LOG.warning('User-Management: << Assessment Process: daemon >> cannot check values')

            # wait 60 seconds
            time.sleep(60)
    except:
        LOG.error('User-Management: << Assessment Process: daemon >> Exception')


# start process
def start():
    global execute
    global d

    execute = True
    if d is None:
        d = threading.Thread(name='daemon', target=daemon)
        d.setDaemon(True)
        d.start()
        return "started"
    elif execute == False and d.isAlive() == False:
        d.setDaemon(True)
        d.start()
        return "started"
    else:
        LOG.warning('User-Management: << Assessment Process: start >> execute: ' + str(execute) + '; d.isAlive(): ' + str(d.isAlive()))
        return "???"


# stop process
def stop():
    global execute
    global d

    execute = False
    if d is None:
        LOG.warning('User-Management: << Assessment Process: stop >> execute: ' + str(execute) + '; d.isAlive(): None')
        return "Stopped"
    else:
        d.join()
        return "Stopped"


# return status
def get_status():
    global execute
    global d

    if d is None:
        return "Not initialized"
    elif execute and d.isAlive() == True:
        return "Running"
    else:
        return "Stopped"