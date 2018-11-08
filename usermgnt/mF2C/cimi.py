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
import sys, traceback
import config
from common.logs import LOG


# CIMI initialization
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

# get_resource_by_id: get resource by id
def get_resource_by_id(resource_id):
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/" + resource_id,
                           headers={'slipstream-authn-info': 'super ADMIN'},
                           verify=False)

        if res.status_code == 200:
            return res.json()

        LOG.error("Request failed: " + res.status_code)
        LOG.error("Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# delete_resource: delete resource by id
def delete_resource(resource_id):
    try:
        res = requests.delete(config.dic['CIMI_URL'] + '/' + resource_id,
                              headers={'slipstream-authn-info': 'super ADMIN'},
                              verify=False)

        if res.status_code == 200:
            return res.json()
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_user_profile: get profile from user
# curl -XGET cimi/api/sharing-model?$filter=acl/owner/principal="user"
def get_user_profile(user_id):
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/user-profile?$filter=acl/owner/principal='" + user_id + "'",
                           headers={'slipstream-authn-info': 'super ADMIN'},
                           verify=False)

        if res.status_code == 200:
            return res.json()['userProfiles'][0]
        else:
            LOG.warning("User's profile not found [user_id=" + user_id + "]")
            return -1
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_user_sharing_model: get sharing model from user
# curl -XGET cimi/api/sharing-model?$filter=acl/owner/principal="user"
def get_user_sharing_model(user_id):
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/sharing-model?$filter=acl/owner/principal='" + user_id + "'",
                           headers={'slipstream-authn-info': 'super ADMIN'},
                           verify=False)

        if res.status_code == 200 and res.json()['count'] > 0:
            return res.json()['sharingModels'][0]
        else:
            LOG.warning("User's profile not found [user_id=" + user_id + "]")
            return -1
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# FUNCTION: add_resource: add resource to cimi
# RETURNS: resource
def add_resource(resource_name, content):
    try:
        LOG.debug("Adding new resource to [" + resource_name + "] ... ")

        # complete map and update resource
        content.update(common_new_map_fields())
        content.pop("user_id", None)

        res = requests.post(config.dic['CIMI_URL'] + '/' + resource_name,
                            headers={'slipstream-authn-info': 'super ADMIN'},
                            verify=False,
                            json=content)

        if res.status_code == 201:
            return get_resource_by_id(res.json()['resource-id'])

        LOG.error("Request failed: " + res.status_code)
        LOG.error("Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# add_resource: add resource to cimi
def update_resource(resource_id, content):
    try:
        LOG.debug("Updating resource [" + resource_id + "] ... ")

        # complete map and update resource
        content.update(common_update_map_fields())
        content.pop("user_id", None)

        res = requests.put(config.dic['CIMI_URL'] + '/' + resource_id,
                           headers={'slipstream-authn-info': 'super ADMIN'},
                           verify=False,
                           json=content)

        if res.status_code == 200:
            return get_resource_by_id(resource_id)

        LOG.error("Request failed: " + res.status_code)
        LOG.error("Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None
