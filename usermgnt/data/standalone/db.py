"""
db: pydblite (https://pydblite.readthedocs.io)
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 17 june 2019

@author: Roi Sucasas - ATOS
"""

import config
import uuid
from usermgnt.common.logs import LOG
from pydblite.pydblite import Base


DB_SHARING_MODEL = None
DB_USER_PROFILE = None

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
'''

# init: initialize elements
def init():
    global DB_SHARING_MODEL
    global DB_USER_PROFILE
    try:
        # DB_SHARING_MODEL:
        LOG.info("[usermgnt.data.standalone.db] [init] Initializing DB_SHARING_MODEL [" + config.dic['UM_WORKING_DIR_VOLUME'] + config.dic['DB_SHARING_MODEL'] + "] ...")
        DB_SHARING_MODEL = Base(config.dic['UM_WORKING_DIR_VOLUME'] + config.dic['DB_SHARING_MODEL'])
        if not DB_SHARING_MODEL.exists():
            # create new base with field names
            DB_SHARING_MODEL.create('id', 'user_id', 'device_id', 'max_apps', 'battery_limit')
        else:
            DB_SHARING_MODEL.open()

        # DB_USER_PROFILE:
        LOG.info("[usermgnt.data.standalone.db] [init] Initializing DB_USER_PROFILE [" + config.dic['UM_WORKING_DIR_VOLUME'] + config.dic['DB_USER_PROFILE'] + "] ...")
        DB_USER_PROFILE = Base(config.dic['UM_WORKING_DIR_VOLUME'] + config.dic['DB_USER_PROFILE'])
        if not DB_USER_PROFILE.exists():
            # create new base with field names
            DB_USER_PROFILE.create('id', 'user_id', 'device_id', 'service_consumer', 'resource_contributor')
        else:
            DB_USER_PROFILE.open()
    except:
        LOG.exception('[usermgnt.data.standalone.db] [init] Exception: Error while initializing db components')


# print_records
def __print_records(db):
    LOG.debug('[usermgnt.data.standalone.db] [__print_records] Retrieving records from db...')
    records = db()
    for r in records:
        LOG.debug("db> " + str(r))


###############################################################################
# DB_USER_PROFILE

# get_from_USER_PROFILE
def get_from_USER_PROFILE(user_id, device_id):
    try:
        # print_records(DB_DOCKER_PORTS) # debug DB
        records = [r for r in DB_USER_PROFILE if r['user_id'] == user_id and r['device_id'] == device_id]
        LOG.debug("[usermgnt.data.standalone.db] [get_from_USER_PROFILE] records: " + str(records))

        if len(records) >= 1:
            return list(records)[0]
        else:
            LOG.warning('[usermgnt.data.standalone.db] [get_from_USER_PROFILE] No records found')
    except:
        LOG.exception('[usermgnt.data.standalone.db] [get_from_USER_PROFILE] Exception')
    return None


# get_from_USER_PROFILE_by_device_id
def get_from_USER_PROFILE_by_device_id(device_id):
    try:
        # print_records(DB_DOCKER_PORTS) # debug DB
        records = [r for r in DB_USER_PROFILE if r['device_id'] == device_id]
        LOG.debug("[usermgnt.data.standalone.db] [get_from_USER_PROFILE_by_device_id] records: " + str(records))

        if len(records) >= 1:
            return list(records)[0]
        else:
            LOG.warning('[usermgnt.data.standalone.db] [get_from_USER_PROFILE_by_device_id] No records found')
    except:
        LOG.exception('[usermgnt.data.standalone.db] [get_from_USER_PROFILE_by_device_id] Exception')
    return None


# get_from_USER_PROFILE_by_id
def get_from_USER_PROFILE_by_id(id):
    try:
        # print_records(DB_DOCKER_PORTS) # debug DB
        records = [r for r in DB_USER_PROFILE if r['id'] == id]
        LOG.debug("[usermgnt.data.standalone.db] [get_from_USER_PROFILE_by_id] records: " + str(records))

        if len(records) >= 1:
            return list(records)[0]
        else:
            LOG.warning('[usermgnt.data.standalone.db] [get_from_USER_PROFILE_by_id] No records found')
    except:
        LOG.exception('[usermgnt.data.standalone.db] [get_from_USER_PROFILE_by_id] Exception')
    return None


# get_current_USER_PROFILE
def get_current_USER_PROFILE():
    try:
        records = DB_USER_PROFILE()
        LOG.debug("[usermgnt.data.standalone.db] [get_current_USER_PROFILE] records: " + str(records))

        if len(records) >= 1:
            return list(records)[0]
        else:
            LOG.warning('[usermgnt.data.standalone.db] [get_current_USER_PROFILE] No records found')
    except:
        LOG.exception('[usermgnt.data.standalone.db] [get_current_USER_PROFILE] Exception')
    return None


# save_to_USER_PROFILE
def save_to_USER_PROFILE(user_id, device_id, service_consumer, resource_contributor):
    LOG.debug('[usermgnt.data.standalone.db] [save_to_USER_PROFILE] Saving record ...')

    # 1. there is only one record [user-profile] per device: delete all
    del_all_from_USER_PROFILE()

    # 2. add record
    try:
        record = get_from_USER_PROFILE(user_id, device_id)
        if record is None:
            id = user_id + "_" + str(uuid.uuid4())
            DB_USER_PROFILE.insert(id=id, user_id=user_id, device_id=device_id, service_consumer=service_consumer, resource_contributor=resource_contributor)
            DB_USER_PROFILE.commit() # save changes on disk

            # debug DB
            __print_records(DB_USER_PROFILE)
            return "saved"
        else:
            LOG.warning('[usermgnt.data.standalone.db] [save_to_USER_PROFILE] User-Profile already added to DB')
            return None
    except:
        LOG.exception('[usermgnt.data.standalone.db] [save_to_USER_PROFILE] Exception')
        return None


# update_USER_PROFILE
def update_USER_PROFILE(id, service_consumer, resource_contributor):
    LOG.debug('[usermgnt.data.standalone.db] [update_USER_PROFILE] Updating record ...')
    try:
        record = get_from_USER_PROFILE_by_id(id)
        if record is not None:
            DB_USER_PROFILE.update(record, service_consumer=service_consumer, resource_contributor=resource_contributor)
            DB_USER_PROFILE.commit() # save changes on disk

            # debug DB
            __print_records(DB_USER_PROFILE)
            return "updated"
        else:
            LOG.warning('[usermgnt.data.standalone.db] [update_USER_PROFILE] User-Profile not found')
            return None
    except:
        LOG.exception('[usermgnt.data.standalone.db] [update_USER_PROFILE] Exception')
        return None


# del_from_USER_PROFILE
def del_from_USER_PROFILE(user_id, device_id):
    try:
        record = get_from_USER_PROFILE(user_id, device_id)
        if record is not None:
            LOG.debug("[usermgnt.data.standalone.db] [del_from_USER_PROFILE] deleted records: " + str(DB_USER_PROFILE.delete(record)))
            DB_USER_PROFILE.commit() # save changes on disk
            return "deleted"
        else:
            LOG.warning('[usermgnt.data.standalone.db] [del_from_USER_PROFILE] User-Profile not found')
            return None
    except:
        LOG.exception('[usermgnt.data.standalone.db] [del_from_USER_PROFILE] Exception')
        return None


# del_from_USER_PROFILE
def del_from_USER_PROFILE_by_id(id):
    try:
        record = get_from_USER_PROFILE_by_id(id)
        if record is not None:
            LOG.debug("[usermgnt.data.standalone.db] [del_from_USER_PROFILE_by_id] deleted records: " + str(DB_USER_PROFILE.delete(record)))
            DB_USER_PROFILE.commit() # save changes on disk
            return "deleted"
        else:
            LOG.warning('[usermgnt.data.standalone.db] [del_from_USER_PROFILE_by_id] User-Profile not found')
            return None
    except:
        LOG.exception('[usermgnt.data.standalone.db] [del_from_USER_PROFILE_by_id] Exception')
        return None


# del_all_from_USER_PROFILE
def del_all_from_USER_PROFILE():
    try:
        records = DB_USER_PROFILE()
        if len(records) > 0:
            for r in records:
                DB_USER_PROFILE.delete(r)
            return True
        else:
            LOG.warning('[usermgnt.data.standalone.db] [del_all_from_USER_PROFILE] No records [User-Profile] found')
            return False
    except:
        LOG.exception('[usermgnt.data.standalone.db] [del_all_from_USER_PROFILE] Exception')
        return False


###############################################################################
# DB_SHARING_MODEL

# get_from_SHARING_MODEL
def get_from_SHARING_MODEL(user_id, device_id):
    try:
        # print_records(DB_SHARING_MODEL) # debug DB
        records = [r for r in DB_SHARING_MODEL if r['user_id'] == user_id and r['device_id'] == device_id]
        LOG.debug("[usermgnt.data.standalone.db] [get_from_SHARING_MODEL] records: " + str(records))

        if len(records) >= 1:
            return list(records)[0]
        else:
            LOG.warning('[usermgnt.data.standalone.db] [get_from_SHARING_MODEL] No records found')
    except:
        LOG.exception('[usermgnt.data.standalone.db] [get_from_SHARING_MODEL] Exception')
    return None


# get_from_SHARING_MODEL_by_device_id
def get_from_SHARING_MODEL_by_device_id(device_id):
    try:
        # print_records(DB_DOCKER_PORTS) # debug DB
        records = [r for r in DB_SHARING_MODEL if r['device_id'] == device_id]
        LOG.debug("[usermgnt.data.standalone.db] [get_from_SHARING_MODEL_by_device_id] records: " + str(records))

        if len(records) >= 1:
            return list(records)[0]
        else:
            LOG.warning('[usermgnt.data.standalone.db] [get_from_SHARING_MODEL_by_device_id] No records found')
    except:
        LOG.exception('[usermgnt.data.standalone.db] [get_from_SHARING_MODEL_by_device_id] Exception')
    return None


# get_from_SHARING_MODEL_by_id
def get_from_SHARING_MODEL_by_id(id):
    try:
        # print_records(DB_DOCKER_PORTS) # debug DB
        records = [r for r in DB_SHARING_MODEL if r['id'] == id]
        LOG.debug("[usermgnt.data.standalone.db] [get_from_SHARING_MODEL_by_id] records: " + str(records))

        if len(records) >= 1:
            return list(records)[0]
        else:
            LOG.warning('[usermgnt.data.standalone.db] [get_from_SHARING_MODEL_by_id] No records found')
    except:
        LOG.exception('[usermgnt.data.standalone.db] [get_from_SHARING_MODEL_by_id] Exception')
    return None


# get_current_SHARING_MODEL
def get_current_SHARING_MODEL():
    try:
        records = DB_SHARING_MODEL()
        LOG.debug("[usermgnt.data.standalone.db] [get_current_SHARING_MODEL] records: " + str(records))

        if len(records) >= 1:
            return list(records)[0]
        else:
            LOG.warning('[usermgnt.data.standalone.db] [get_current_SHARING_MODEL] No records found')
    except:
        LOG.exception('[usermgnt.data.standalone.db] [get_current_SHARING_MODEL] Exception')
    return None


# save_to_SHARING_MODEL
def save_to_SHARING_MODEL(user_id, device_id, max_apps, battery_limit):
    LOG.debug('[usermgnt.data.standalone.db] [save_to_SHARING_MODEL] Saving record ...')

    # 1. there is only one record [sharing-model] per device: delete all
    del_all_from_SHARING_MODEL()

    # 2. add record
    try:
        record = get_from_SHARING_MODEL(user_id, device_id)
        if record is None:
            id = user_id + "_" + str(uuid.uuid4())
            # 'id', 'user_id', 'device_id', 'max_apps', 'battery_limit'
            DB_SHARING_MODEL.insert(id=id, user_id=user_id, device_id=device_id, max_apps=max_apps, battery_limit=battery_limit)
            DB_SHARING_MODEL.commit() # save changes on disk

            # debug DB
            __print_records(DB_SHARING_MODEL)
            return "saved"
        else:
            LOG.warning('[usermgnt.data.standalone.db] [save_to_SHARING_MODEL] Sharing-Model already added to DB')
            return None
    except:
        LOG.exception('[usermgnt.data.standalone.db] [save_to_SHARING_MODEL] Exception')
        return None


# update_SHARING_MODEL
def update_SHARING_MODEL(id, max_apps, battery_limit):
    LOG.debug('[usermgnt.data.standalone.db] [update_SHARING_MODEL] Updating record ...')
    try:
        record = get_from_SHARING_MODEL_by_id(id)
        if record is not None:
            # 'id', 'user_id', 'device_id', 'max_apps', 'battery_limit'
            DB_SHARING_MODEL.update(record, max_apps=max_apps, battery_limit=battery_limit)
            DB_SHARING_MODEL.commit() # save changes on disk

            # debug DB
            __print_records(DB_SHARING_MODEL)
            return "updated"
        else:
            LOG.warning('[usermgnt.data.standalone.db] [update_SHARING_MODEL] Sharing-Model not found')
            return None
    except:
        LOG.exception('[usermgnt.data.standalone.db] [update_SHARING_MODEL] Exception')
        return None


# del_from_SHARING_MODEL
def del_from_SHARING_MODEL(user_id, device_id):
    try:
        record = get_from_SHARING_MODEL(user_id, device_id)
        if record is not None:
            LOG.debug("[usermgnt.data.standalone.db] [del_from_SHARING_MODEL] deleted records: " + str(DB_SHARING_MODEL.delete(record)))
            DB_SHARING_MODEL.commit() # save changes on disk
            return "deleted"
        else:
            LOG.warning('[usermgnt.data.standalone.db] [del_from_SHARING_MODEL] Sharing-Model not found')
            return None
    except:
        LOG.exception('[usermgnt.data.standalone.db] [del_from_SHARING_MODEL] Exception')
        return None


# del_from_SHARING_MODEL_by_id
def del_from_SHARING_MODEL_by_id(id):
    try:
        record = get_from_USER_PROFILE_by_id(id)
        if record is not None:
            LOG.debug("[usermgnt.data.standalone.db] [del_from_SHARING_MODEL_by_id] deleted records: " + str(DB_SHARING_MODEL.delete(record)))
            DB_SHARING_MODEL.commit() # save changes on disk
            return "deleted"
        else:
            LOG.warning('[usermgnt.data.standalone.db] [del_from_SHARING_MODEL_by_id] Sharing-Model not found')
            return None
    except:
        LOG.exception('[usermgnt.data.standalone.db] [del_from_SHARING_MODEL_by_id] Exception')
        return None


# del_all_from_SHARING_MODEL
def del_all_from_SHARING_MODEL():
    try:
        records = DB_SHARING_MODEL()
        if len(records) > 0:
            for r in records:
                DB_SHARING_MODEL.delete(r)
            return True
        else:
            LOG.warning('[usermgnt.data.standalone.db] [del_all_from_SHARING_MODEL] No records [Sharing-Model] found')
            return False
    except:
        LOG.exception('[usermgnt.data.standalone.db] [del_all_from_SHARING_MODEL] Exception')
        return False