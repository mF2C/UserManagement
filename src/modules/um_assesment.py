"""
User Management Assesment module operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import src.modules.assessment_process as process


# start process
def start():
    return {'module': 'assesment-process', 'operation': 'start', 'result': process.start()}


# stop process
def stop():
    return {'module': 'assesment-process', 'operation': 'stop', 'result': process.stop()}


# get process status
def status():
    return {'module': 'assesment-process', 'operation': 'get-status', 'result': process.getStatus()}
