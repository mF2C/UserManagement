"""
Sharing Model operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import usermgnt.mF2C.data as datamgmt
import usermgnt.utils.common as common
from usermgnt.utils.logs import LOG


# Sharing model content:
# {
#       "user_id": "user/1230958abdef",
# 	    "max_apps": integer,
# 	    "gps_allowed": boolean,
# 	    "max_cpu_usage": integer,
# 	    "max_memory_usage": integer,
# 	    "max_storage_usage": integer,
# 	    "max_bandwidth_usage": integer,
# 	    "battery_limit": integer
# }


# Get shared resources
def get_sharing_model(user_id):
    LOG.info("User-Management: Sharing model module: get_sharing_model_values: " + str(user_id))

    # get sharing_model
    sharing_model = datamgmt.get_sharing_model(user_id)
    if sharing_model is None:
        return common.gen_response(500, 'Exception', 'user_id', user_id, 'sharing_model', {})
    elif sharing_model == -1:
        return common.gen_response_ko('Warning: Sharing model not found', 'user_id', user_id, 'profile', {})
    else:
        return common.gen_response_ok('Sharing model found', 'user_id', user_id, 'sharing_model', sharing_model)


# Initializes shared resources values
def init_sharing_model(data):
    LOG.info("User-Management: Sharing model module: init_sharing_model: " + str(data))
    if 'user_id' not in data:
        LOG.warning('User-Management: Sharing model module: init_sharing_model: parameter not found: user_id')
        return common.gen_response(406, 'parameter not found: user_id', 'data', str(data))

    # check if sharing_model exists
    sharing_model = datamgmt.get_sharing_model(data['user_id'])
    if sharing_model == -1 or sharing_model is None:
        # initializes sharing_model
        sharing_model = datamgmt.init_sharing_model(data)
        if sharing_model is None:
            return common.gen_response(500, 'Exception', 'data', str(data), 'sharing_model', {})
        else:
            return common.gen_response_ok('Sharing model initialized', 'data', str(data), 'sharing_model', sharing_model.json)
    else:
        return common.gen_response_ko('Warning: Sharing model already exists', 'user_id', data['user_id'], 'sharing_model', sharing_model)


# Updates shared resources values
def update_sharing_model(data):
    LOG.info("User-Management: Sharing model module: update_sharing_model_values: " + str(data))
    if 'user_id' not in data:
        LOG.warning('User-Management: Sharing model module: update_sharing_model_values: parameter not found: user_id')
        return common.gen_response(406, 'parameter not found: user_id', 'data', str(data))

    # updates sharing_model
    sharing_model = datamgmt.update_sharing_model(data)
    if sharing_model is None:
        return common.gen_response(500, 'Exception', 'data', str(data), 'sharing_model', {})
    elif sharing_model == -1:
        return common.gen_response_ko('Warning: Sharing model not found', 'user_id', data['user_id'], 'profile', {})
    else:
        return common.gen_response_ok('Sharing model updated', 'data', str(data), 'sharing_model', sharing_model.json)


# Deletes  shared resources values
def delete_sharing_model_values(data):
    LOG.info("User-Management: Sharing model module: delete_sharing_model_values: " + str(data))
    if 'user_id' not in data:
        LOG.warning('User-Management: Sharing model module: delete_sharing_model_values: parameter not found: user_id')
        return common.gen_response(406, 'parameter not found: user_id', 'data', str(data))

    # deletes sharing_model
    if datamgmt.delete_sharing_model(data['user_id']) is None:
        return common.gen_response(500, 'Exception', 'user_id', data['user_id'])
    else:
        return common.gen_response_ok('Sharing model deleted', 'user_id', data['user_id'])


