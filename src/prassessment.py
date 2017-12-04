'''
User Management Assesment process / daemon
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python

import requests
import time
import threading
import logs


execute = True
d = None


# daemon process
def daemon():
    global execute
    try:
        while execute:
            # TODO
            logs.info('>> assessment daemon >> executing ...')

            # 1. get profile

            # 2. get shared resources

            # 3. get services running in device

            # 4. get resources used by apps ==> landscaper.GetSubgraph(serviceID)
            # http://docs.python-requests.org/en/master/
            # r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
            # if r.status_code == 200:
            #     logs.info('status_code = 200')
            # else:
            #     logs.error('Error (1): status_code != 200')

            # 5. compare and send warning if needed

            time.sleep(10)
    except:
        logs.error('Error (0)')
        return {'module': 'assesment-process', 'result': 'Exception', 'message': 'Error (0)'}


# start process
def start():
    global execute
    global d
    try:
        execute = True
        if d is None:
            d = threading.Thread(name='daemon', target=daemon)
            d.setDaemon(True)
            d.start()
            return "started"
        else:
            if execute == False and d.isAlive() == False:
                d.setDaemon(True)
                d.start()
                return "started"
            else:
                logs.warning('>> start() >> execute: ' + str(execute) + '; d.isAlive(): ' + str(d.isAlive()))
                return "???"
    except:
        logs.error('Error (0)')
        return "Exception"


# stop process
def stop():
    global execute
    global d
    try:
        execute = False
        if d is None:
            logs.warning('>> stop() >> execute: ' + str(execute) + '; d.isAlive(): None')
            return "Stopped"
        else:
            d.join()
            return "Stopped"
    except:
        logs.error('Error (0)')
        return "Exception"



# return status
def getStatus():
    global execute
    global d

    if d is None:
        return "Not initialized"
    elif execute == True and d.isAlive() == True:
        return "Running"
    else:
        return "Stopped"