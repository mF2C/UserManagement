"""
Default data adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 17 june 2019

@author: Roi Sucasas - ATOS
"""


from usermgnt.common.logs import LOG


# Data adapter class
class StandaloneDataAdapter:

    # FUNCTION: get_current_device_id
    def get_current_device_id(self):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_current_device_id] not implemented")
        return None


    # FUNCTION: get_current_device_ip
    def get_current_device_ip(self):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_current_device_ip] not implemented")
        return None


    # FUNCTION: get_leader_device_ip
    def get_leader_device_ip(self):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_leader_device_ip] not implemented")
        return None


    # FUNCTION: get_agent_info
    def get_agent_info(self):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_agent_info] not implemented")
        return None


    ###############################################################################
    # USER

    # FUNCTION: get_user_info: gets user info
    def get_user_info(self, user_id):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_user_info] not implemented")
        return None


    # FUNCTION: delete_user: deletes user
    def delete_user(self, user_id):
        LOG.warning("[usermgnt.data.default_data_adapter] [delete_user] not implemented")
        return None


    ###############################################################################
    # SHARING MODEL

    # FUNCTION: get_user_profile_by_id
    def get_sharing_model_by_id(self, sharing_model_id):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_sharing_model_by_id] not implemented")
        return None


    # Get shared resources
    def get_sharing_model(self, device_id):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_sharing_model] not implemented")
        return None


    # Initializes shared resources values
    def init_sharing_model(self, data):
        LOG.warning("[usermgnt.data.default_data_adapter] [init_sharing_model] not implemented")
        return None


    # Updates shared resources values
    def update_sharing_model_by_id(self, sharing_model_id, data):
        LOG.warning("[usermgnt.data.default_data_adapter] [update_sharing_model_by_id] not implemented")
        return None


    # delete_sharing_model_by_id: Deletes  shared resources values
    def delete_sharing_model_by_id(self, sharing_model_id):
        LOG.warning("[usermgnt.data.default_data_adapter] [delete_sharing_model_by_id] not implemented")
        return None


    # FUNCTION: get_current_sharing_model: Get current SHARING-MODEL
    def get_current_sharing_model(self):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_current_sharing_model] not implemented")
        return None


    ###############################################################################
    # USER-PROFILE

    # get_user_profile_by_id
    def get_user_profile_by_id(self, profile_id):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_user_profile_by_id] not implemented")
        return None


    # get_user_profile: Get user profile
    def get_user_profile(self, device_id):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_user_profile] not implemented")
        return None


    # update_user_profile_by_id: Updates a profile
    def update_user_profile_by_id(self, profile_id, data):
        LOG.warning("[usermgnt.data.default_data_adapter] [update_user_profile_by_id] not implemented")
        return None


    # Deletes users profile
    def delete_user_profile_by_id(self, profile_id):
        LOG.warning("[usermgnt.data.default_data_adapter] [delete_user_profile_by_id] not implemented")
        return None


    # Initializes users profile
    def register_user(self, data):
        LOG.warning("[usermgnt.data.default_data_adapter] [register_user] not implemented")
        return None


    # setAPPS_RUNNING
    def setAPPS_RUNNING(self, apps=0):
        LOG.warning("[usermgnt.data.default_data_adapter] [setAPPS_RUNNING] not implemented")
        return None


    # FUNCTION: get_current_user_profile: Get Current USER-PROFILE
    def get_current_user_profile(self):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_current_user_profile] not implemented")
        return None


    ###############################################################################
    ## AGENT INFO
    ## power, apps running ...

    # FUNCTION: get_total_services_running: Get services running
    def get_total_services_running(self):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_total_services_running] not implemented")
        return None


    # FUNCTION: get_power: Get battery level from DEVICE_DYNAMIC
    def get_power(self):
        LOG.warning("[usermgnt.data.default_data_adapter] [get_power] not implemented")
        return None


    ###############################################################################
    ## LOCAL VOLUME
    ## Used to store / read 'user_id' and 'device_id'

    # FUNCTION: save_device_id
    def save_device_id(self, device_id):
        LOG.warning("[usermgnt.data.default_data_adapter] [save_device_id] not implemented")
        return None


    # FUNCTION: read_device_id
    def read_device_id(self):
        LOG.warning("[usermgnt.data.default_data_adapter] [read_device_id] not implemented")
        return None