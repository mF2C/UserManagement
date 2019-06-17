"""
db: pydblite (https://pydblite.readthedocs.io)
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 17 june 2019

@author: Roi Sucasas - ATOS
"""

import config
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
        LOG.info('[usermgnt.data.app.db] [init] Initializing DB_SHARING_MODEL ...')
        DB_SHARING_MODEL = Base(config.dic['UM_WORKING_DIR_VOLUME'] + config.dic['DB_SHARING_MODEL'])
        if not DB_SHARING_MODEL.exists():
            # create new base with field names
            DB_SHARING_MODEL.create('user_id', 'device_id', 'max_apps', 'battery_limit')
        else:
            DB_SHARING_MODEL.open()

        # DB_USER_PROFILE:
        LOG.info('[usermgnt.data.app.db] [init] Initializing DB_USER_PROFILE ...')
        DB_USER_PROFILE = Base(config.dic['UM_WORKING_DIR_VOLUME'] + config.dic['DB_USER_PROFILE'])
        if not DB_USER_PROFILE.exists():
            # create new base with field names
            DB_USER_PROFILE.create('user_id', 'device_id', 'service_consumer', 'resource_contributor')
        else:
            DB_USER_PROFILE.open()
    except:
        LOG.exception('[usermgnt.data.app.db] [init] Exception: Error while initializing db components')


# print_records
def __print_records(db):
    LOG.debug('[usermgnt.data.app.db] [__print_records] Retrieving records from db...')
    records = db()
    for r in records:
        LOG.debug("db> " + str(r))


###############################################################################
# DB_USER_PROFILE

# get_from_DB_DOCKER_PORTS
def get_from_USER_PROFILE(user_id, device_id):
    try:
        # debug DB
        # print_records(DB_DOCKER_PORTS)
        records = [r for r in DB_USER_PROFILE if r['user_id'] == user_id and r['device_id'] == device_id]
        LOG.debug("[usermgnt.data.app.db] [get_from_USER_PROFILE] records: " + str(records))

        #records = DB_DOCKER_PORTS(port=port)
        if len(records) >= 1:
            return records[0]
        else:
            LOG.warning('[usermgnt.data.app.db] [get_from_USER_PROFILE] No records found')
    except:
        LOG.exception('[usermgnt.data.app.db] [get_from_USER_PROFILE] Exception')
    return None


# save_to_DB_DOCKER_PORTS
def save_to_USER_PROFILE(user_id, device_id, service_consumer, resource_contributor):
    LOG.debug('[usermgnt.data.app.db] [save_to_DB_DOCKER_PORTS] Saving record ...')
    try:
        record = get_from_USER_PROFILE(user_id, device_id)
        if record is None:
            DB_USER_PROFILE.insert(user_id=user_id, device_id=device_id, service_consumer=service_consumer, resource_contributor=resource_contributor)
            # save changes on disk
            DB_USER_PROFILE.commit()

            # debug DB
            __print_records(DB_USER_PROFILE)
            return True
        else:
            LOG.warning('[usermgnt.data.app.db] [save_to_USER_PROFILE] Port already added to DB')
            return False
    except:
        LOG.exception('[usermgnt.data.app.db] [save_to_USER_PROFILE] Exception')
        return False


# update_USER_PROFILE
def update_USER_PROFILE(user_id, device_id, service_consumer, resource_contributor):
    LOG.debug('[usermgnt.data.app.db] [update_USER_PROFILE] Saving record ...')
    try:
        record = get_from_USER_PROFILE(user_id, device_id)
        if record is not None:
            DB_USER_PROFILE.update(record, service_consumer=service_consumer, resource_contributor=resource_contributor)
            # save changes on disk
            DB_USER_PROFILE.commit()

            # debug DB
            __print_records(DB_USER_PROFILE)
            return True
        else:
            LOG.warning('[usermgnt.data.app.db] [update_USER_PROFILE] Port already added to DB')
            return False
    except:
        LOG.exception('[usermgnt.data.app.db] [update_USER_PROFILE] Exception')
        return False


# del_from_DB_DOCKER_PORTS
def del_from_USER_PROFILE(user_id, device_id):
    try:
        record = get_from_USER_PROFILE(user_id, device_id)
        if record is not None:
            LOG.debug("[usermgnt.data.app.db] [del_from_USER_PROFILE] deleted records: " + str(DB_USER_PROFILE.delete(record)))
            # save changes on disk
            DB_USER_PROFILE.commit()
            return True
        else:
            LOG.warning('[usermgnt.data.app.db] [del_from_USER_PROFILE] Port was not found in DB')
            return False
    except:
        LOG.exception('[usermgnt.data.app.db] [del_from_USER_PROFILE] Exception')
        return False


###############################################################################
# DB_SHARING_MODEL