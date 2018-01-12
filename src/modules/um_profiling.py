"""
Profiling operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import src as um_sharing_model
from src.utils import logs
from flask import Response, json

# dataClay
# from model_mf2c.classes import *
# from dataclay import api
#
#
# api.init()


# Get user profile
def getProfiling(user_id):
    try:
        logs.info("Profiling: getProfiling: " + user_id)
        # TODO

        return {'module': 'profiling', 'result': {'email': '', 'service_consumer': '', 'resource_contributor': ''}}
    except:
        logs.error('Error (0): Profiling: getProfiling: Exception')
        return {'module': 'profiling', 'error': 'Exception', 'user_id': user_id}


# Initializes user's profile
def userRegistration(data):
    try:
        logs.info("Profiling: userRegistration: " + str(data))
        # data: user_id=user_key, email="email", name="name"
        if 'user_id' not in data or 'email' not in data or 'name' not in data:
            logs.error('Profiling: userRegistration: user_id / email / name not found')
            return Response(json.dumps({'module': 'profiling', 'error': 'user_id / email / name not found'}),
                            status=406, content_type='application/json')
        else:
            logs.info('Profiling: userRegistration: Registering user...')
            # Create and store user
            # my_user = User(user_id=data['user_key'], email=data['email'], name=data['name'])
            # logs.info('Profiling: userRegistration:' my_user.getID())
            return {'module': 'profiling', 'result': {'user_id': data['user_id'], 'email': data['email'], 'name': data['name']}}
    except:
        logs.error('Error (0): Profiling: userRegistration: Exception')
        return {'module': 'profiling', 'error': 'Exception', 'data': str(data)}


# Updates user's profile
def updateProfiling(data):
    try:
        logs.info("Profiling: updateProfiling: " + str(data))
        # TODO

        return {'module': 'profiling', 'result': {'email': '', 'service_consumer': '', 'resource_contributor': ''}}
    except:
        logs.error('Error (0): Profiling: updateProfiling: Exception')
        return {'module': 'profiling', 'error': 'Exception', 'data': str(data)}


# Deletes user's profile
def deleteProfile(data):
    try:
        logs.info("Profiling: deleteProfile: " + str(data))
        # TODO

        um_sharing_model.deleteSharingModelValues(data)

        return {'module': 'profiling', 'result': 'deleted'}
    except:
        logs.error('Error (0): Profiling: deleteProfile: Exception')
        return {'module': 'profiling', 'error': 'Exception', 'data': str(data)}
