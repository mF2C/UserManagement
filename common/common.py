"""
Common functions
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import os
import config
from flask import Response, json
from common.logs import LOG


###############################################################################
# RESPONSEs:

# CLASS ResponseCIMI
class ResponseCIMI():
    msj = ""


# Generate response 200
def gen_response_ok(message, key, value, key2=None, value2=None):
    dict = {'error': False, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.debug("USRMNGT: Generate response OK; dict=" + str(dict))
    return dict


# Generate response ERROR
def gen_response(status, message, key, value, key2=None, value2=None):
    dict = {'error': True, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.debug('USRMNGT: Generate response ' + str(status) + "; dict=" + str(dict))
    return Response(json.dumps(dict), status=status, content_type='application/json')

# Generate response 200
def gen_response_ko(message, key, value, key2=None, value2=None):
    dict = {'error': True, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.debug("USRMNGT: Generate response KO; dict=" + str(dict))
    return dict


###############################################################################
# ENV:
# set_value_env: set value (in config dict) from environment
def set_value_env(env_name):
    res = os.getenv(env_name, default='not-defined')
    #LOG.debug('USRMNGT: [' + env_name + '=' + res + ']')
    if res != 'not-defined':
        config.dic[env_name] = res
