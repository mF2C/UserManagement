"""
Profiling operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import src.modules.um_sharing_model as um_sharing_model
from src.utils import logs
from flask import Response, json


# TODO Dataclay / CIMI initialization
# from model_mf2c.classes import *
# from dataclay import api
#
#
# api.init()
# ...


# Get user profile
def get_profiling(user_id):
    try:
        logs.info("User-Management: Profiling module: Get user profile: " + user_id)

        # TODO Dataclay or CIMI
        # Get user profile:
        #user_profile = User.get_by_alias(user_id)
        #...

        # TEST
        return {'error': False, 'message': 'User found', 'user_id': user_id,
                'profile': {'email': 'TEST@EMAIL.COM', 'service_consumer': True, 'resource_contributor': True}}
    except:
        logs.error('User-Management: Profiling module: get_profiling: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'user_id': '', 'profile': {}}),
                        status=500, content_type='application/json')


# Initializes users profile
#   data: {'user_id':'', 'email':''}
def register_user(data):
    try:
        logs.info("User-Management: Profiling module: Register user: " + str(data))

        if 'user_id' not in data or 'email' not in data:
            logs.error('User-Management: Profiling module: Register user: parameter not found: user_id / email')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id / email'}),
                            status=405, content_type='application/json')
        else:
            # TODO Dataclay or CIMI
            # Create and store user:
            #my_user = User(user_id=data['user_key'], email=data['email'], name=data['name'])
            #my_user.make_persistent(alias=data['user_key'])
            #...

            # TEST
            return {'error': False, 'message': 'User registered', 'user_id': data['user_id'],
                    'profile': {'email': data['email'], 'service_consumer': True, 'resource_contributor': True}}
    except:
        logs.error('User-Management: Profiling module: register_user: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'profile': {}}),
                        status=500, content_type='application/json')


# Updates users profile
#   data: {'user_id':'', 'email':'', 'service_consumer': '', 'resource_contributor': ''}
def update_profile(data):
    try:
        logs.info("User-Management: Profiling module: Updates user's profile: " + str(data))

        if 'user_id' not in data:
            logs.error('User-Management: Profiling module: Update profile: parameter not found: user_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id'}),
                            status=405, content_type='application/json')
        else:
            # TODO Dataclay or CIMI
            #...

            # TEST
            return {'error': False, 'message': 'Profile updated', 'user_id': data['user_id'],
                    'profile': {'email': 'TEST@EMAIL.COM', 'service_consumer': True, 'resource_contributor': True}}
    except:
        logs.error('User-Management: Profiling module: update_profile: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'profile': {}}),
                        status=500, content_type='application/json')


# Deletes users profile
#   data: {'user_id':''}
def delete_profile(data):
    try:
        logs.info("User-Management: Profiling module: Deletes users profile: " + str(data))

        if 'user_id' not in data:
            logs.error('User-Management: Assessment module: operation: Exception - parameter not found: user_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id', 'profile': {}}),
                            status=406, content_type='application/json')

        # TODO Dataclay or CIMI
        #...

        # TEST
        um_sharing_model.delete_sharing_model_values(data)

        return {'error': False, 'message': 'Profile deleted', 'user_id': data['user_id']}
    except:
        logs.error('User-Management: Profiling module: delete_profile: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'profile': {}}),
                        status=500, content_type='application/json')
