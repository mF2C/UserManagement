"""
CONFIGURATION FILE
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python

dic = { "VERSION":                      "1.2.8",

        # USER MANAGEMENT MODULE MODE: "DEFAULT", "MF2C" , "STANDALONE"
        "UM_MODE":                      "MF2C",

        # CIMI
        "CIMI_URL":                     "http://cimi:8201/api",         # https://dashboard.mf2c-project.eu/api
        "DEVICE_USER":                  "rsucasas",

        # SERVER - REST API
        "SERVER_PORT":                  46300,
        "HOST_IP":                      "localhost",                       # if possible, read from env values
        "API_DOC_URL":                  "/api/v2/um",

        # working dir
        "UM_WORKING_DIR_VOLUME":        "/tmp/mf2c/um/",

        # db
        "DB_SHARING_MODEL":             "dbt1",
        "DB_USER_PROFILE":              "dbt2",

        # VERIFY_SSL controls whether we verify the server's TLS certificate or not
        "VERIFY_SSL":                   False,

        # for testing the interaction with the lifecycle management
        "ENABLE_ASSESSMENT":            True,

        # CIMI RESOURCES managed by this component
        "CIMI_PROFILES":                "user-profile",  # "userProfiles",
        "CIMI_SHARING_MODELS":          "sharing-model",  # "sharingModels",
        "SERVICE_CONSUMER":             True,
        "RESOURCE_CONTRIBUTOR":         True,
        "MAX_APPS":                     2,
        "BATTERY_LIMIT":                50,
        "GPS_ALLOWED":                  True,
        "MAX_CPU_USAGE":                50,
        "MAX_MEM_USAGE":                50,
        "MAX_STO_USAGE":                50,
        "MAX_BANDWITH_USAGE":           50,

        # URLs / ports from other mF2C components:
        # LIFECYCLE
        "URL_PM_LIFECYCLE":             "http://lifecycle:46000/api/v2/lm"
}


# APPS RUNNING
APPS_RUNNING = 0