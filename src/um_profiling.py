'''
Profiling operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python3

# Get user profile
def getProfiling(user_id):
    try:
        print("> getProfiling: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'Profiling': 'get', 'user_id': user_id}


# Initializes user
def userRegistration(user_id, data):
    try:
        print("> userRegistration: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'Profiling': 'post', 'user_id': user_id, 'data': data}


# Updates profile
def updateProfiling(user_id, data):
    try:
        print("> updateProfiling: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'Profiling': 'put', 'user_id': user_id, 'data': data}


# Deletes user
def deleteProfile(user_id, data):
    try:
        print("> deleteProfile: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'Profiling': 'delete', 'user_id': user_id, 'data': data}
