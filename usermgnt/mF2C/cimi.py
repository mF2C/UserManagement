"""
CIMI interface
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import requests
import datetime
import config
from common.logs import LOG


# CIMI initialization
CIMI_HEADER_PROPERTY = "slipstream-authn-info"
CIMI_HEADER_VALUE = "super ADMIN"

# ACL
acl = {"owner":
           {"principal": config.dic['CIMI_USER'], #"ADMIN",
            "type": "ROLE"},
       "rules": [{"principal": config.dic['CIMI_USER'], #"ADMIN",
                  "type": "ROLE",
                  "right": "ALL"},
                 {"principal": "ANON",
                  "type": "ROLE",
                  "right": "ALL"}
                 ]}


# common_new_map_fields: generates a map with time and acl values
def common_new_map_fields():
    now = datetime.datetime.now()
    default_map = {
        "created": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "updated": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "acl": acl
    }
    return default_map


# common_update_map_fields: generates a map with time and acl values
def common_update_map_fields():
    now = datetime.datetime.now()
    default_map = {
        "updated": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "acl": acl
    }
    return default_map


###############################################################################
# COMMON

# TODO get this information from new RESOURCE: AGENT
# get_current_device_info
def get_current_device_info():
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/device",
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)
        LOG.info("USRMNGT: cimi: get_current_device_info: Response: " + str(res.json()))

        if res.status_code == 200 and res.json()['count'] == 0:
            LOG.warning("USRMNGT: cimi: get_current_device_info: 'device' not found")
            return -1
        elif res.status_code == 200:
            return res.json()['devices'][0]

        LOG.warning("USRMNGT: cimi: get_current_device_info: 'device' not found")
        return -1
    except:
        LOG.exception('USRMNGT: cimi: get_current_device_info: Exception')
        return None


# exist_user: check if 'user id' exists
def exist_user(user_id):
    try:
        user_id = user_id.replace('user/', '')
        res = requests.get(config.dic['CIMI_URL'] + "/user/" + user_id,
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)
        LOG.debug("USRMNGT: cimi: exist_user: Response: " + str(res.json()))

        if res.status_code == 200 and not res.json()['id'] is None:
            return True
    except:
        LOG.warning("LIFECYCLE: cimi: exist_user: controlled exception")
    LOG.warning("USRMNGT: cimi: exist_user: 'user' not found / error getting user")
    return False


# exist_device: check if 'device id' exists
def exist_device(device_id):
    try:
        device_id = device_id.replace('device/', '')
        res = requests.get(config.dic['CIMI_URL'] + "/device/" + device_id,
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)
        LOG.debug("USRMNGT: cimi: exist_device: Response: " + str(res.json()))

        if res.status_code == 200 and not res.json()['id'] is None:
            return True
    except:
        LOG.warning("LIFECYCLE: cimi: exist_device: controlled exception")
    LOG.warning("USRMNGT: cimi: exist_device: 'device' not found / error getting device")
    return False


###############################################################################

# get_resource_by_id: get resource by id
def get_resource_by_id(resource_id):
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/" + resource_id,
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)

        if res.status_code == 200:
            return res.json()

        LOG.error("USRMNGT: cimi: get_resource_by_id: Request failed: " + res.status_code)
        LOG.error("USRMNGT: cimi: get_resource_by_id: Response: " + str(res.json()))
        return None
    except:
        LOG.exception('USRMNGT: cimi: get_resource_by_id: Exception')
        return None


# get_user_profile: get profile from user and device
def get_user_profile(user_id, device_id):
    try:
        user_id = user_id.replace('user/', '')
        device_id = device_id.replace('device/', '')

        res = requests.get(config.dic['CIMI_URL'] + "/user-profile?$filter=user_id=\"user/" + user_id + "\" and device_id=\"device/" + device_id + "\"",
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)

        LOG.debug("USRMNGT: cimi: get_user_profile: response: " + str(res))
        LOG.debug("USRMNGT: cimi: get_user_profile: response: " + str(res.json()))

        if res.status_code == 200 and len(res.json()['userProfiles']) > 0:
            return res.json()['userProfiles'][0]
        else:
            LOG.warning("USRMNGT: cimi: get_user_profile: User's profile not found [user_id=" + user_id + ", device_id=" + device_id + "]")
            return -1
    except:
        LOG.exception('USRMNGT: cimi: get_user_profile: Exception')
        return None


# TODO get this information from new RESOURCE: AGENT
# get_user_profile_by_device: get profile from device
def get_user_profile_by_device(device_id):
    try:
        device_id = device_id.replace('device/', '')

        res = requests.get(config.dic['CIMI_URL'] + "/user-profile?$filter=device_id=\"device/" + device_id + "\"",
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)

        LOG.debug("USRMNGT: cimi: get_user_profile_by_device: response: " + str(res))
        LOG.debug("USRMNGT: cimi: get_user_profile_by_device: response: " + str(res.json()))

        if res.status_code == 200 and len(res.json()['userProfiles']) > 0:
            res_user_profile = res.json()['userProfiles'][0]
            res_user_profile['apps_running'] = config.APPS_RUNNING
            return res_user_profile
        else:
            LOG.warning("USRMNGT: cimi: get_user_profile_by_device: User's profile not found [device_id=" + device_id + "]")
            return -1
    except:
        LOG.exception('USRMNGT: cimi: get_user_profile_by_device: Exception')
        return None


# get_sharing_model: get sharing model from user
def get_sharing_model(user_id, device_id):
    try:
        user_id = user_id.replace('user/', '')
        device_id = device_id.replace('device/', '')

        res = requests.get(config.dic['CIMI_URL'] + "/sharing-model?$filter=user_id=\"user/" + user_id + "\" and device_id=\"device/" + device_id + "\"",
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)

        LOG.debug("USRMNGT: cimi: get_sharing_model: response: " + str(res))
        LOG.debug("USRMNGT: cimi: get_sharing_model: response: " + str(res.json()))

        if res.status_code == 200 and len(res.json()['sharingModels']) > 0:
            return res.json()['sharingModels'][0]
        else:
            LOG.warning("USRMNGT: cimi: get_sharing_model: Sharing-model not found [user_id=" + user_id + ", device_id=" + device_id + "]")
            return -1
    except:
        LOG.exception('USRMNGT: cimi: get_sharing_model: Exception')
        return None


# TODO get this information from new RESOURCE: AGENT
# get_sharing_model_by_device: get sharing model from device
def get_sharing_model_by_device(device_id):
    try:
        device_id = device_id.replace('device/', '')

        res = requests.get(config.dic['CIMI_URL'] + "/sharing-model?$filter=device_id=\"device/" + device_id + "\"",
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)

        LOG.debug("USRMNGT: cimi: get_sharing_model_by_device: response: " + str(res))
        LOG.debug("USRMNGT: cimi: get_sharing_model_by_device: response: " + str(res.json()))

        if res.status_code == 200 and len(res.json()['sharingModels']) > 0:
            return res.json()['sharingModels'][0]
        else:
            LOG.warning("USRMNGT: cimi: get_sharing_model_by_device: Sharing-model not found [device_id=" + device_id + "]")
            return -1
    except:
        LOG.exception('USRMNGT: cimi: get_sharing_model_by_device: Exception')
        return None


# FUNCTION: add_resource: add resource to cimi
# RETURNS: resource
def add_resource(resource_name, content):
    try:
        LOG.debug("USRMNGT: cimi: add_resource: Adding new resource to [" + resource_name + "] with content [" + str(content) + "] ... ")

        # complete map and update resource
        content.update(common_new_map_fields())
        #content.pop("user_id", None)

        res = requests.post(config.dic['CIMI_URL'] + '/' + resource_name,
                            headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                            verify=False,
                            json=content)

        LOG.debug("USRMNGT: cimi: add_resource: response: " + str(res))
        LOG.debug("USRMNGT: cimi: add_resource: response: " + str(res.json()))

        if res.status_code == 201:
            return get_resource_by_id(res.json()['resource-id'])

        LOG.error("USRMNGT: cimi: add_resource: Request failed: " + res.status_code)
        LOG.error("USRMNGT: cimi: add_resource: Response: " + str(res.json()))
        return None
    except:
        LOG.exception('USRMNGT: cimi: add_resource: Exception')
        return None


# add_resource: add resource to cimi
def update_resource(resource_id, content):
    try:
        LOG.debug("USRMNGT: cimi: update_resource: Updating resource [" + resource_id + "] with content [" + str(content) + "] ... ")

        # complete map and update resource
        content.update(common_update_map_fields())

        res = requests.put(config.dic['CIMI_URL'] + '/' + resource_id,
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False,
                           json=content)

        LOG.debug("USRMNGT: cimi: update_resource: response: " + str(res))
        LOG.debug("USRMNGT: cimi: update_resource: response: " + str(res.text))

        if res.status_code == 200:
            return get_resource_by_id(resource_id)

        LOG.error("USRMNGT: cimi: update_resource: Request failed: " + res.status_code)
        LOG.error("USRMNGT: cimi: update_resource: Response: " + str(res.json()))
        return None
    except:
        LOG.exception('USRMNGT: cimi: update_resource: Exception')
        return None


# delete_resource: delete resource by id
def delete_resource(resource_id):
    try:
        res = requests.delete(config.dic['CIMI_URL'] + '/' + resource_id,
                              headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                              verify=False)

        LOG.debug("USRMNGT: cimi: delete_resource: response: " + str(res))
        LOG.debug("USRMNGT: cimi: delete_resource: response: " + str(res.json()))

        if res.status_code == 200:
            return res.json()
        return None
    except:
        LOG.exception('USRMNGT: cimi: delete_resource: Exception')
        return None


# TODO!!!
###############################################################################
# DEVICE DYNAMIC
#
#{
#  "device_id":x
#  "updated_on": x
#  "available_RAM_size_in_MB": long,
#  "available_RAM_in_percentage": float,
#  "available_Storage_size_in_MB": long,
#  "available_Storage_in_percentage": float,
#  "available_CPU_percentage": float,
#  "power_remaining_status": string,
#  "remaining_power_info_in_seconds": string,
#  "ethernet_address": string,
#  "wifi_address": string,
#  "throughput_info_ethernet": string,
#  "throughput_info_wifi": string
#  "inclinometer": x,                  The information about the sensors and actuators will be provided
#  "temperature": x,
#  "jammer": x,
#  "location": x,
#  "ambulance": x,
#  "fire_car": x,
#  "traffic_light": x,
#  "street_light": x
# }
###############################################################################
# DEVICE
#
#{
#  "device_id" : string,
#  "created_on": x,
#  "isleader": "False",
#  "os":  string,
#  "arch": string,
#  "cpu_manufacturer": string,
#  "physical_cpu_cores": int,
#  "logical_cpu_cores": int,
#  "cpu_clock_speed": string,
#  "RAM_size_in_MB": long,
#  "Storage_size_in_MB": long,
#  "power_plugged_information": boolean,
#  "networking_standards": string,
#  "ethernet_address": string,
#  "wifi_address": string
# }

# get_power
def get_power(device_id):
    try:
        device_id = device_id.replace('device/', '')
        res = requests.get(config.dic['CIMI_URL'] + "/device-dynamic?$filter=device/href='device/" + device_id + "'",
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)

        if res.status_code == 200 and res.json()['count'] > 0:
            return res.json()['deviceDynamics'][0]
        else:
            LOG.warning("USRMNGT: cimi: 'device-dynamic' not found [device_id=" + device_id + "]")
            return -1
    except:
        LOG.exception('USRMNGT: cimi: get_power: Exception')
        return None


# get_parent
def get_parent(device_id):
    try:
        device_id = device_id.replace('device/', '')
        res = requests.get(config.dic['CIMI_URL'] + "/device-dynamic?$filter=myLeaderID/href='device/" + device_id + "'",
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)

        if res.status_code == 200:
            return res.json()['deviceDynamics'][0]
        else:
            LOG.warning("USRMNGT: cimi: get_parent: 'device-dynamic' not found [device_id=" + device_id + "]")
            return -1
    except:
        LOG.exception('USRMNGT: cimi: get_parent: Exception')
        return None


###############################################################################
# NUM APPS RUNNING

# get_num_apps_running
def get_num_apps_running(device_id):
    try:
        # get IP from device-dynamic / agent


        # get service instances filtering by agent/url

        res = requests.get(config.dic['CIMI_URL'] + "/device-dynamic?$filter=device_id='" + device_id + "'",
                           headers={CIMI_HEADER_PROPERTY: CIMI_HEADER_VALUE},
                           verify=False)

        if res.status_code == 200:
            return res.json()['deviceDynamics'][0]
        else:
            LOG.warning("USRMNGT: cimi: 'device-dynamic' not found [device_id=" + device_id + "]")
            return -1
    except:
        LOG.exception('USRMNGT: cimi: Exception')
        return None