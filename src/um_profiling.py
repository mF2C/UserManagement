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



# Get user profile
def getProfiling(user_id):
    try:
        logs.info("> getProfiling: " + user_id)
        # TODO

        return {'module': 'profiling', 'result': {'email': '', 'service_consumer': '', 'resource_contributor': ''}}
    except:
        logs.error('Error (0)')
        return {'module': 'profiling', 'error': 'Exception', 'user_id': user_id}


# Initializes user's profile
def userRegistration(user_id, data):
    try:
        logs.info("> userRegistration: " + user_id)
        # TODO

        return {'module': 'profiling', 'result': {'email': '', 'service_consumer': '', 'resource_contributor': ''}}
    except:
        logs.error('Error (0)')
        return {'module': 'profiling', 'error': 'Exception', 'user_id': user_id}


# Updates user's profile
def updateProfiling(user_id, data):
    try:
        logs.info("> updateProfiling: " + user_id)
        # TODO

        return {'module': 'profiling', 'result': {'email': '', 'service_consumer': '', 'resource_contributor': ''}}
    except:
        logs.error('Error (0)')
        return {'module': 'profiling', 'error': 'Exception', 'user_id': user_id}


# Deletes user's profile
def deleteProfile(user_id):
    try:
        logs.info("> deleteProfile: " + user_id)
        # TODO

        um_sharing_model.deleteSharingModelValues(user_id)

        return {'module': 'profiling', 'result': 'deleted'}
    except:
        logs.error('Error (0)')
        return {'module': 'profiling', 'error': 'Exception', 'user_id': user_id}
