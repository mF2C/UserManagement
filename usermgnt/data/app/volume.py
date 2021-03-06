"""
Data Management: dataclay, cimi...
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 april 2019

@author: Roi Sucasas - ATOS
"""

from usermgnt.common.logs import LOG
from usermgnt.common.common import TRACE
import config


###############################################################################
## LOCAL VOLUME

# save_device_id
def save_device_id(device_id):
    try:
        LOG.log(TRACE, "[usermgnt.data.app.volume] [save_device_id] Storing 'device_id' [" + device_id + "] value in local VOLUME [" + config.dic['UM_WORKING_DIR_VOLUME'] + "] ...")
        with open(config.dic['UM_WORKING_DIR_VOLUME'] + "device_id.txt", "w") as file:
            file.write(device_id)
    except:
        LOG.error("[usermgnt.data.app.volume] [save_device_id] UM could not save 'device_id' value in " + config.dic['UM_WORKING_DIR_VOLUME'] + "device_id.txt. Returning None ...")
        return None


# read_device_id
def read_device_id():
    LOG.log(TRACE, "[usermgnt.data.app.volume] [read_device_id] Reading 'device_id' value from local VOLUME [" + config.dic['UM_WORKING_DIR_VOLUME'] + "] ...")
    try:
        with open(config.dic['UM_WORKING_DIR_VOLUME'] + "device_id.txt", "r") as file:
            return file.readline()
    except:
        LOG.error("[usermgnt.data.app.volume] [read_device_id] UM could not get 'device_id' value from " + config.dic['UM_WORKING_DIR_VOLUME'] + "device_id.txt. Returning None ...")
        return None


# save_user_id
def save_user_id(user_id):
    try:
        LOG.log(TRACE, "[usermgnt.app.volume] [save_user_id] Storing user_id [" + user_id + "] value in local VOLUME [" + config.dic['UM_WORKING_DIR_VOLUME'] + "] ...")
        with open(config.dic['UM_WORKING_DIR_VOLUME'] + "user_id.txt", "w") as file:
            file.write(user_id)
    except:
        LOG.error("[usermgnt.data.app.volume] [save_user_id] UM could not save 'user_id' value in " + config.dic['UM_WORKING_DIR_VOLUME'] + "user_id.txt. Returning None ...")
        return None


# read_user_id
def read_user_id():
    LOG.log(TRACE, "[usermgnt.data.app.volume] [read_user_id] Reading user_id value from local VOLUME [" + config.dic['UM_WORKING_DIR_VOLUME'] + "] ...")
    try:
        with open(config.dic['UM_WORKING_DIR_VOLUME'] + "user_id.txt", "r") as file:
            return file.readline()
    except:
        LOG.error("[usermgnt.data.app.volume] [read_user_id] UM could not save 'user_id' value in " + config.dic['UM_WORKING_DIR_VOLUME'] + "user_id.txt. Returning None ...")
        return None