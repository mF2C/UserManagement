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


execute = False
d = None


# check_resources_used: checks if the resources used by mF2C apps, match the user's profiling and sharing model properties
def check_resources_used(user_profile, sharing_model, battery_level, total_services):
    try:
        LOG.debug("USRMNGT: << Assessment Process: check_resources_used >> [battery_level=" + str(battery_level) + "], "
                  "[total_services=" + str(total_services) + "]")

        result = {}
        if battery_level <= sharing_model['battery_limit']:
            result['battery_limit_violation'] = True

        if not user_profile['resource_contributor'] and total_services > 0:
            result['resource_contributor_violation'] = True

        if total_services > user_profile['max_apps']:
            result['max_apps_violation'] = True
    except:
        LOG.exception('USRMNGT: << Assessment Process: check_resources_used >> check_resources_used >> Exception')
    return result # TODO check if empty


# daemon process
def daemon():
    global execute
    try:
        while execute:
            LOG.debug('USRMNGT: << Assessment Process: daemon >> executing ...')

            device_id = None
            user_id = None

            # 1. get current profile
            user_profile = datamgmt.get_current_user_profile()
            if user_profile is None:
                LOG.error('USRMNGT: << Assessment Process: daemon >> user_profile not found / error')
            elif user_profile == -1:
                LOG.warning('USRMNGT: << Assessment Process: daemon >> user_profile not found')
            else:
                user_id = user_profile['user_id']
                device_id = user_profile['device_id']
                LOG.debug('USRMNGT: << Assessment Process: daemon >> user_profile found')

            # 2. get current sharing model
            sharing_model = datamgmt.get_current_sharing_model()
            if sharing_model is None:
                LOG.error('USRMNGT: << Assessment Process: daemon >> sharing_model not found / error')
            elif sharing_model == -1:
                LOG.warning('USRMNGT: << Assessment Process: daemon >> sharing_model not found')
            else:
                user_id = sharing_model['user_id']
                device_id = sharing_model['device_id']
                LOG.debug('User-Management: << Assessment Process: daemon >> sharing_model found')

            if not user_id is None and not device_id is None:
                LOG.debug('USRMNGT: << Assessment Process: daemon >> checking values ...')
                # 3. Get information:
                #   - battery
                battery_level = datamgmt.get_power()
                battery_level = 50 # TODO
                #   - total services running
                total_services = datamgmt.get_total_services_running()

                # 4. check information and send warning to Lifecycle if needed
                result = check_resources_used(user_profile, sharing_model, battery_level, total_services)
                if not result:
                    LOG.debug("USRMNGT: << Assessment Process: daemon >> no violations: result: " + str(result))
                else:
                    LOG.debug("USRMNGT: << Assessment Process: daemon >> violations found: result: " + str(result))
                    LOG.debug('USRMNGT: << Assessment Process: daemon >> generating warning / sending notification ...')
                    mf2c.send_warning(user_id, device_id, user_profile, sharing_model, result)
            else:
                LOG.warning('USRMNGT: << Assessment Process: daemon >> cannot check values')

            # wait 60 seconds
            time.sleep(60)
    except:
        LOG.exception('USRMNGT: << Assessment Process: daemon >> Exception')


# start process
def start():
    global execute
    global d

    LOG.debug("USRMNGT: << Assessment Process: start >> Starting assessment process [execute=" + str(execute) + "]")

    if d is None:
        LOG.debug("USRMNGT: << Assessment Process: start >> [d is None]")
        d = threading.Thread(target=daemon) #(name='daemon', target=daemon)
        d.setDaemon(True)
        execute = True
        d.start()
        return "started"
    else:
        LOG.warning("USRMNGT: << Assessment Process: start >> [execute: " + str(execute) + "; d.isAlive(): " + str(d.isAlive()) + "]")
        return "???"


# stop process
def stop():
    global execute
    global d

    LOG.debug("USRMNGT: << Assessment Process: stop >> Stopping assessment process [execute=" + str(execute) + "]")

    if d is None:
        LOG.warning('USRMNGT: << Assessment Process: stop >> [execute: ' + str(execute) + '; d.isAlive(): None]')
        return "???"
    else:
        LOG.debug('USRMNGT: << Assessment Process: stop >> [d.join()]')
        execute = False
        d.join()
        d = None
        return "Stopped"


# return status
def get_status():
    global execute
    global d

    LOG.debug("USRMNGT: << Assessment Process: stop >> Getting assessment process status [execute=" + str(execute) + "]")

    if d is None:
        return "Not initialized"
    elif execute and d.isAlive() == True:
        return "Running"
    elif execute:
        return "???"
    else:
        return "Stopped"