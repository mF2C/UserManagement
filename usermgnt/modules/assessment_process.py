"""
User Management Assesment process / daemon
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

import time, threading
from usermgnt.data import data_adapter as data_adapter
from usermgnt.data.atos import lifecycle as mf2c
from usermgnt.common.logs import LOG


execute = False
d = None


# check_resources_used: checks if the resources used by mF2C apps, match the user's profiling and sharing model properties
def __check_resources_used(user_profile, sharing_model, battery_level, total_services):
    try:
        LOG.debug("[usermgnt.modules.assessment] [__check_resources_used] << Assessment Process >> [battery_level=" + str(battery_level) + "], "
                  "[total_services=" + str(total_services) + "]")

        result = {}
        if battery_level <= sharing_model['battery_limit']:
            result['battery_limit_violation'] = True

        if not user_profile['resource_contributor'] and total_services > 0:
            result['resource_contributor_violation'] = True

        if total_services > sharing_model['max_apps']:
            result['max_apps_violation'] = True
    except:
        LOG.exception('[usermgnt.modules.assessment] [__check_resources_used] << Assessment Process >> check_resources_used >> Exception')
    return result # TODO check if empty


# daemon process
def __daemon():
    global execute
    try:
        while execute:
            LOG.debug('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> executing ...')

            device_id = None
            user_id = None

            # 1. get current profile
            user_profile = data_adapter.get_current_user_profile()
            if user_profile is None:
                LOG.error('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> user_profile not found / error')
            elif user_profile == -1:
                LOG.warning('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> user_profile not found')
            else:
                user_id = user_profile['user_id']
                device_id = user_profile['device_id']
                LOG.debug('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> user_profile found')

            # 2. get current sharing model
            sharing_model = data_adapter.get_current_sharing_model()
            if sharing_model is None:
                LOG.error('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> sharing_model not found / error')
            elif sharing_model == -1:
                LOG.warning('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> sharing_model not found')
            else:
                user_id = sharing_model['user_id']
                device_id = sharing_model['device_id']
                LOG.debug('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> sharing_model found')

            if not user_id is None and not device_id is None:
                LOG.debug('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> checking values ...')
                # 3. Get information:
                #   - battery
                battery_level = data_adapter.get_power()
                # battery_level = 50 # TODO
                #   - total services running
                total_services = data_adapter.get_total_services_running()

                # 4. check information and send warning to Lifecycle if needed
                result = __check_resources_used(user_profile, sharing_model, battery_level, total_services)
                if not result:
                    LOG.debug("[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> no violations: result: " + str(result))
                else:
                    LOG.debug("[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> violations found: result: " + str(result))
                    LOG.debug('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> generating warning / sending notification ...')
                    mf2c.send_warning(user_id, device_id, user_profile, sharing_model, result)
            else:
                LOG.warning('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> cannot check values')

            # wait 60 seconds
            time.sleep(60)
    except:
        LOG.exception('[usermgnt.modules.assessment] [__daemon] << Assessment Process Thread >> Exception')


# start process
def start():
    global execute
    global d

    LOG.debug("[usermgnt.modules.assessment] [start] << Assessment Process >> Starting assessment process [execute=" + str(execute) + "]")

    if d is None:
        LOG.debug("[usermgnt.modules.assessment] [start] << Assessment Process >> [d is None]")
        d = threading.Thread(target=__daemon) #(name='daemon', target=daemon)
        d.setDaemon(True)
        execute = True
        d.start()
        return "started"
    else:
        LOG.warning("[usermgnt.modules.assessment] [start] << Assessment Process >> [execute: " + str(execute) + "; d.isAlive(): " + str(d.isAlive()) + "]")
        return "???"


# stop process
def stop():
    global execute
    global d

    LOG.debug("[usermgnt.modules.assessment] [stop] << Assessment Process >> Stopping assessment process [execute=" + str(execute) + "]")

    if d is None:
        LOG.warning('[usermgnt.modules.assessment] [stop] << Assessment Process >> [execute: ' + str(execute) + '; d.isAlive(): None]')
        return "???"
    else:
        LOG.debug('[usermgnt.modules.assessment] [stop] << Assessment Process >> [d.join()]')
        execute = False
        d.join()
        d = None
        return "Stopped"


# return status
def get_status():
    global execute
    global d

    LOG.debug("[usermgnt.modules.assessment] [get_status] << Assessment Process >> Getting assessment process status [execute=" + str(execute) + "]")

    if d is None:
        return "Not initialized"
    elif execute and d.isAlive() == True:
        return "Running"
    elif execute:
        return "???"
    else:
        return "Stopped"