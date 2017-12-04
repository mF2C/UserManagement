'''
Sharing Model operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python

import logs


# Get shared resources
def getSharingModelValues(user_id):
    try:
        logs.info("Sharing_model: getSharingModelValues: " + user_id)
        # TODO

        return {'module': 'sharing_model', 'result': ''}
    except:
        logs.error('Error (0): Sharing_model: getSharingModelValues: Exception')
        return {'module': 'sharing_model', 'error': 'Exception', 'user_id': user_id}


# Initializes shared resources values
def initSharingModelValues(user_id, data):
    try:
        logs.info("Sharing_model: initSharingModelValues: " + user_id)
        # TODO

        return {'module': 'sharing_model', 'result': ''}
    except:
        logs.error('Error (0): Sharing_model: initSharingModelValues: Exception')
        return {'module': 'sharing_model', 'error': 'Exception', 'user_id': user_id}


# Updates shared resources values
def updateSharingModelValues(user_id, data):
    try:
        logs.info("Sharing_model: updateSharingModelValues: " + user_id)
        # TODO

        return {'module': 'sharing_model', 'result': ''}
    except:
        logs.error('Error (0): Sharing_model: updateSharingModelValues: Exception')
        return {'module': 'sharing_model', 'error': 'Exception', 'user_id': user_id}


# Deletes  shared resources values
def deleteSharingModelValues(user_id):
    try:
        logs.info("Sharing_model: deleteSharingModelValues: " + user_id)
        # TODO

        return {'module': 'sharing_model', 'result': ''}
    except:
        logs.error('Error (0): Sharing_model: deleteSharingModelValues: Exception')
        return {'module': 'sharing_model', 'error': 'Exception', 'user_id': user_id}
