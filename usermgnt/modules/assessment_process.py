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
import usermgnt.mF2C.dependencies as dependencies
import usermgnt.mF2C.data as datamgmt
from usermgnt.utils.logs import LOG


execute = True
d = None


# checks if the resources used by mF2C apps, match the user's profiling and sharing model properties
# TODO
def check_resources_used(list_resources_used, profile, shared_model):
    try:
        for item in list_resources_used:
            LOG.debug('User-Management: >> check_resources_used: ' + item)
        return True
    except:
        LOG.error('User-Management >> check_resources_used >> Exception')
    return True


# daemon process
def daemon():
    global execute
    try:
        while execute:
            LOG.debug('User-Management: >> assessment daemon >> executing ...')

            # 0. get user_id & device_id # TODO
            user_id = "user_id" # TODO user_id?
            device_id = "device_id" # TODO device_id?

            # 1. get profile
            profile = datamgmt.get_profiling(user_id)

            # 2. get shared resources
            shared_model = datamgmt.get_sharing_model_values(user_id) # TODO

            # 3. get services running in device or get all allowed services
            allowed_services = datamgmt.get_services(user_id)

            # 4. get resources used by apps ==> landscaper.GetSubgraph(serviceID)
            if not allowed_services:
                LOG.debug('User-Management: >> No services found / services list is empty')
            else:
                list_resources_used = []
                for serviceID in allowed_services:
                    resources_used = dependencies.get_resources_used_by_service(serviceID) # TODO
                    list_resources_used.append(resources_used)

                # 5. check information and send warning to Lifecycle if needed
                if not check_resources_used(list_resources_used, profile, shared_model): # TODO
                    dependencies.send_warning(user_id, device_id, list_resources_used, profile, shared_model)

            # wait 30 seconds
            time.sleep(30)
    except:
        LOG.error('User-Management >> assessment daemon >> Exception')


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
        LOG.warning('User-Management: Assesment process: start() >> execute: ' + str(execute) + '; d.isAlive(): ' + str(d.isAlive()))
        return "???"


# stop process
def stop():
    global execute
    global d

    execute = False
    if d is None:
        LOG.warning('User-Management: Assesment process: stop() >> execute: ' + str(execute) + '; d.isAlive(): None')
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
    elif execute == True and d.isAlive() == True:
        return "Running"
    else:
        return "Stopped"