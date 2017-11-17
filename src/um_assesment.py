'''
User Management Assesment module operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python3

def start():
    return {'module': 'assesment-process', 'result': 'started'}

def restart():
    return {'module': 'assesment-process', 'result': 'restarted'}

def stop():
    return {'module': 'assesment-process', 'result': 'stopped'}

def status():
    return {'module': 'assesment-process', 'result': '???'}
