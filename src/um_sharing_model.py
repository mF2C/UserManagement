'''
Sharing Model operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python3


#
def getSharingModelValues(user_id):
    try:
        print("> getSharingModelValues: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'SharingModel': 'get'}


#
def initSharingModelValues(user_id, data):
    try:
        print("> initSharingModelValues: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'SharingModel': 'post', 'data': data}


#
def updateSharingModelValues(user_id, data):
    try:
        print("> updateSharingModelValues: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'SharingModel': 'put', 'data': data}


#
def deleteSharingModelValues(user_id):
    try:
        print("> deleteSharingModelValues: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'SharingModel': 'delete'}