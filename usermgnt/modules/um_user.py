"""
User operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 23 sept. 2019

@author: Roi Sucasas - ATOS
"""

from usermgnt.data import data_adapter as data_adapter
from usermgnt.common import common as common
from usermgnt.common.logs import LOG


# FUNCTION: get_user: Get user
def get_user(user_id):
    LOG.debug("[usermgnt.modules.um_user] [get_user] user_id=" + str(user_id))
    user = data_adapter.get_user_info(user_id)
    if user is None:
        return common.gen_response(500, 'Error or User not found', 'user_id', user_id, 'user', {})
    elif user == -1:
        return common.gen_response(403, "Warning: User " + user_id + " has no permissions on this device",
                                   'user_id', user_id, 'user', {})
    else:
        return common.gen_response_ok('User found', 'user_id', user_id, 'user', user)


# FUNCTION: delete_user: Deletes user
def delete_user(data):
    if 'user_id' not in data:
        LOG.warning('[usermgnt.modules.um_user] [delete_user] parameter not found: user_id')
        return common.gen_response(405, 'parameter not found: user_id', 'data', str(data))

    user_id = data['user_id']
    LOG.debug("[usermgnt.modules.um_user] [delete_user] user_id=" + str(user_id))
    user = data_adapter.delete_user(user_id)
    if user is None:
        return common.gen_response(500, 'Error or User not found', 'user_id', user_id, 'user', {})
    elif user == -1:
        return common.gen_response(403, "Warning: User " + user_id + " has no permissions on this device",
                                   'user_id', user_id, 'user', {})
    else:
        return common.gen_response_ok('User deleted', 'user_id', user_id)