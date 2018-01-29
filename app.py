"""
REST API
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python

import src.modules.um_profiling as um_profiling
import src.modules.um_sharing_model as um_sharing_model
import src.modules.um_assesment as um_assesment
import src.utils.auth as auth
import config
from src.utils.logs import LOG
from flask_cors import CORS
from flask import Flask, request, Response, json
from flask_restful import Resource, Api
from flask_restful_swagger import swagger


try:
    # TODO get vars from ENV
    # CONFIGURATION values
    LOG.info('[SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
    LOG.info('[API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
    LOG.info('[CERT_CRT=' + config.dic['CERT_CRT'] + ']')
    LOG.info('[CERT_KEY=' + config.dic['CERT_KEY'] + ']')
    LOG.info('[DEBUG=' + str(config.dic['DEBUG']) + ']')

    # CIMI URL
    CIMI_API_ENV_NAME = "CIMI_API"
    CIMI_API_ENV_VALUE = "http://...."

    # APP
    app = Flask(__name__)
    CORS(app)

    # API DOC
    api = swagger.docs(Api(app),
                       apiVersion='1.0',
                       api_spec_url=config.dic['API_DOC_URL'],
                       produces=["application/json", "text/html"],
                       swaggerVersion="1.2",
                       description='User Management component REST API - mF2C',
                       basePath='http://localhost:' + str(config.dic['SERVER_PORT']),
                       resourcePath='/')
except ValueError:
    LOG.error('ERROR')


###############################################################################
## API Route
###############################################################################
@app.route('/api/v1/', methods=['GET'])
@auth.requires_auth # test basic auth
def default_route():
    data = {
        'app': 'User Management Module REST API',
        'status': 'Running',
        'api_doc_json': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
        'api_doc_html': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + '.html#!/spec'
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


###############################################################################
## Profiling
###############################################################################
class GetProfiling(Resource):
    # Get Profile properties from user
    @swagger.operation(
        summary="Returns the user's profile",
        notes="Returns the user's profile",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_id",
                "description": "User ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, user_id):
        return um_profiling.get_profiling(user_id)


class Profiling(Resource):
    # Initializes the users profile - User registration
    @swagger.operation(
        summary="Initializes a user's profile.",
        notes="Initializes a user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"123asdf123\", "
                               "\"email\":\"...\", \"name\":\"...\"}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 405,
                "message": "Parameter not found: user_id / email"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def post(self):
        return um_profiling.register_user( request.get_json() )

    # Updates the users profile
    @swagger.operation(
        summary="Updates a user's profile.",
        notes="Updates a user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"123asdf123\", "
                               "\"email\":\"...\", \"service_consumer\":\"...\" ...}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 405,
                "message": "User ID parameter not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def put(self):
        return um_profiling.update_profile( request.get_json() )

    # Deletes the users profile
    @swagger.operation(
        summary="Deletes the user's profile",
        notes="Deletes the user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"123asdf123\"}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 406,
                "message": "User ID parameter not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def delete(self):
        return um_profiling.delete_profile( request.get_json() )


api.add_resource(Profiling, '/api/v1/user-management/profiling/')
api.add_resource(GetProfiling, '/api/v1/user-management/profiling/<string:user_id>')


###############################################################################
## Assessment
###############################################################################
class Assessment(Resource):
    # Get process status
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


api.add_resource(Assessment, '/api/v1/user-management/assesment')


###############################################################################
## Sharing Model
###############################################################################
class GetSharingModel(Resource):
    # Get the user sharing model
    @swagger.operation(
        summary="Returns the user's sharing model information",
        notes="Returns the user's sharing model information",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "user_id",
                "description": "User ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, user_id):
        return um_sharing_model.get_sharing_model_values(user_id)


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
                               "{\"user_id\":\"123asdf123\", "
                               "\"max_apps\": \"integer\", "
                               "\"GPS_allowed\": \"boolean\", "
                               "\"max_CPU_usage\": \"integer\", "
                               "\"max_memory_usage\": \"integer\", "
                               "\"max_storage_usage\": \"integer\", "
                               "\"max_bandwidth_usage\": \"integer\", "
                               "\"battery_limit\": \"integer\" }",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 406,
                "message": "User ID parameter not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def post(self):
        return um_sharing_model.init_sharing_model( request.get_json() )

    # Updates sharing model
    @swagger.operation(
        summary="Updates the user's shared resources values",
        notes="Updates the user's shared resources values",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>"
                               "{\"user_id\":\"123asdf123\", "
                               "\"max_apps\": \"integer\", "
                               "\"GPS_allowed\": \"boolean\", "
                               "\"max_CPU_usage\": \"integer\", "
                               "\"max_memory_usage\": \"integer\", "
                               "\"max_storage_usage\": \"integer\", "
                               "\"max_bandwidth_usage\": \"integer\", "
                               "\"battery_limit\": \"integer\" }",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 406,
                "message": "User ID parameter not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def put(self):
        return um_sharing_model.update_sharing_model_values( request.get_json() )

    # Deletes the shared resources values from a user
    @swagger.operation(
        summary="Deletes the shared resources values from a user",
        notes="Deletes the shared resources values from a user",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"123asdf123\"}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }],
        responseMessages=[{
                "code": 406,
                "message": "User ID parameter not found"
            },{
                "code": 500,
                "message": "Exception processing request"
            }])
    def delete(self):
        return um_sharing_model.delete_sharing_model_values( request.get_json() )


api.add_resource(SharingModel, '/api/v1/user-management/sharingmodel')
api.add_resource(GetSharingModel, '/api/v1/user-management/sharingmodel/<string:user_id>')


###############################################################################

def main():
    # get CIMI_API_ENV_VALUE from env
    # CIMI_API_ENV_VALUE = os.environ.get(CIMI_API_ENV_NAME, '...')
    # logs.info('[CIMI_API_ENV_VALUE=' + CIMI_API_ENV_VALUE + ']')
    # START SERVER
    context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=config.dic['DEBUG'])


if __name__ == "__main__":
    main()
