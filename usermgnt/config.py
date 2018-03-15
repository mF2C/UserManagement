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
        # URLs from other mF2C components:
        # CIMI
        "CIMI_URL":                     "https://192.192.192.192",
        "CIMI_COOKIES_PATH":            "~./cookies",           # "C://TMP/cookies",
        "CIMI_USER":                    "testuser2",
        "CIMI_PASSWORD":                "testpassword",
        # PM-Lifecycle: /api/v1/lifecycle/<string:service_id>
        "URL_PM_LIFECYCLE":             "https://192.192.192.192:46000/api/v1/lifecycle/",
        # PM-Landscaper: api/v1/landscape/...
        "URL_PM_LANDSCAPER":            "https://192.192.192.192:46010/api/v1/landscaper/"}