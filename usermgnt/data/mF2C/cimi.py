"""
CIMI interface
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

import requests, datetime
import config
from usermgnt.common.logs import LOG


'''
CIMI RESOURCES USED / MANAGED:

* USER-PROFILE
{
    "device_id": "device/11111111d",
  	"service_consumer": boolean,
	"resource_contributor": boolean
}
* SHARING-MODEL
{
    "device_id": "device/11111111d",
 	"gps_allowed": boolean,
	"max_cpu_usage": integer,
	"max_memory_usage": integer,
	"max_storage_usage": integer,
	"max_bandwidth_usage": integer,
	"max_apps": 1,
 	"battery_limit": integer
}
* AGENT
{
    "authenticated" : true,
    "leader_id" : "device_2",
    "leaderAddress" : "192.168.252.42",
    "connected" : true,
    "device_ip" : "192.168.252.41",
    "id" : "agent/9a2f5cf5-b885-4c8f-8783-66451f59928d",
    "isLeader" : false,
    "resourceURI" : "http://schemas.dmtf.org/cimi/2/Agent",
    "childrenIPs" : [ "192.168.252.43" ],
    "device_id" : "device_1"
}
* DEVICE
{
    "cpuinfo" : "<rawCPUinfo>",
    "memory" : 7874.211,
    "logicalCores" : 8,
    "cpuManufacturer" : "Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz",
    "arch" : "x86_64",
    "physicalCores" : 4,
    "networkingStandards" : "[eth0, lo]",
    "id" : "device/4cdf8b30-3c6b-4663-be0a-8e911ba12b93",
    "isLeader" : false,
    "deviceID" : "agent_1",
    "storage" : 234549.5,
    "hwloc" : "<xmlString>",
    "resourceURI" : "http://schemas.dmtf.org/cimi/2/Device",
    "os" : "Linux-4.13.0-38-generic-x86_64-with-debian-8.10",
    "cpuClockSpeed" : "1.8000 GHz",
    "agentType" : "<agentType>"
} 
* DEVICE_DYNAMIC
{
    "powerPlugged" : true,
    "wifiAddress" : "Empty",
    "ramFree" : 4795.1523,
    "ethernetAddress" : "192.168.252.41",
    "storageFreePercent" : 93.6,
    "wifiThroughputInfo" : [ "a" ],
    "id" : "device-dynamic/89bafd65-e2a1-4e18-9f05-7e939246719a",
    "ethernetThroughputInfo" : [ "E", "m", "p", "t", "y" ],
    "powerRemainingStatus" : "60.75885328836425",
    "cpuFreePercent" : 93.5,
    "actuatorInfo" : "<actuatorInfo>",
    "resourceURI" : "http://schemas.dmtf.org/cimi/2/DeviceDynamic",
    "device" : {
      "href" : "device/4cdf8b30-3c6b-4663-be0a-8e911ba12b93"
    },
    "ramFreePercent" : 60.9,
    "powerRemainingStatusSeconds" : "3817",
    "storageFree" : 208409.25
}
'''


# CIMI initialization
CIMI_HEADER = {'slipstream-authn-info': 'super ADMIN'}


# Generates ACL for a specific user
def getACLforUser():
    ACL_USER = {"owner":
                   {"principal": config.dic['DEVICE_USER'],
                    "type": "ROLE"},
                "rules": [{"principal": "ADMIN",
                          "type": "ROLE",
                          "right": "ALL"},
                         {"principal": "ANON",
                          "type": "ROLE",
                          "right": "ALL"}
                         ]}
    return ACL_USER

# common_new_map_fields: generates a map with time and acl values
def common_new_map_fields():
    now = datetime.datetime.now()
    default_map = {
        "created": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "updated": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "acl": getACLforUser()
    }
    return default_map


# common_update_map_fields: generates a map with time and acl values
def common_update_map_fields():
    now = datetime.datetime.now()
    default_map = {
        "updated": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "acl": getACLforUser()
    }
    return default_map


###############################################################################
# COMMON

# FUNCTION: get_current_device_info: get 'agent' resource content
# {
#     "authenticated" : true,
#     "leader_id" : "device_2",
#     "leaderAddress" : "192.168.252.42",
#     "connected" : true,
#     "device_ip" : "192.168.252.41",
#     "id" : "agent/9a2f5cf5-b885-4c8f-8783-66451f59928d",
#     "isLeader" : false,
#     "resourceURI" : "http://schemas.dmtf.org/cimi/2/Agent",
#     "childrenIPs" : [ "192.168.252.43" ],
#     "device_id" : "device_1"
# }
def get_agent_info():
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/agent",
                           headers=CIMI_HEADER,
                           verify=False)
        LOG.debug("[usermgnt.data.mF2C.cimi] [get_agent_info] response: " + str(res) + ", " + str(res.json()))

        if res.status_code == 200 and res.json()['count'] == 0:
            LOG.warning("[usermgnt.data.mF2C.cimi] [get_agent_info] 'agent' not found")
            return -1
        elif res.status_code == 200:
            return res.json()['agents'][0]

        LOG.warning("[usermgnt.data.mF2C.cimi] [get_agent_info] 'agent' not found; Returning -1 ...")
        return -1
    except:
        LOG.error("[usermgnt.data.mF2C.cimi] [get_agent_info] Exception; Returning None ...")
        return None


# FUNCTION: get_id_from_device: get 'id' from device by 'deviceID'
def get_id_from_device(deviceID):
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/device?$filter=deviceID=\"" + deviceID + "\"",
                           headers=CIMI_HEADER,
                           verify=False)
        LOG.debug("[usermgnt.data.mF2C.cimi] [get_id_from_device] response: " + str(res)) # + ", " + str(res.json()))

        if res.status_code == 200 and len(res.json()['devices']) > 0:
            return res.json()['devices'][0]['id']
        else:
            LOG.warning("[usermgnt.data.mF2C.cimi] [get_id_from_device] No device found; Returning -1 ...")
            return -1
    except:
        LOG.exception("[usermgnt.data.mF2C.cimi] [get_id_from_device] Exception; Returning None ...")
        return None


# FUNCTION: get_resource_by_id: get resource by id
def get_resource_by_id(resource_id):
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/" + resource_id,
                           headers=CIMI_HEADER,
                           verify=False)
        LOG.debug("[usermgnt.data.mF2C.cimi] [get_resource_by_id] response: " + str(res) + ", " + str(res.json()))

        if res.status_code == 200:
            return res.json()

        LOG.error("[usermgnt.data.mF2C.cimi] [get_resource_by_id] Request failed: " + res.status_code + "; Returning None ...")
    except:
        LOG.exception("[usermgnt.data.mF2C.cimi] [get_resource_by_id] Exception; Returning None ...")
    return None


# FUNCTION: add_resource: add resource to cimi
# RETURNS: resource
def add_resource(resource_name, content):
    try:
        LOG.debug("[usermgnt.data.mF2C.cimi] [add_resource] Adding new resource to [" + resource_name + "] with content [" + str(content) + "] ... ")
        # complete map and update resource
        content.update(common_new_map_fields())
        #content.pop("user_id", None)
        res = requests.post(config.dic['CIMI_URL'] + '/' + resource_name,
                            headers=CIMI_HEADER,
                            verify=False,
                            json=content)
        LOG.debug("[usermgnt.data.mF2C.cimi] [add_resource] response: " + str(res) + ", " + str(res.json()))

        if res.status_code == 201:
            return get_resource_by_id(res.json()['resource-id'])

        LOG.error("[usermgnt.data.mF2C.cimi] [add_resource] Request failed: " + str(res.status_code) + "; Returning None ...")
    except:
        LOG.exception("[usermgnt.data.mF2C.cimi] [add_resource] Exception; Returning None ...")
    return None


# FUNCTION: add_resource: add resource to cimi
def update_resource(resource_id, content):
    try:
        LOG.debug("[usermgnt.data.mF2C.cimi] [update_resource] (1) Updating resource [" + resource_id + "] with content [" + str(content) + "] ... ")
        # complete map and update resource
        content.update(common_update_map_fields())
        LOG.debug("[usermgnt.data.mF2C.cimi] [update_resource] (2) Updating resource [" + resource_id + "] with content [" + str(content) + "] ... ")
        res = requests.put(config.dic['CIMI_URL'] + '/' + resource_id,
                           headers=CIMI_HEADER,
                           verify=False,
                           json=content)
        LOG.debug("[usermgnt.data.mF2C.cimi] [update_resource] response: " + str(res) + ", " + str(res.json()))

        if res.status_code == 200:
            return get_resource_by_id(resource_id)

        LOG.error("[usermgnt.data.mF2C.cimi] [update_resource] Request failed: " + str(res.status_code) + "; Returning None ...")
    except:
        LOG.exception("[usermgnt.data.mF2C.cimi] [update_resource] Exception; Returning None ...")
    return None


# FUNCTION: delete_resource: delete resource by id
def delete_resource(resource_id):
    try:
        res = requests.delete(config.dic['CIMI_URL'] + '/' + resource_id,
                              headers=CIMI_HEADER,
                              verify=False)
        LOG.debug("[usermgnt.data.mF2C.cimi] [delete_resource] response: " + str(res) + ", " + str(res.json()))

        if res.status_code == 200:
            return res.json()
    except:
        LOG.exception("[usermgnt.data.mF2C.cimi] [delete_resource] Exception; Returning None ...")
    return None


# FUNCTION: delete_resource_by_owner: delete resource by owner
def delete_resource_by_owner(resource, resources, owner_id):
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/" + resource + "?$filter=acl/owner/principal='" + owner_id + "'",
                           headers=CIMI_HEADER,
                           verify=False)
        LOG.debug("[usermgnt.data.mF2C.cimi] [delete_resource_by_owner] response: " + str(res)) # + ", " + str(res.json()))

        if res.status_code == 200 and len(res.json()[resources]) > 0:
            for r in res.json()[resources]:
                res2 = requests.delete(config.dic['CIMI_URL'] + "/" + r["id"],
                                       headers=CIMI_HEADER,
                                       verify=False)
                LOG.debug("[usermgnt.data.mF2C.cimi] [delete_resource_by_owner] response: " + str(res2) + ", " + str(res2.json()))

                if res2.status_code == 200:
                    LOG.debug("[usermgnt.data.mF2C.cimi] [delete_resource_by_owner] Resource " + r["id"] + " deleted!")
        else:
            LOG.warning("[usermgnt.data.mF2C.cimi] [delete_resource_by_owner] No " + resources + " found.")
    except:
        LOG.exception("[usermgnt.data.mF2C.cimi] [delete_resource_by_owner] Exception.")


###############################################################################
# DEVICE DYNAMIC
# DEVICE

# get_user_profile: get profile from user and device
def get_user_profile(device_id):
    try:
        device_id = device_id.replace('device/', '')

        res = requests.get(config.dic['CIMI_URL'] + "/user-profile?$filter=device_id=\"device/" + device_id + "\"",
                           headers=CIMI_HEADER,
                           verify=False)
        LOG.debug("[usermgnt.data.mF2C.cimi] [get_user_profile] response: " + str(res) + ", " + str(res.json()))

        if res.status_code == 200 and len(res.json()['userProfiles']) > 0:
            return res.json()['userProfiles'][0]
        else:
            LOG.warning("[usermgnt.data.mF2C.cimi] [get_user_profile] User's profile not found [device_id=" + device_id + "]; Returning -1 ...")
            return -1
    except:
        LOG.exception("[usermgnt.data.mF2C.cimi] [get_user_profile] Exception; Returning None ...")
        return None


# get_sharing_model: get sharing model from user
def get_sharing_model(device_id):
    try:
        device_id = device_id.replace('device/', '')
        res = requests.get(config.dic['CIMI_URL'] + "/sharing-model?$filter=device_id=\"device/" + device_id + "\"",
                           headers=CIMI_HEADER,
                           verify=False)
        LOG.debug("[usermgnt.data.mF2C.cimi] [get_sharing_model] response: " + str(res) + ", " + str(res.json()))

        if res.status_code == 200 and len(res.json()['sharingModels']) > 0:
            return res.json()['sharingModels'][0]
        else:
            LOG.warning("[usermgnt.data.mF2C.cimi] [get_sharing_model] Sharing-model not found [device_id=" + device_id + "]; Returning -1 ...")
            return -1
    except:
        LOG.exception("[usermgnt.data.mF2C.cimi] [get_sharing_model] Exception; Returning None ...")
        return None


###############################################################################
# DEVICE DYNAMIC
# DEVICE

# get_power
def get_power(device_id):
    try:
        device_id = device_id.replace('device/', '')
        res = requests.get(config.dic['CIMI_URL'] + "/device-dynamic?$filter=device/href='device/" + device_id + "'",
                           headers=CIMI_HEADER,
                           verify=False)
        LOG.debug("[usermgnt.data.mF2C.cimi] [get_power] response: " + str(res) + ", " + str(res.json()))

        if res.status_code == 200 and res.json()['count'] > 0:
            power_value = res.json()['deviceDynamics'][0]['powerRemainingStatus']
            if str(power_value).lower() == "unlimited":
                return 100
            else:
                return int(power_value)
        else:
            LOG.warning("[usermgnt.data.mF2C.cimi] [get_power] 'device-dynamic' not found [device_id=" + device_id + "]; Returning -1 ...")
            return -1
    except:
        LOG.exception("[usermgnt.data.mF2C.cimi] [get_power] Exception; Returning None ...")
        return None
