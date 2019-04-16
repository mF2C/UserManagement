"""
Initial configuration
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 02 may 2018

@author: Roi Sucasas - ATOS
"""


import config
import common.common as common
from common.logs import LOG


def init():
    try:
        # get CIMI from environment values:
        LOG.info('USRMNGT: Reading values from ENVIRONMENT...')
        common.set_value_env('HOST_IP')
        common.set_value_env('CIMI_COOKIES_PATH')
        common.set_value_env('CIMI_USER')
        common.set_value_env('CIMI_PASSWORD')
        common.set_value_env('UM_WORKING_DIR_VOLUME') # UM_WORKING_DIR_VOLUME from environment values:
        common.set_value_env('CIMI_URL')

        # CIMI URL
        if "/api" not in config.dic['CIMI_URL'] and not config.dic['CIMI_URL'].endswith("/api"):
            LOG.debug("Adding '/api' to CIMI_URL ...")
            if config.dic['CIMI_URL'].endswith("/"):
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "api"
            else:
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "/api"
            LOG.debug('USRMNGT: [CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        else:
            LOG.debug("USRMNGT: CIMI_URL ... " + config.dic['CIMI_URL'])

        # CIMI
        LOG.debug('USRMNGT: Checking configuration...')
        LOG.info('USRMNGT: [CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        LOG.info('USRMNGT: [CIMI_COOKIES_PATH=' + config.dic['CIMI_COOKIES_PATH'] + ']')
        LOG.info('USRMNGT: [CIMI_USER=' + config.dic['CIMI_USER'] + ']')
        LOG.info('USRMNGT: [CIMI_PASSWORD=' + config.dic['CIMI_PASSWORD'] + ']')
        LOG.info('USRMNGT: [UM_WORKING_DIR_VOLUME=' + config.dic['UM_WORKING_DIR_VOLUME'] + ']')
        LOG.info('USRMNGT: [SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
        LOG.info('USRMNGT: [API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
        LOG.info('USRMNGT: [CERT_CRT=' + config.dic['CERT_CRT'] + ']')
        LOG.info('USRMNGT: [CERT_KEY=' + config.dic['CERT_KEY'] + ']')
        LOG.info('USRMNGT: [HOST_IP=' + config.dic['HOST_IP'] + ']')
    except:
        LOG.error('USRMNGT: init_config: Exception: Error while initializing application')