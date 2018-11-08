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
        # CONFIGURATION values
        LOG.info('Reading values from CONFIG FILE...')

        LOG.info('[SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
        LOG.info('[API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
        LOG.info('[CERT_CRT=' + config.dic['CERT_CRT'] + ']')
        LOG.info('[CERT_KEY=' + config.dic['CERT_KEY'] + ']')
        # CIMI
        LOG.info('[CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        LOG.info('[CIMI_COOKIES_PATH=' + config.dic['CIMI_COOKIES_PATH'] + ']')
        LOG.info('[CIMI_USER=' + config.dic['CIMI_USER'] + ']')
        LOG.info('[CIMI_PASSWORD=' + config.dic['CIMI_PASSWORD'] + ']')

        # get CIMI from environment values:
        LOG.info('Reading values from ENVIRONMENT...')
        common.set_value_env('CIMI_COOKIES_PATH')
        common.set_value_env('CIMI_USER')
        common.set_value_env('CIMI_PASSWORD')

        # CIMI URL
        common.set_value_env('CIMI_URL')
        LOG.debug('[CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        if "/api" not in config.dic['CIMI_URL'] and not config.dic['CIMI_URL'].endswith("/api"):
            LOG.debug("Adding '/api' to CIMI_URL ...")
            if config.dic['CIMI_URL'].endswith("/"):
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "api"
            else:
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "/api"
            LOG.debug('[CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        else:
            LOG.debug("CIMI_URL ... " + config.dic['CIMI_URL'])

        # CIMI
        LOG.info('Checking CIMI configuration...')
        LOG.info('[CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        LOG.info('[CIMI_COOKIES_PATH=' + config.dic['CIMI_COOKIES_PATH'] + ']')
        LOG.info('[CIMI_USER=' + config.dic['CIMI_USER'] + ']')
        LOG.info('[CIMI_PASSWORD=' + config.dic['CIMI_PASSWORD'] + ']')
    except:
        LOG.error('Lifecycle-Management: init_config: Exception: Error while initializing application')