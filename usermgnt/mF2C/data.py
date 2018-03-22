"""
Data Management: dataclay, cimi...
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

import usermgnt.mF2C.cimi as cimi
from usermgnt.utils.logs import LOG
from usermgnt import config


###############################################################################
# USER

# Get user
def get_user_by_id(user_id):
    LOG.info("User-Management: Data: get_user: " + str(user_id))
    return cimi.get_user_by_id(user_id)


###############################################################################
# SHARING MODEL
#
# {
#       ----------------"user_id": "user/1230958abdef",
# 	    "max_apps": integer,
# 	    "gps_allowed": boolean,
# 	    "max_cpu_usage": integer,
# 	    "max_memory_usage": integer,
# 	    "max_storage_usage": integer,
# 	    "max_bandwidth_usage": integer,
# 	    "battery_limit": integer
# }

# Get shared resources
def get_sharing_model(user_id):
    LOG.info("User-Management: Data: get_sharing_model_values: " + str(user_id))
    return cimi.get_user_sharing_model(user_id)


# Initializes shared resources values
def init_sharing_model(data):
    LOG.info("User-Management: Data: init_sharing_model: " + str(data))
    return cimi.add_resource(config.dic['CIMI_SHARING_MODELS'], data)


# Updates shared resources values
def update_sharing_model(data):
    LOG.info("User-Management: Data: update_sharing_model_values: " + str(data))
    resp = cimi.get_user_sharing_model(data['user_id'])
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# Deletes  shared resources values
def delete_sharing_model(user_id):
    LOG.info("User-Management: Data: delete_sharing_model_values: " + user_id)
    resp = cimi.get_user_sharing_model(user_id)
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None


###############################################################################
# PROFILING
#
#  {
#       ----------------"user_id": "user/1230958abdef",
#  	    "id_key": string,
#  	    "email": string,
#  	    "service_consumer": boolean,
#  	    "resource_contributor": boolean
#  }

# Get user profile
def get_profiling(user_id):
    LOG.info("User-Management: Data: get_profiling: " + user_id)
    return cimi.get_user_profile(user_id)


# Get allowed services
def get_services(user_id):
    LOG.info("User-Management: Data: get_services: " + user_id)

    # TODO CIMI
    # ...

    return ['service_id_1', 'service_id_2', 'service_id_3']


# Initializes users profile
#   data: {'user_id':'', 'email':'', 'name':''}
def register_user(data):
    LOG.info("User-Management: Data: register_user: " + str(data))
    return cimi.add_resource(config.dic['CIMI_PROFILES'], data)


# Updates users profile
#   data: {'user_id':'', 'email':'', 'service_consumer': '', 'resource_contributor': ''}
def update_profile(data):
    LOG.info("User-Management: Data: update_profile: " + str(data))
    resp = cimi.get_user_profile(data['user_id'])
    if resp and resp == -1:
        return -1
    elif resp:
        resp = cimi.update_resource(resp['id'], data)
        return resp
    return None


# Deletes users profile
def delete_profile(user_id):
    LOG.info("User-Management: Data: delete_profile: " + user_id)
    resp = cimi.get_user_profile(user_id)
    if resp and resp == -1:
        return None
    elif resp:
        resp = cimi.delete_resource(resp['id'])
        return resp
    return None
