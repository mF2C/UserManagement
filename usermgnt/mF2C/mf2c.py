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
#               "result": {'battery_limit_violation': true, 'max_apps_violation': true}
#           }
#   }
def send_warning(user_id, device_id, user_profile, sharing_model, result):
    try:
        LOG.info("User-Management: Dependencies: send_warning: " + user_id + "/" + device_id)

        # TEST INTERACTION WITH OTHER COMPONENTS
        if config.dic['ENABLE_ASSESSMENT_TESTS']:
            LOG.debug('User-Management: Dependencies: send_warning: sending warning to LIFECYCLE [' +
                      config.dic['URL_PM_LIFECYCLE'] + '] ...')
            param = "id_service"
            body = {"type": "um_warning",
                    "data": {
                        "user_id": user_id,
                        "device_id": device_id,
                        "user_profile": user_profile,
                        "sharing_model": sharing_model,
                        "result": result}}
            r = requests.post(config.dic['URL_PM_LIFECYCLE'] + param, json=body, verify=config.dic['VERIFY_SSL'])
            if r.status_code == 200:
                LOG.debug('User-Management: Dependencies: send_warning: status_code=' + r.status_code + '; response: ' + r.text)
                return True
            else:
                LOG.error('User-Management: Dependencies: send_warning: Error: status_code=' + r.status_code)
    except:
        LOG.error('User-Management: Dependencies: get_resources_used_by_service: Exception')
    return False