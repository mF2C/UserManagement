"""
Data Management: dataclay, cimi...
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


from src.utils.logs import LOG
# TODO Dataclay / CIMI initialization
# from model_mf2c.classes import *
# from dataclay import api


# api.init()
# ...


###############################################################################
# SHARING MODEL


fake_sharing_model_info = {
    "max_apps": 1,
    "GPS_allowed": False,
    "max_CPU_usage": 50,
    "max_memory_usage": 200,
    "max_storage_usage": 1000,
    "max_bandwidth_usage": 1000,
    "battery_limit": 25
}


# Get shared resources
def get_sharing_model_values(user_id):
    sharing_model = None
    try:
        LOG.info("User-Management: Data: get_sharing_model_values: " + str(user_id))

        # TODO Dataclay or CIMI
        #...

        return fake_sharing_model_info
    except:
        LOG.error('User-Management: Data: get_sharing_model_values: Exception')
    return sharing_model


# Initializes shared resources values
def init_sharing_model(data):
    sharing_model = None
    try:
        LOG.info("User-Management: Data: init_sharing_model: " + str(data))

        # TODO Dataclay or CIMI
        #...

        return fake_sharing_model_info
    except:
        LOG.error('User-Management: Data: init_sharing_model: Exception')
    return sharing_model


# Updates shared resources values
def update_sharing_model_values(data):
    sharing_model = None
    try:
        LOG.info("User-Management: Data: update_sharing_model_values: " + str(data))

        # TODO Dataclay or CIMI
        #...

        return fake_sharing_model_info
    except:
        LOG.error('User-Management: Data: update_sharing_model_values: Exception')
    return sharing_model


# Deletes  shared resources values
def delete_sharing_model_values(user_id):
    try:
        LOG.info("User-Management: Data: delete_sharing_model_values: " + user_id)

        # TODO Dataclay or CIMI
        #...

        return True
    except:
        LOG.error('User-Management: Data: delete_sharing_model_values: Exception')
    return False


###############################################################################
# PROFILING

# Get user profile
def get_profiling(user_id):
    user_profile = None
    try:
        LOG.info("User-Management: Data: get_profiling: " + user_id)

        # TODO Dataclay or CIMI
        # Get user profile:
        #user_profile = User.get_by_alias(user_id)
        #...

        return {'email': 'TEST@EMAIL.COM', 'service_consumer': True, 'resource_contributor': True}
    except:
        LOG.error('User-Management: Data: get_profiling: Exception')
    return user_profile


# Get allowed services
def get_services(user_id):
    services = None
    try:
        LOG.info("User-Management: Data: get_services: " + user_id)

        # TODO Dataclay or CIMI
        # Get user profile:
        #user_profile = User.get_by_alias(user_id)
        #...

        return ['service_id_1', 'service_id_2', 'service_id_3']
    except:
        LOG.error('User-Management: Data: get_services: Exception')
    return services


# Initializes users profile
#   data: {'user_id':'', 'email':''}
def register_user(data):
    user_profile = None
    try:
        LOG.info("User-Management: Data: register_user: " + str(data))

        # TODO Dataclay or CIMI
        # Create and store user:
        # my_user = User(user_id=data['user_key'], email=data['email'], name=data['name'])
        # my_user.make_persistent(alias=data['user_key'])
        # ...

        return {'email': data['email'], 'service_consumer': True, 'resource_contributor': True}
    except:
        LOG.error('User-Management: Data: register_user: Exception')
    return user_profile


# Updates users profile
#   data: {'user_id':'', 'email':'', 'service_consumer': '', 'resource_contributor': ''}
def update_profile(data):
    user_profile = None
    try:
        LOG.info("User-Management: Data: update_profile: " + str(data))

        # TODO Dataclay or CIMI
        # Create and store user:
        # my_user = User(user_id=data['user_key'], email=data['email'], name=data['name'])
        # my_user.make_persistent(alias=data['user_key'])
        # ...

        return {'email': 'TEST@EMAIL.COM', 'service_consumer': True, 'resource_contributor': True}
    except:
        LOG.error('User-Management: Data: update_profile: Exception')
    return user_profile


# Deletes users profile
#   data: {'user_id':''}
def delete_profile(user_id):
    try:
        LOG.info("User-Management: Data: delete_profile: " + user_id)

        # TODO Dataclay or CIMI
        #...

        # deletes / resets sharing model
        return delete_sharing_model_values(user_id)
    except:
        LOG.error('User-Management: Data: delete_profile: Exception')
    return False
