"""
CONFIGURATION FILE
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python

dic = { "SERVER_PORT":                  46300,
        "API_DOC_URL":                  "/api/v1/user-management",
        "CERT_CRT":                     "cert/ia.crt",
        "CERT_KEY":                     "cert/ia.key",
        "DEBUG":                        False,
        # for testing the interaction with the lifecycle management
        "ENABLE_ASSESSMENT_TESTS":      True,
        # VERIFY_SSL controls whether we verify the server's TLS certificate or not
        "VERIFY_SSL":                   False,
        # CIMI RESOURCES
        "CIMI_USERS":                   "users",
        "CIMI_PROFILES":                "user-profile", #"userProfiles",
        "CIMI_PROFILE":                 "user-profile",
        "CIMI_SHARING_MODELS":          "sharing-model", #"sharingModels",
        "CIMI_SHARING_MODEL":           "sharing-model",
        # URLs from other mF2C components:
        # CIMI
        "CIMI_URL":                     "https://dashboard.mf2c-project.eu/api",        # (env value) => https://proxy
        "CIMI_COOKIES_PATH":            "~./cookies",
        "CIMI_USER":                    "rsucasas",                                     # (env value)
        "CIMI_PASSWORD":                "password",                                     # (env value)
        # PM-Lifecycle: /api/v1/lifecycle/<string:service_id>
        "URL_PM_LIFECYCLE":             "https://127.0.0.1:46000/api/v1/lifecycle/",
        # PM-Landscaper: api/v1/landscape/...
        "URL_PM_LANDSCAPER":            "https://127.0.0.1:46010/api/v1/landscaper/"}