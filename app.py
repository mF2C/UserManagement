#!/usr/bin/python3

"""
USER MANAGEMENT MODULE & LIFECYCLE MANAGER - REST API
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import config as config
# um
import usermgnt.init_config as um_init_config
import usermgnt.modules.um_profiling as um_profiling
import usermgnt.modules.um_sharing_model as um_sharing_model
import usermgnt.modules.um_assesment as um_assesment
# common
from common.logs import LOG
# ext
from flask_cors import CORS
from flask import Flask, request, Response, json
from flask_restful import Resource, Api
from flask_restful_swagger import swagger


'''
REST API
    Routes:
        Root:
            /api/v2
                        GET:    get rest api service status
            User Management:
                /um/
                        GET:    check initialization values
                        
                /um/user-profile/
                        GET:    get "current" profile
                        POST:   create a new profile
                /um/user-profile/<string:user_profile_id>
                        GET:    get profile by profile ID
                        PUT:    updates profile
                        DELETE: deletes profile
                /um/user-profile/user/<string:user_id>/device/<string:device_id>
                        GET:    get user's profile by user ID and device ID
                        PUT:    updates profile
                        DELETE: deletes profile
                        
                /um/sharing-model
                        GET:    get current sharing model
                        POST:   create new sharing model
                /um/sharing-model/<string:sharing_model_id>
                        GET:    get a sharing model
                        PUT:    updates a sharing model
                        DELETE: deletes a sharing model
                /um/sharing-model/user/<string:user_id>/profile/<string:device_id>
                        GET:    get user's sharing model
                        PUT:    updates sharing model
                        DELETE: deletes sharing model
                        
                /um/assesment
                        GET:    gets the status of the current assessment in the device
                        PUT:    start / stop assessment
'''


try:
    um_init_config.init()

    # APP
    app = Flask(__name__)
    CORS(app)

    # API DOC
    api = swagger.docs(Api(app),
                       apiVersion='1.0.1',
                       api_spec_url=config.dic['API_DOC_URL'],
                       produces=["application/json", "text/html"],
                       swaggerVersion="1.2",
                       description='mF2C - User Management REST API - version ' + config.dic['VERSION'],
                       basePath='http://localhost:' + str(config.dic['SERVER_PORT']),
                       resourcePath='/')
except ValueError:
    LOG.error('User-Management: app: Exception: Error while initializing app / api')


########################################################################################################################
### USER MANAGEMENT
########################################################################################################################

#
# API 'home' Route
#
#     '/api/v2/'
#         GET:    get rest api service status
#
@app.route('/api/v2/', methods=['GET'])
def default_route():
    data = {
        'app': "User Management module REST API", 'status': "Running", 'api_doc_json': "http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
        'api_doc_html': "http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + ".html#!/spec"
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


#
# UserManagementModule route:
#
#   '/api/v2/um/'
#            GET:    check initialization values
#
class UserManagementModule(Resource):
    # GET
    @swagger.operation(
        summary="Checks initialization values",
        notes="Checks initialization values",
        produces=["application/json"],
        authorizations=[],
        parameters=[],
        responseMessages=[{
            "code": 500,
            "message": "Exception processing request"
        }])
    def get(self):
        data = {
            'app': 'User Management modules REST API',
            'status': 'Running',
            'api_doc_json': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
            'api_doc_html': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic[
                'API_DOC_URL'] + '.html#!/spec'
        }
        resp = Response(json.dumps(data), status=200, mimetype='application/json')
        return resp

api.add_resource(UserManagementModule, '/api/v2/um')


########################################################################################################################
### PROFILE
########################################################################################################################
#
#  ProfileInstanceById route:
#
#     '/api/v2/um/user-profile/<string:user_profile_id>'
#
#         GET:    get profile by ID
#         PUT:    updates profile
#         DELETE: deletes profile
#
class ProfileInstanceById(Resource):
    # GET Get Profile by ID
    @swagger.operation(
        summary="Returns a profile by ID",
        notes="Returns a profile by ID",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_profile_id",
                "description": "User ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, user_profile_id):
        return um_profiling.get_user_profile_by_id(user_profile_id)


    # PUT Updates the users profile
    @swagger.operation(
        summary="Updates a profile.",
        notes="Updates a profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_profile_id",
                "description": "User ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"user/testuser\", "
                               "\"device_id\":\"device/50b12ccc-76fb-45a6-af7f-634312bc7ca5\", "
                               "\"resource_contributor\":false, \"service_consumer\":false, \"max_apps\":1}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 405,
                "message": "User ID / Device ID parameters not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def put(self, user_profile_id):
        return um_profiling.update_user_profile_by_id(user_profile_id, request.get_json())


    # DELETE Deletes the users profile
    @swagger.operation(
        summary="Deletes a profile",
        notes="Deletes a profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_profile_id",
                "description": "User ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 406,
                "message": "User ID / Device ID parameters not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def delete(self, user_profile_id):
        return um_profiling.delete_user_profile_by_id(user_profile_id)


api.add_resource(ProfileInstanceById, '/api/v2/um/user-profile/<string:user_profile_id>')


#
#  ProfileInstance route:
#
#     '/api/v2/um/user-profile/user/<string:user_id>/device/<string:device_id>'
#
#         GET:    get user's profile from a specific device
#         PUT:    updates profile from a specific device
#         DELETE: deletes profile from a specific device
#
class ProfileInstance(Resource):
    # GET Get Profile properties from user
    @swagger.operation(
        summary="Returns the user's profile",
        notes="Returns the user's profile",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_id",
                "description": "User ID. Example: 'testuser'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "device_id",
                "description": "Device ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, user_id, device_id):
        return um_profiling.get_user_profile(user_id, device_id)


    # PUT Updates the users profile
    @swagger.operation(
        summary="Updates a user's profile.",
        notes="Updates a user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_id",
                "description": "User ID. Example: 'testuser'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "device_id",
                "description": "Device ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"user/testuser\", "
                               "\"device_id\":\"device/50b12ccc-76fb-45a6-af7f-634312bc7ca5\", "
                               "\"resource_contributor\":false, \"service_consumer\":false, \"max_apps\":1}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 405,
                "message": "User ID / Device ID parameters not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def put(self, user_id, device_id):
        return um_profiling.update_user_profile(user_id, device_id, request.get_json())


    # DELETE Deletes the users profile
    @swagger.operation(
        summary="Deletes the user's profile",
        notes="Deletes the user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_id",
                "description": "User ID. Example: 'testuser'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "device_id",
                "description": "Device ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 406,
                "message": "User ID / Device ID parameters not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def delete(self, user_id, device_id):
        return um_profiling.delete_user_profile(user_id, device_id)


api.add_resource(ProfileInstance, '/api/v2/um/user-profile/user/<string:user_id>/profile/<string:device_id>')


#
#  Profile route:
#
#     '/api/v2/um/user-profile'
#         GET:    get "current" profile
#         PUT:
#         POST:   create new profile
#
class Profile(Resource):
    # GET Get the user profile of current device
    @swagger.operation(
        summary="Returns the current user-profile information",
        notes="Returns the current user-profile information",
        produces=["application/json"],
        authorizations=[],
        parameters=[], responseMessages=[{
        "code": 500, "message": "Exception processing request"
    }])
    def get(self):
        return um_profiling.get_current_user_profile()

    # PUT updates User Management global properties
    @swagger.operation(
        summary="updates User Management global properties",
        notes="updates User Management global properties",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>{"
                           "\"apps_running\":1}",
            "required": True,
            "paramType": "body",
            "type": "string"
    }], responseMessages=[{
        "code": 405, "message": "Parameter not found: user_id / device_id / service_consumer / resource_contributor"
    }, {
        "code": 500, "message": "Exception processing request"
    }])
    def put(self):
        return um_profiling.updateUM(request.get_json())

    # POST Initializes the users profile - User registration
    @swagger.operation(
        summary="Initializes a user's profile.",
        notes="Initializes a user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"user/testuser\", "
                               "\"device_id\":\"device/50b12ccc-76fb-45a6-af7f-634312bc7ca5\", "
                               "\"service_consumer\":true, \"resource_contributor\":false, \"max_apps\":2}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 405,
                "message": "Parameter not found: user_id / device_id / service_consumer / resource_contributor"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def post(self):
        return um_profiling.create_user_profile( request.get_json() )


api.add_resource(Profile, '/api/v2/um/user-profile')


########################################################################################################################
### SHARING MODEL
########################################################################################################################
#
#  SharingModelInstance route:
#
#     '/api/v2/um/sharing-model/user/<string:user_id>/device/<string:device_id>'
#
#         GET:
#         PUT:
#         DELETE:
#
class SharingModelInstance(Resource):
    # GET Get the user sharing model
    @swagger.operation(
        summary="Returns the user's sharing model information",
        notes="Returns the user's sharing model information",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_id",
                "description": "User ID. Example: 'testuser'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "device_id",
                "description": "Device ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, user_id, device_id):
        return um_sharing_model.get_sharing_model(user_id, device_id)    # TODO solve 'slash' problem


    # PUT Updates sharing model
    @swagger.operation(
        summary="Updates the user's shared resources values",
        notes="Updates the user's shared resources values",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_id",
                "description": "User ID. Example: 'testuser'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "device_id",
                "description": "Device ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"user_id\":\"user/testuser\", "
                           "\"device_id\":\"device/50b12ccc-76fb-45a6-af7f-634312bc7ca5\", "
                           "\"gps_allowed\": false, "
                           "\"max_cpu_usage\": 3, "
                           "\"max_memory_usage\": 3, "
                           "\"max_storage_usage\": 3, "
                           "\"max_bandwidth_usage\": 3, "
                           "\"battery_limit\": 3 }",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "User ID / Device ID parameters not found not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def put(self, user_id, device_id):
        return um_sharing_model.update_sharing_model(user_id, device_id, request.get_json())


    # DELETE Deletes the shared resources values from a user
    @swagger.operation(
        summary="Deletes the shared resources values from a user",
        notes="Deletes the shared resources values from a user",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_id",
                "description": "User ID. Example: 'testuser'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "device_id",
                "description": "Device ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
            "code": 406,
            "message": "User ID / Device ID parameters not found not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def delete(self, user_id, device_id):
        return um_sharing_model.delete_sharing_model_values(user_id, device_id)


api.add_resource(SharingModelInstance, '/api/v2/um/sharing-model/user/<string:user_id>/device/<string:device_id>')


# TODO
#
#  SharingModelInstance route:
#
#     /um/sharing-model/<string:sharing_model_id>
#
#         GET:
#         PUT:
#         DELETE:
#
class SharingModelInstanceById(Resource):
    # GET Get the user sharing model
    @swagger.operation(
        summary="Returns a sharing model information",
        notes="Returns a sharing model information",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "sharing_model_id",
                "description": "User ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, sharing_model_id):
        return um_sharing_model.get_sharing_model_by_id(sharing_model_id)


    # PUT Updates sharing model
    @swagger.operation(
        summary="Updates a sharing model",
        notes="Updates a sharing model",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "sharing_model_id",
                "description": "User ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"user_id\":\"user/testuser\", "
                           "\"device_id\":\"device/50b12ccc-76fb-45a6-af7f-634312bc7ca5\", "
                           "\"gps_allowed\": false, "
                           "\"max_cpu_usage\": 3, "
                           "\"max_memory_usage\": 3, "
                           "\"max_storage_usage\": 3, "
                           "\"max_bandwidth_usage\": 3, "
                           "\"battery_limit\": 3 }",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "User ID / Device ID parameters not found not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def put(self, sharing_model_id):
        return um_sharing_model.update_sharing_model_by_id(sharing_model_id, request.get_json())


    # DELETE Deletes a sharing model
    @swagger.operation(
        summary="Deletes a sharing model",
        notes="Deletes a sharing model",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "sharing_model_id",
                "description": "User ID. Example: '50b12ccc-76fb-45a6-af7f-634312bc7ca5'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
            "code": 406,
            "message": "User ID / Device ID parameters not found not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def delete(self, sharing_model_id):
        return um_sharing_model.delete_sharing_model_by_id(sharing_model_id)


api.add_resource(SharingModelInstanceById, '/api/v2/um/sharing-model/<string:sharing_model_id>')


#
#  SharingModel route:
#
#     '/api/v2/um/sharingmodel'
#         GET:    get "current" sharing model
#         POST:   create new sharing model
#
class SharingModel(Resource):
    # GET Get the user sharing model
    @swagger.operation(
        summary="Returns the current device/user's sharing model information",
        notes="Returns the current device/user's sharing model information",
        produces=["application/json"],
        authorizations=[],
        parameters=[], responseMessages=[{
        "code": 500, "message": "Exception processing request"
    }])
    def get(self):
        return um_sharing_model.get_current_sharing_model()

    # POST Initializes sharing model
    @swagger.operation(
        summary="Initializes the user's sharing model information",
        notes="Initializes the user's sharing model information",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>"
                               "{\"user_id\":\"user/testuser\", "
                               "\"device_id\":\"device/50b12ccc-76fb-45a6-af7f-634312bc7ca5\", "
                               "\"gps_allowed\": false, "
                               "\"max_cpu_usage\": 1, "
                               "\"max_memory_usage\": 1, "
                               "\"max_storage_usage\": 1, "
                               "\"max_bandwidth_usage\": 1, "
                               "\"battery_limit\": 55 }",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 406,
                "message": "User ID / Device ID parameters not found not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def post(self):
        return um_sharing_model.init_sharing_model( request.get_json() )


api.add_resource(SharingModel, '/api/v2/um/sharing-model')


########################################################################################################################

'''
 Assessment route:

    '/api/v2/um/assesment'

        GET:    gets the status of the current assessment in the device
        PUT:    start / stop assessment
'''
class Assessment(Resource):
    # Get process status
    # GET /api/v2/um/assesment
    @swagger.operation(
        summary="Returns the assessment process status",
        notes="Returns a json object with the information about the assessment process status",
        produces=["application/json"],
        authorizations=[],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self):
        return um_assesment.status()

    # Process operation: start / stop
    #   data: {'operation':'stop/start'}
    # PUT /api/v2/um/assesment
    @swagger.operation(
        summary="Starts / stops the assessment process",
        notes="Starts / stops the assessment process. 'operation' value (start, stop) is readed from body.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format. Options: start, stop<br/>Example: <br/>"
                               "{\"operation\":\"stop\"}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 406,
                "message": "'Operation' parameter not found"
            },{
                "code": 501,
                "message": "Operation not defined / implemented"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def put(self):
        return um_assesment.operation( request.get_json() )

api.add_resource(Assessment, '/api/v2/um/assesment')


########################################################################################################################
# MAIN
def main():
    LOG.info("USRMNGT: Starting User Management application [version=" + str(config.dic['VERSION']) + "] ...")
    LOG.info("USRMNGT: Swagger running on http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + ".html")
    LOG.info("USRMNGT: REST API running on http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'])

    # START (SSL) SERVER
    # context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    # app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=False)

    # START SERVER
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], threaded=True, debug=False)


if __name__ == "__main__":
    main()