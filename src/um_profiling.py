'''
Profiling operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python

import src.um_sharing_model as um_sharing_model
import logs
# dataClay
from model_mf2c.classes import *
from dataclay import api


api.init()


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
def userRegistration(user_id, data):
    try:
        logs.info("Profiling: userRegistration: " + user_id)
        # TODO

        logs.info('#######################')
        # Create and store user. This would be done in the cloud, but I do it here for testing
        user_key = "id-user"
        my_user = User(user_id=user_key, email="email", name="name")
        logs.info(my_user.getID())
        logs.info('#######################')

        return {'module': 'profiling', 'result': {'email': '', 'service_consumer': '', 'resource_contributor': ''}}
    except:
        logs.error('Error (0): Profiling: userRegistration: Exception')
        return {'module': 'profiling', 'error': 'Exception', 'user_id': user_id}


# Updates user's profile
def updateProfiling(user_id, data):
    try:
        logs.info("Profiling: updateProfiling: " + user_id)
        # TODO

        return {'module': 'profiling', 'result': {'email': '', 'service_consumer': '', 'resource_contributor': ''}}
    except:
        logs.error('Error (0): Profiling: updateProfiling: Exception')
        return {'module': 'profiling', 'error': 'Exception', 'user_id': user_id}


# Deletes user's profile
def deleteProfile(user_id):
    try:
        logs.info("Profiling: deleteProfile: " + user_id)
        # TODO

        um_sharing_model.deleteSharingModelValues(user_id)

        return {'module': 'profiling', 'result': 'deleted'}
    except:
        logs.error('Error (0): Profiling: deleteProfile: Exception')
        return {'module': 'profiling', 'error': 'Exception', 'user_id': user_id}
