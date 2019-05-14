"""
User Management Assesment module operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

from usermgnt.modules import assessment_process as process
from usermgnt.common.logs import LOG
from usermgnt.common import common as common


# start process
def __start():
    LOG.info("[usermgnt.modules.um_assessment] [__start] start process")
    try:
        p_status = process.start()
        return common.gen_response_ok('Assessment process started', 'status', p_status)
    except:
        LOG.exception('[usermgnt.modules.um_assessment] [__start] Exception')
        return common.gen_response(500, 'Exception when starting the assessment process', 'status', '')


# stop process
def __stop():
    LOG.info("[usermgnt.modules.um_assessment] [__stop] stop process")
    try:
        p_status = process.stop()
        return common.gen_response_ok('Assessment process stopped', 'status', p_status)
    except:
        LOG.exception('[usermgnt.modules.um_assessment] [__stop] Exception')
        return common.gen_response(500, 'Exception when stopping the assessment process', 'status', '')


# operation
def operation(data):
    LOG.info("[usermgnt.modules.um_assessment] [operation] Execute operation: " + str(data))

    if 'operation' not in data:
        LOG.error('[usermgnt.modules.um_assessment] [operation] Exception - parameter not found')
        return common.gen_response(406, 'parameter not found: operation', 'data', str(data))

    if data['operation'] == 'start':
        return __start()
    elif data['operation'] == 'stop':
        return __stop()
    else:
        LOG.error('[usermgnt.modules.um_assessment] [operation] Operation ' + data['operation'] + ' not defined / implemented')
        return common.gen_response(500, 'operation not defined / implemented', 'operation', data['operation'])


# get process status
def status():
    LOG.info("[usermgnt.modules.um_assessment] [status] get process status")
    try:
        p_status = process.get_status()
        return common.gen_response_ok('Assessment process status', 'status', p_status)
    except:
        LOG.exception('[usermgnt.modules.um_assessment] [status] Exception')
        return common.gen_response(500, 'Exception getting the assessment process status', 'status', '')
