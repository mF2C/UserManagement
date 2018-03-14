"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

from usermgnt import config
import requests
from usermgnt.utils.logs import LOG
from slipstream.api import Api


# TODO
# CALL TO ?????
# get allowed services ==> ??
def get_allowed_services():
    try:
        LOG.info("User-Management: Dependencies: get_allowed_services")

        allowed_services = ['serv1', 'serv2', 'serv3']
        return allowed_services
    except:
        LOG.error('User-Management: Dependencies: get_allowed_services: Exception')
    return []


# CALL TO LANDSCAPER
# get resources used by apps ==> landscaper.GetSubgraph(serviceID)
def get_resources_used_by_service(serviceID):
    try:
        LOG.info("User-Management: Dependencies: get_resources_used_by_service: " + str(serviceID))

        r = requests.get(config.dic['URL_PM_LANDSCAPER'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            LOG.debug('User-Management: Dependencies: status_code=' + r.status_code + '; response: ' + r.text)
        else:
            LOG.error('User-Management: Dependencies: Error: status_code=' + r.status_code)

        return ""
    except:
        LOG.error('User-Management: Dependencies: get_resources_used_by_service: Exception')
    return ""


# CALL TO LIFECYCLE MGMT
# send warning to LM - Warnings Handler: it handles warnings coming from User Management Assessment:
#   {
#       "type": "um_warning",
#       "data"
#           {
#               "user_id": "",
#               "device_id": "",
#               "service_id": "",
#               "warning_id": "",
#               "warning_txt": ""
#           }
#   }
def send_warning(user_id, device_id, list_resources_used, profile, shared_model):
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
                        "service_id": "XXXXXXXXXXX",
                        "warning_id": "XXXXXXXXXXX",
                        "warning_txt": "XXXXXXXXXXX"}}
            r = requests.post(config.dic['URL_PM_LIFECYCLE'] + param, json=body, verify=config.dic['VERIFY_SSL'])
            if r.status_code == 200:
                LOG.debug('User-Management: Dependencies: send_warning: status_code=' + r.status_code + '; response: ' + r.text)
                return True
            else:
                LOG.error('User-Management: Dependencies: send_warning: Error: status_code=' + r.status_code)
    except:
        LOG.error('User-Management: Dependencies: get_resources_used_by_service: Exception')
    return False