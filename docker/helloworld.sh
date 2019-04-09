#!/bin/bash

# DEVICE
echo "1. Creating new device ... \n"

device_id=$(curl \
--insecure \
--header "Content-type: application/json" \
--header "slipstream-authn-info: super ADMIN" \
--request POST \
--data '{
    "deviceID": "agent_1",
    "isLeader": false,
    "os": "Linux-4.13.0-38-generic-x86_64-with-debian-8.10",
    "arch": "x86_64",
    "cpuManufacturer": "Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz",
    "physicalCores": 4,
    "logicalCores": 8,
    "cpuClockSpeed": "1.8000 GHz",
    "memory": 7874.2109375,
    "storage": 234549.5078125,
    "powerPlugged": true,
	"agentType": "<agentType>",
	"actuatorInfo": "<actuatorInfo>",
    "networkingStandards": "['eth0', 'lo']",
    "ethernetAddress": "192.168.252.41",
    "wifiAddress": "Empty",
    "hwloc": "<xmlString>",
    "cpuinfo": "<rawCPUinfo>"
}' \
https://localhost/api/device | jq -r '.["resource-id"]')

echo "2. Device submitted: $device_id \n"


# DEVICE_DYNAMIC
echo "Creating new device dynamic instance ... \n"

device_dynamic_id=$(curl \
--insecure \
--header "Content-type: application/json" \
--header "slipstream-authn-info: super ADMIN" \
--request POST \
--data '{
    "device": {"href": "'"$device_id"'"},
    "ramFree": 4795.15234375,
    "ramFreePercent": 60.9,
    "storageFree": 208409.25,
    "storageFreePercent": 93.6,
    "cpuFreePercent": 93.5,
    "powerRemainingStatus": "60.75885328836425",
    "powerRemainingStatusSeconds": "3817",
    "ethernetAddress": "192.168.252.41",
    "wifiAddress": "Empty",
	"ethernetThroughputInfo": ["E","m","p","t","y"],
    "wifiThroughputInfo": ["a"],
    "myLeaderID": {"href": "'"$device_id"'"}
}' \
https://localhost/api/device-dynamic | jq -r '.["resource-id"]')

echo "Device Dynamic instance submitted: $device_dynamic_id \n"


# USER
echo "3. Creating new user ... \n"

user_id=$(curl \
--insecure \
--header "Content-type: application/json" \
--header "slipstream-authn-info: super ADMIN" \
--request POST \
--data '{
    "userTemplate": {
        "href": "user-template/self-registration",
        "password": "testpassword",
        "passwordRepeat" : "testpassword",
        "emailAddress": "test@gmail.com",
        "username": "testuser1"
    }
}' \
https://localhost/api/user | jq -r '.["resource-id"]')

echo "User submitted: $user_id \n"



# SERVICE (COMPSS)
echo "4. Creating new COMPSs service ... \n"

service_id=$(curl \
--insecure \
--header "Content-type: application/json" \
--header "slipstream-authn-info: super ADMIN" \
--request POST \
--data '{
	"name": "compss-test",
	"description": "compss-test IT-2",
	"exec": "mf2c/compss-test:it2",
	"os": "linux",
	"disk": 100,
	"category": 0,
	"num_agents": 1,
	"exec_type": "compss",
	"exec_ports": [80],
	"agent_type": "normal",
	"cpu_arch": "x86-64",
	"memory_min": 1000,
	"storage_min": 100,
	"req_resource": [],
	"opt_resource": []
}' \
https://localhost/api/service | jq -r '.["resource-id"]')

echo "Service submitted: $service_id \n"


# AGREEMENT
echo "5. Creating new SLA ... \n"

agreement_id=$(curl \
--insecure \
--header "Content-type: application/json" \
--header "slipstream-authn-info: super ADMIN" \
--request POST \
--data '{
    "name": "compss-hello-world",
    "state": "started",
    "details":{
        "id": "a02",
        "type": "agreement",
        "name": "compss-hello-world",
        "provider": { "id": "mf2c", "name": "mF2C Platform" },
        "client": { "id": "c02", "name": "A client" },
        "creation": "2018-01-16T17:09:45.01Z",
        "expiration": "2019-01-17T17:09:45.01Z",
        "guarantees": [
            {
                "name": "TestGuarantee",
                "constraint": "execution_time < 10"
            }
        ]
    }
}' \
https://localhost/api/agreement | jq -r '.["resource-id"]')

echo "Agreement submitted: $agreement_id \n"


# USER-PROFILE
echo "6. Creating user-profile ... \n"

user_profile=$(curl \
--insecure \
--header "Content-type: application/json" \
--request POST \
--data '{
	"user_id": "'"$user_id"'",
	"device_id": "'"$device_id"'",
	"service_consumer": true,
	"resource_contributor": true,
	"max_apps": 1
}' \
http://localhost:46300/api/v2/um/user-profile | jq -r .message)

echo "User Profile: $user_profile \n"


# SHARING-MODEL
echo "7. Creating sharing-model ... \n"

sharing_model=$(curl \
--insecure \
--header "Content-type: application/json" \
--request POST \
--data '{
	"user_id": "'"$user_id"'",
	"device_id": "'"$device_id"'",
	"gps_allowed": false,
	"max_cpu_usage": 3,
	"max_memory_usage": 3,
	"max_storage_usage": 3,
	"max_bandwidth_usage": 3,
	"battery_limit": 30
}' \
http://localhost:46300/api/v2/um/sharing-model | jq -r .message)

echo "Sharing Model: $sharing_model \n"


# SERVICE_INSTANCE
echo "8. Launching a service ... \n"

service_instance=$(curl \
--insecure \
--header "Content-type: application/json" \
--request POST \
--data '{"service_id": "'"$service_id"'", "agreement_id": "'"$agreement_id"'", "user_id": "'"$user_id"'"}' \
http://localhost:46000/api/v2/lm/service | jq -r .message)

echo "Service instance: $service_instance \n"