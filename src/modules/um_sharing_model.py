"""
Sharing Model operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import src.modules.data as datamgmt
import src.utils.common as common
from src.utils.logs import LOG


# Get shared resources
def get_sharing_model_values(user_id):
    LOG.info("User-Management: Sharing model module: get_sharing_model_values: " + str(user_id))
    # get sharing_model
    sharing_model = datamgmt.get_sharing_model_values(user_id)
    if sharing_model is None:
        return common.gen_response(500, 'Exception', 'user_id', user_id, 'sharing_model', {})
    else:
        return common.gen_response_ok('Sharing model found', 'user_id', user_id, 'sharing_model', sharing_model)


# Initializes shared resources values
def init_sharing_model(data):
    LOG.info("User-Management: Sharing model module: init_sharing_model: " + str(data))
    if 'user_id' not in data:
        LOG.warning('User-Management: Sharing model module: init_sharing_model: parameter not found: user_id')
        return common.gen_response(406, 'parameter not found: user_id', 'data', str(data))
    # initializes sharing_model
    sharing_model = datamgmt.init_sharing_model(data)
    if sharing_model is None:
        return common.gen_response(500, 'Exception', 'data', str(data), 'sharing_model', {})
    else:
        return common.gen_response_ok('Sharing model initialized', 'data', str(data), 'sharing_model', sharing_model)


# Updates shared resources values
def update_sharing_model_values(data):
    LOG.info("User-Management: Sharing model module: update_sharing_model_values: " + str(data))
    if 'user_id' not in data:
        LOG.warning('User-Management: Sharing model module: update_sharing_model_values: parameter not found: user_id')
        return common.gen_response(406, 'parameter not found: user_id', 'data', str(data))
    # updates sharing_model
    sharing_model = datamgmt.update_sharing_model_values(data)
    if sharing_model is None:
        return common.gen_response(500, 'Exception', 'data', str(data), 'sharing_model', {})
    else:
        return common.gen_response_ok('Sharing model updated', 'data', str(data), 'sharing_model', sharing_model)


# Deletes  shared resources values
def delete_sharing_model_values(data):
    LOG.info("User-Management: Sharing model module: delete_sharing_model_values: " + str(data))
    if 'user_id' not in data:
        LOG.warning('User-Management: Sharing model module: delete_sharing_model_values: parameter not found: user_id')
        return common.gen_response(406, 'parameter not found: user_id', 'data', str(data))
    # deletes sharing_model
    if datamgmt.delete_sharing_model_values(data['user_id']):
        return common.gen_response_ok('Sharing model deleted', 'user_id', data['user_id'])
    else:
        return common.gen_response(500, 'Exception', 'user_id', data['user_id'])

