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
                /um/profiling/
                        POST:
                /um/profiling/<string:user_id>/<string:device_id>
                        GET:    get user's profile
                        PUT:    updates profile
                        DELETE: deletes profile
                /um/profile-services/<string:user_id>/<string:device_id>
                        GET:    get allowed services (not implemented !)
                /um/sharingmodel
                        POST:
                /um/sharingmodel/<string:user_id>/<string:device_id>
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
                       description='mF2C - User Management REST API',
                       basePath='http://localhost:' + str(config.dic['SERVER_PORT']),
                       resourcePath='/')
except ValueError:
    LOG.error('User-Management: app: Exception: Error while initializing app / api')


'''
 API 'home' Route

    '/api/v2/'
    
        GET:    get rest api service status
'''
@app.route('/api/v2/', methods=['GET'])
def default_route():
    data = {
        'app': 'User Management modules REST API',
        'status': 'Running',
        'api_doc_json': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
        'api_doc_html': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + '.html#!/spec'
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


########################################################################################################################
### USER MANAGEMENT
########################################################################################################################
'''
 ProfileInstance route: gets user's profile

    '/api/v2/um/profiling/<string:user_id>/<string:device_id>'

        GET:       Gets the user's profile from a device
        PUT:
        DELETE:
'''
class ProfileInstance(Resource):
    # Get Profile properties from user
    # GET /api/v2/um/profiling/<string:user_id>/<string:device_id>
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
                "description": "Device ID. Example: 'testdevice'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, user_id):
        return um_profiling.get_profiling(user_id)    # TODO solve 'slash' problem


    # Updates the users profile
    # PUT /api/v2/um/profiling/<string:user_id>/<string:device_id>
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
                "description": "Device ID. Example: 'testdevice'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"testuser\", "
                               "\"resource_contributor\":false, \"service_consumer\":false}",
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
    def put(self, user_id):
        return um_profiling.update_profile(user_id, request.get_json())


    # Deletes the users profile
    # DELETE /api/v2/um/profiling/<string:user_id>/<string:device_id>
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
                "description": "Device ID. Example: 'testdevice'",
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
    def delete(self, user_id):
        return um_profiling.delete_profile(user_id)

api.add_resource(ProfileInstance, '/api/v2/um/profiling/<string:user_id>/<string:device_id>')


'''
 Profile route:

    '/api/v2/um/profiling'

        POST:       Creates a new profile
'''
class Profile(Resource):
    # Initializes the users profile - User registration
    # POST /api/v2/um/profiling
    @swagger.operation(
        summary="Initializes a user's profile.",
        notes="Initializes a user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"testuser\", \"device_id\":\"testdevice\", "
                               "\"service_consumer\":true, \"resource_contributor\":false}",
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
        return um_profiling.register_user( request.get_json() )

api.add_resource(Profile, '/api/v2/um/profiling/')


'''
TODO
 ProfileServices route:

    '/api/v2/um/profile-services/<string:user_id>/<string:device_id>'

        GET:    Gets allowed services for user and device
'''
class ProfileServices(Resource):
    # Get Profile properties from user
    @swagger.operation(
        summary="Returns the user's allowed services",
        notes="Returns the user's allowed services",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_id",
                "description": "User ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
                "name": "device_id",
                "description": "Device ID. Example: 'testdevice'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, user_id):
        return um_profiling.get_services(user_id)

# TODO IT-2:
#api.add_resource(ProfileServices, '/api/v2/um/profile-services/<string:user_id>/<string:device_id>')


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


'''
 SharingModelInstance route:

    '/api/v2/um/sharingmodel/<string:user_id>/<string:device_id>'

        GET:    
        PUT:    
        DELETE:
'''
class SharingModelInstance(Resource):
    # Get the user sharing model
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
                "description": "Device ID. Example: 'testdevice'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, user_id):
        return um_sharing_model.get_sharing_model(user_id)    # TODO solve 'slash' problem


    # Updates sharing model
    # PUT /api/v2/um/sharingmodel/<string:user_id>/<string:device_id>
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
                "description": "Device ID. Example: 'testdevice'",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"user_id\":\"testuser\", "
                           "\"device_id\":\"testdevice\", "
                           "\"max_apps\": 2, "
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
    def put(self, user_id):
        return um_sharing_model.update_sharing_model(user_id, request.get_json())


    # Deletes the shared resources values from a user
    # DELETE /api/v2/um/sharingmodel/<string:user_id>/<string:device_id>
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
                "description": "Device ID. Example: 'testdevice'",
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
    def delete(self, user_id):
        return um_sharing_model.delete_sharing_model_values(user_id)

api.add_resource(SharingModelInstance, '/api/v2/um/sharingmodel/<string:user_id>/<string:device_id>')


'''
 SharingModel route:

    '/api/v2/um/sharingmodel'

        POST:
'''
class SharingModel(Resource):
    # Initializes sharing model
    @swagger.operation(
        summary="Initializes the user's sharing model information",
        notes="Initializes the user's sharing model information",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>"
                               "{\"user_id\":\"testuser\", "
                               "\"device_id\":\"testdevice\", "
                               "\"max_apps\": 2, "
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
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def post(self):
        return um_sharing_model.init_sharing_model( request.get_json() )

api.add_resource(SharingModel, '/api/v2/um/sharingmodel')


########################################################################################################################
# MAIN
def main():
    LOG.info("Starting User Management application [version=" + str(config.dic['VERSION']) + "] ...")
    LOG.info("Swagger running on http://localhost:" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + ".html")
    LOG.info("REST API running on http://localhost:" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'])

    # START (SSL) SERVER
    # context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    # app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=False)

    # START SERVER
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], threaded=True, debug=False)


if __name__ == "__main__":
    main()