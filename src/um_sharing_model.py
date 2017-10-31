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
def getSharingModel():
    try:
        print("> getSharingModel: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'SharingModel': 'get'}


#
def initSharingModel(data):
    try:
        print("> setSharingModel: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'SharingModel': 'post', 'data': data}


#
def updateSharingModel(data):
    try:
        print("> updateSharingModel: " + user_id)
        # TODO
    except:
        print('> Unknown error detected.')
    return {'SharingModel': 'put', 'data': data}
