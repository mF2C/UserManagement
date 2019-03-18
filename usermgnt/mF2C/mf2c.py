"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

import config
import requests
from common.logs import LOG


# CALL TO LIFECYCLE MGMT
# send warning to LM - Warnings Handler: it handles warnings coming from User Management Assessment:
#   {
#       "type": "um_warning",
#       "data"
#           {
#               "user_id": "",
#               "device_id": "",
#               "user_profile": {},
#               "sharing_model": {},
#               "result": {'battery_limit_violation': true, 'max_apps_violation': true, 'resource_contributor_violation': true}
#           }
#   }
def send_warning(user_id, device_id, user_profile, sharing_model, result):
    try:
        LOG.info("USRMNGT: Dependencies: send_warning: " + user_id + ", " + device_id)

        if config.dic['ENABLE_ASSESSMENT']:
            LOG.debug('USRMNGT: Dependencies: send_warning: sending warning to LIFECYCLE [' + config.dic['URL_PM_LIFECYCLE'] + '] ...')
            body = {"type": "um_warning",
                    "data": {
                        "user_id": user_id,
                        "device_id": device_id,
                        "user_profile": user_profile,
                        "sharing_model": sharing_model,
                        "result": result}}
            r = requests.post(config.dic['URL_PM_LIFECYCLE'], json=body, verify=config.dic['VERIFY_SSL'])
            if r.status_code == 200:
                LOG.debug('USRMNGT: Dependencies: send_warning: status_code=' + r.status_code + '; response: ' + r.text)
                return True
            else:
                LOG.error('USRMNGT: Dependencies: send_warning: Error: status_code=' + r.status_code)
    except:
        LOG.exception('USRMNGT: Dependencies: send_warning: Exception')
    return False