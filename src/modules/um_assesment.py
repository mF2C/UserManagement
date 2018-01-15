"""
User Management Assesment module operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import src.modules.assessment_process as process
from src.utils import logs
from flask import Response, json


# start process
def __start():
    logs.info("User-Management: Assessment module: start process")
    try:
        p_status = process.start()
        return {'error': False, 'message': 'Assessment process started', 'status': p_status}
    except:
        logs.error('User-Management: Assessment module: start: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception when starting the assessment process',
                                    'status': ''}),
                        status=500, content_type='application/json')


# stop process
def __stop():
    logs.info("User-Management: Assessment module: stop process")
    try:
        p_status = process.stop()
        return {'error': False, 'message': 'Assessment process stopped', 'status': p_status}
    except:
        logs.error('User-Management: Assessment module: stop: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception when stopping the assessment process',
                                    'status': ''}),
                        status=500, content_type='application/json')


# operation
def operation(data):
    logs.info("User-Management: Assessment module: Execute operation: " + str(data))

    if 'operation' not in data:
        logs.error('User-Management: Assessment module: operation: Exception - parameter not found')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: operation', 'status': ''}),
                        status=406, content_type='application/json')

    if data['operation'] == 'start':
        return __start()
    elif data['operation'] == 'stop':
        return __stop()
    else:
        logs.error('User-Management: Assessment module: operation: Operation ' + data['operation'] +
                   ' not defined / implemented')
        return Response(json.dumps({'error': 'operation ' + data['operation'] + ' not defined / implemented'}),
                        status=501, content_type='application/json')


# get process status
def status():
    logs.info("User-Management: Assessment module: get process status")
    try:
        p_status = process.get_status()
        return {'error': False, 'message': 'Assessment process status', 'status': p_status}
    except:
        logs.error('User-Management: Assessment module: status: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception when getting assessment process status',
                                    'status': ''}),
                        status=500, content_type='application/json')
