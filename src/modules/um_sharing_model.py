"""
Sharing Model operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


from src.utils.logs import LOG
from flask import Response, json


fake_sharing_model_info = {
    "max_apps": 1,
    "GPS_allowed": False,
    "max_CPU_usage": 50,
    "max_memory_usage": 200,
    "max_storage_usage": 1000,
    "max_bandwidth_usage": 1000,
    "battery_limit": 25
}


# Get shared resources
def get_sharing_model_values(user_id):
    try:
        LOG.info("User-Management: Sharing model module: Get sharing model: " + user_id)

        # TODO Dataclay or CIMI
        #...

        # TEST
        return {'error': False, 'message': 'Sharing model found', 'user_id': user_id, 'sharing_model': fake_sharing_model_info}
    except:
        LOG.error('User-Management: Sharing model module: get_sharing_model_values: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'user_id': '', 'sharing_model': {}}),
                        status=500, content_type='application/json')


# Initializes shared resources values
def init_sharing_model(data):
    try:
        LOG.info("User-Management: Sharing model module: Initializes sharing model: " + str(data))

        if 'user_id' not in data:
            LOG.error('User-Management: Sharing model module: init_sharing_model: Exception - parameter not found: user_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id', 'profile': {}}),
                            status=406, content_type='application/json')

        # TODO Dataclay or CIMI
        #...

        # TEST
        return {'error': False, 'message': 'Sharing model initialized', 'user_id': data['user_id'],
                'sharing_model': fake_sharing_model_info}
    except:
        LOG.error('User-Management: Sharing model module: init_sharing_model: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'user_id': '', 'sharing_model': {}}),
                        status=500, content_type='application/json')


# Updates shared resources values
def update_sharing_model_values(data):
    try:
        LOG.info("User-Management: Sharing model module: Updates sharing model: " + str(data))

        if 'user_id' not in data:
            LOG.error('User-Management: Sharing model module: init_sharing_model: Exception - parameter not found: user_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id', 'profile': {}}),
                            status=406, content_type='application/json')

        # TODO Dataclay or CIMI
        #...

        # TEST
        return {'error': False, 'message': 'Sharing model updated', 'user_id': data['user_id'],
                'sharing_model': fake_sharing_model_info}
    except:
        LOG.error('User-Management: Sharing model module: update_sharing_model_values: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'user_id': '', 'sharing_model': {}}),
                        status=500, content_type='application/json')


# Deletes  shared resources values
def delete_sharing_model_values(data):
    try:
        LOG.info("Sharing_model: deleteSharingModelValues: " + str(data))

        if 'user_id' not in data:
            LOG.error('User-Management: Sharing model module: init_sharing_model: Exception - parameter not found: user_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id', 'profile': {}}),
                            status=406, content_type='application/json')

        # TODO Dataclay or CIMI
        # ...

        # TEST
        return {'error': False, 'message': 'Sharing model deleted', 'user_id': data['user_id']}
    except:
        LOG.error('User-Management: Sharing model module: delete_sharing_model_values: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'sharing_model': {}}),
                        status=500, content_type='application/json')
