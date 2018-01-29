"""
User Management Assesment process / daemon
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import config
import time
import threading
import requests
import src.modules.um_profiling as um_profiling
import src.modules.um_sharing_model as um_sharing_model
from src.utils.logs import LOG


execute = True
d = None


# daemon process
def daemon():
    global execute

    while execute:
        LOG.debug('User-Management: >> assessment daemon >> executing ...')

        # 1. get profile
        # TODO user_id?
        profile = um_profiling.get_profiling('user_id')

        # 2. get shared resources
        shared_model = um_sharing_model.get_sharing_model_values('user_id')

        # 3. get services running in device
        # TODO

        # 4. get resources used by apps ==> landscaper.GetSubgraph(serviceID)
        # TODO get services from PM Landscaper?
        r = requests.get(config.dic['URL_PM_LANDSCAPER'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            LOG.debug('User-Management: >> assessment daemon >> status_code=' + r.status_code + '; response: ' + r.text)
        else:
            LOG.error('User-Management: >> Error (1): status_code=' + r.status_code)

        # 5. compare and send warning if needed
        # TODO

        # 6. Send warning to Lifecycle
        # Warnings Handler: handle warnings coming from User Management Assessment:
        #   {
        #       "type": "um_warning",
        #       "data"
        #           {
        #               "user_id": "",
        #               "device_id": "",
        #               "service_id": "",
        #               "warning_id": "",
        #               "warning_txt": ""
        #           }
        #   }
        # TEST INTERACTION WITH OTHER COMPONENTS
        if config.dic['ENABLE_ASSESSMENT_TESTS']:
            LOG.debug('User-Management: >> assessment daemon >> sending warning to LIFECYCLE [' +
                       config.dic['URL_PM_LIFECYCLE'] + '] ...')
            param = "id_service"
            body = {"type": "um_warning",
                    "data": {
                        "user_id": "aaaaaa",
                        "device_id": "bbbbbb",
                        "service_id": "cccccc",
                        "warning_id": "dddddd",
                        "warning_txt": "eeeeee"}}
            r = requests.post(config.dic['URL_PM_LIFECYCLE'] + param, json=body, verify=config.dic['VERIFY_SSL'])
            if r.status_code == 200:
                LOG.debug('User-Management: >> assessment daemon >> status_code=' + r.status_code + '; response: ' + r.text)
            else:
                LOG.error('User-Management: >> Error (2): status_code=' + r.status_code)
            time.sleep(20)
        else:
            time.sleep(10)


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