"""
CIMI interface
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import sys, traceback
import requests
from usermgnt import config
from usermgnt.utils.logs import LOG
from slipstream.api import Api


# CIMI initialization
try:
    # API
    LOG.info('Connecting UM to ' + config.dic['CIMI_URL'] + " ...")

    api = Api(config.dic['CIMI_URL'],
              insecure=True,
              cookie_file=config.dic['CIMI_COOKIES_PATH'],
              login_creds={'username': config.dic['CIMI_USER'],
                           'password': config.dic['CIMI_PASSWORD']})

    # Login with username & password
    api.login({"href": "session-template/internal",
               "username": config.dic['CIMI_USER'],
               "password": config.dic['CIMI_PASSWORD']})

    # test api
    resp = api.cimi_search('users')
    LOG.info('UM connected to ' + config.dic['CIMI_URL'] + ": total users: " + str(resp.count))

    # ACL
    acl = {"owner":
               {"principal": "ADMIN",
                "type": "ROLE"},
           "rules": [{"principal": "ADMIN",
                      "type": "ROLE",
                      "right": "ALL"},
                     {"principal": "ANON",
                      "type": "ROLE",
                      "right": "ALL"}
                     ]}
except ValueError:
    traceback.print_exc(file=sys.stdout)
    LOG.error('ERROR')


# common_map_fields: generates a map with time and acl values
def common_map_fields():
    default_map = {
        "created": "1964-08-25T10:00:00.0Z",
        "updated": "1964-08-25T10:00:00.0Z",
        "acl": acl
    }
    return default_map


###############################################################################


# get_user_by_id: get user by id
def get_user_by_id(user_id):
    try:
        resp = api.cimi_search("users", filter="id='" + user_id + "'")
        if resp.count == 1:
            return resp.json['users'][0] # dict
        else:
            LOG.warning("User not found [user_id=" + user_id + "]")
            return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_all: get all resources
def get_all(resource_type):
    try:
        return api.cimi_search(resource_type)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_resource_by_id: get resource by id
def get_resource_by_id(resource_id):
    try:
        return api.cimi_get(resource_id)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# delete_resource: delete resource by id
def delete_resource(resource_id):
    try:
        return api.cimi_delete(resource_id)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_user_profile: get profile from user
def get_user_profile(user_id):
    try:
        resp = api.cimi_search("profiles", filter="user_id='" + user_id + "'")
        if resp.count == 1:
            return resp.json['profiles'][0] # dict
        else:
            LOG.warning("User's profile not found [user_id=" + user_id + "]")
            return -1
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_user_sharing_model: get sharing model from user
def get_user_sharing_model(user_id):
    try:
        resp = api.cimi_search("sharingmodels", filter="user_id='" + user_id + "'")
        if resp.count == 1:
            return resp.json['sharingmodels'][0]  # dict
        else:
            LOG.warning("User's sharing model not found [user_id=" + user_id + "]")
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
        content.update(common_map_fields())

        resp = api.cimi_add(resource_name, content)
        LOG.debug("resp:        " + str(resp.message))
        LOG.debug("resource-id: " + str(resp.json['resource-id']))

        return get_resource_by_id(resp.json['resource-id'])
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# add_resource: add resource to cimi
def update_resource(resource_id, content):
    try:
        LOG.debug("Adding new resource to [" + resource_id + "] ... ")

        # complete map and update resource
        content.update(common_map_fields())

        resp = api.cimi_edit(resource_id, content)
        LOG.debug("resp: " + str(resp))
        LOG.debug("id: " + str(resp.id))

        return get_resource_by_id(resp.id)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


###############################################################################
# TESTS

# create_user: create a user in cimi
def create_admin_user_test():
    try:
        body = {
                "userTemplate": {
                    "href": "user-template/auto",
                    "password": "E9E633097AB9CEB3E48EC3F70EE2BEBA41D05D5420EFEE5DA85F97D97005727587FDA33EF4FF2322088F4C79E8133CC9CD9F3512F4D3A303CBDB5BC585415A00",
                    "emailAddress": "mf2c-developers@lists.atosresearch.eu",
                    "roles": "ADMIN",
                    "username": "testuser",
                    "firstName": "Test",
                    "state": "ACTIVE",
                    "organization": "mF2C",
                    "lastName": "User",
                    "resourceURI": "http://sixsq.com/slipstream/1/User",
                    "isSuperUser": False
                }
            }

        r = requests.post('https://192.168.252.41/api/user',
                          verify=False,
                          headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json'},
                          json=body)
        LOG.debug(str(r))
        LOG.debug(r.content)
        LOG.debug(r.status_code)
        LOG.debug(r.ok)
        if r.status_code == 201:
            LOG.info('OK')
        else:
            LOG.error('ERROR')
    except:
        LOG.error('Exception')


def create_anon_user_test():
    try:
        body = {
                "userTemplate": {
                    "href": "user-template/auto",
                    "password": "E9E633097AB9CEB3E48EC3F70EE2BEBA41D05D5420EFEE5DA85F97D97005727587FDA33EF4FF2322088F4C79E8133CC9CD9F3512F4D3A303CBDB5BC585415A00",
                    "emailAddress": "mf2c-developers2@lists.atosresearch.eu",
                    "roles": "ANON",
                    "username": "testuser2",
                    "firstName": "Test2",
                    "state": "ACTIVE",
                    "organization": "mF2C",
                    "lastName": "User",
                    "resourceURI": "http://sixsq.com/slipstream/1/User",
                    "isSuperUser": False
                }
            }

        r = requests.post('https://192.168.252.41/api/user',
                          verify=False,
                          headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json'},
                          json=body)
        LOG.debug(str(r))
        LOG.debug(r.content)
        LOG.debug(r.status_code)
        LOG.debug(r.ok)
        if r.status_code == 201:
            LOG.info('OK')
        else:
            LOG.error('ERROR')
    except:
        LOG.error('Exception')


# add_profile_test
def add_profile_test():
    profile = {
        "user_id": "user/testuser",
        "id": "https://192.168.252.41/api/profile/ProfileResource/asdasdasdasd2f81",
        "resourceURI": "https://192.168.252.41/api/profile/ProfileResource/asdasdasdasd2f81",
        "id_key": "asdasdasdasd2f81",
        "email": "email1@gmail.com",
        "service_consumer": True,
        "resource_contributor": False
    }
    resp = add_resource("profiles", profile)
    return resp


# edit_profile_test
def edit_profile_test():
    resp = get_user_profile("user/testuser")
    if resp:
        profile2 = {
            "service_consumer": False
        }

        resp = update_resource(resp['id'], profile2)
        return resp
    return None
