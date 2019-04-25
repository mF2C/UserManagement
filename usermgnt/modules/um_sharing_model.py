"""
Sharing Model operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import usermgnt.mF2C.data as datamgmt
import common.common as common
from common.logs import LOG


# Sharing model content:
# {
#       "device_id": "device/11111111d",
# 	    "gps_allowed": boolean,
# 	    "max_cpu_usage": integer,
# 	    "max_memory_usage": integer,
# 	    "max_storage_usage": integer,
# 	    "max_bandwidth_usage": integer,
#  	    "max_apps": 1,
# 	    "battery_limit": integer
# }


# setAPPS_RUNNING
def updateUM(data):
    LOG.info("USRMNGT: Profiling module: register_user: " + str(data))
    if 'apps_running' in data:
        datamgmt.setAPPS_RUNNING(data['apps_running'])


# get_sharing_model_by_id: Get shared resources
def get_sharing_model_by_id(sharing_model_id):
    LOG.info("USRMNGT: Sharing-model module: get_sharing_model_by_id: " + sharing_model_id)
    # get sharing_model
    sharing_model = datamgmt.get_sharing_model_by_id(sharing_model_id)
    if sharing_model is None:
        return common.gen_response(500, 'Exception', 'sharing_model_id', sharing_model_id, 'sharing_model', {})
    elif sharing_model == -1:
        return common.gen_response_ko('Warning: Sharing-model not found', 'sharing_model_id', sharing_model_id, 'sharing_model', {})
    else:
        return common.gen_response_ok('Sharing model found', 'sharing_model_id', sharing_model_id, 'sharing_model', sharing_model)


# get_current_sharing_model: Get current sharing model
def get_current_sharing_model():
    LOG.info("USRMNGT: Sharing-model module: get_current_sharing_model: getting current user-device value ...")
    sharing_model = datamgmt.get_current_sharing_model()
    if sharing_model is None:
        return common.gen_response(500, 'Error', 'sharing_model', 'not found / error', 'sharing_model', {})
    elif sharing_model == -1:
        return common.gen_response_ko('Warning: Sharing-model not found', 'sharing_model', 'not found / error', 'sharing_model', {})
    else:
        return common.gen_response_ok('Sharing-model found', 'sharing_model', sharing_model)


# Initializes shared resources values
def init_sharing_model(data):
    LOG.info("USRMNGT: Sharing-model module: init_sharing_model: " + str(data))

    # check if sharing_model exists
    device_id = data['device_id']
    sharing_model = datamgmt.get_sharing_model(device_id)
    datamgmt.save_device_id(device_id)

    if sharing_model == -1 or sharing_model is None:
        # initializes sharing_model
        sharing_model = datamgmt.init_sharing_model(data)
        if sharing_model is None:
            return None
        else:
            return sharing_model
    else:
        return sharing_model


# Updates shared resources values
def update_sharing_model_by_id(sharing_model_id, data):
    LOG.info("USRMNGT: Sharing-model module: update_sharing_model_by_id: " + sharing_model_id + ", " + str(data))
    # updates sharing_model
    sharing_model = datamgmt.update_sharing_model_by_id(sharing_model_id, data)
    if sharing_model is None:
        return common.gen_response(500, 'Exception', 'data', str(data), 'sharing_model', {})
    elif sharing_model == -1:
        return common.gen_response_ko('Warning: Sharing model not found', 'sharing_model_id', sharing_model_id, 'sharing_model', {})
    else:
        return common.gen_response_ok('Sharing-model updated', 'data', str(data), 'sharing_model', sharing_model)


# delete_sharing_model_by_id: Deletes  shared resources values
def delete_sharing_model_by_id(sharing_model_id):
    LOG.info("USRMNGT: Sharing-model module: delete_sharing_model_by_id: " + sharing_model_id)
    # deletes sharing_model
    res = datamgmt.delete_sharing_model_by_id(sharing_model_id)
    if res is None:
        return common.gen_response(500, 'Exception', 'sharing_model_id', sharing_model_id)
    elif res == -1:
        return common.gen_response_ko('Warning: Sharing-model not found', 'sharing_model_id', sharing_model_id)
    else:
        return common.gen_response_ok('Sharing-model deleted', 'sharing_model_id', sharing_model_id)


