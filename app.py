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
import src.utils.logs as logs
import src.utils.auth as auth
import config

from flask_cors import CORS
from flask import Flask, request, Response, json
from flask_restful import Resource, Api
from flask_restful_swagger import swagger


try:
    # CONFIGURATION values
    logs.info('[SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
    logs.info('[API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
    logs.info('[CERT_CRT=' + config.dic['CERT_CRT'] + ']')
    logs.info('[CERT_KEY=' + config.dic['CERT_KEY'] + ']')

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
    logs.error('ERROR')


# 'home' Route
@app.route('/api/v1/', methods=['GET'])
@auth.requires_auth # to test basic auth
def default_route():
    data = {
        'app': 'User Management Module REST API',
        'status': 'Running',
        'api_doc_json': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
        'api_doc_html': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + '.html#!/spec'
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


# Assessment Route
class Assessment(Resource):
    @swagger.operation(
        summary="Returns the assessment process status",
        notes="Returns a json object with the information about the assessment process status",
        produces=["application/json"],
        authorizations=[]
    )
    def get(self):
        return um_assesment.status()

    @swagger.operation(
        summary="Starts / stops the assessment process",
        notes="Starts / stops the assessment process. 'operation' value (start, stop) is readed from body.",
        produces=["application/json"],
        authorizations=[],
        parameters=[
            {
                "name": "body",
                "description": "Parameters in JSON format. Options: start, stop<br/>Example: <br/>"
                               "{\"operation\":\"stop\"}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }
        ],
        responseMessages=[
            {
                "code": 406,
                "message": "Operation not found"
            },
            {
                "code": 501,
                "message": "Operation not defined / implemented"
            }
        ]
    )
    def put(self):
        data = request.get_json()

        if 'operation' not in data:
            logs.error('Error (rest_api.py - Assessment) : PUT : operation not found')
            return Response(json.dumps({'error': 'operation not found'}), status=406, content_type='application/json')

        if data['operation'] == 'start':
            return um_assesment.start()

        elif data['operation'] == 'stop':
            return um_assesment.stop()

        else:
            logs.error('Error (rest_api.py - Assessment) : PUT : operation not defined / implemented')
            return Response(json.dumps({'error': 'operation not defined / implemented'}),
                            status=501,
                            content_type='application/json')


api.add_resource(Assessment, '/api/v1/user-management/assesment')


# Profiling Route
class Profiling(Resource):
    @swagger.operation(
        summary="Initializes a user's profile.",
        notes="Initializes a user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[
            {
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"123asdf123\", "
                               "\"email\":\"...\", \"name\":\"...\"}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }
        ],
        responseMessages=[
            {
                "code": 406,
                "message": "Parameter not found: user_id / email / name"
            }
        ])
    def post(self):
        data = request.get_json()
        return um_profiling.userRegistration(data)

    @swagger.operation(
        summary="Updates a user's profile.",
        notes="Updates a user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[
            {
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"123asdf123\", "
                               "\"email\":\"...\", \"service_consumer\":\"...\" ...}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }
        ],
        responseMessages=[
            {
                "code": 406,
                "message": "User ID not found"
            }
        ])
    def put(self):
        data = request.get_json()
        return um_profiling.updateProfiling(data)

    @swagger.operation(
        summary="Deletes the user's profile",
        notes="Deletes the user's profile.",
        produces=["application/json"],
        authorizations=[],
        parameters=[
            {
                "name": "body",
                "description": "Parameters in JSON format.<br/>Example: <br/>{\"user_id\":\"123asdf123\"}",
                "required": True,
                "paramType": "body",
                "type": "string"
            }
        ],
        responseMessages=[
            {
                "code": 406,
                "message": "User ID not found"
            }
        ])
    def delete(self):
        data = request.get_json()
        return um_profiling.deleteProfile(data)


api.add_resource(Profiling, '/api/v1/user-management/profiling/')


# GetProfiling Route
class GetProfiling(Resource):
    @swagger.operation(
        summary="Returns the user's profile",
        notes="Returns the user's profile",
        produces=["application/json"],
        authorizations=[],
        parameters=[
            {
                "name": "user_id",
                "description": "User ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            }
        ]
    )
    def get(self, user_id):
        return um_profiling.getProfiling(user_id)


api.add_resource(GetProfiling, '/api/v1/user-management/profiling/<string:user_id>')


# SharingModel Route
class SharingModel(Resource):
    @swagger.operation(
        summary="Returns the user's sharing model information",
        notes="Returns the user's sharing model information",
        produces=["application/json"],
        authorizations=[],
        parameters=[
            {
                "name": "user_id",
                "description": "User ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            }
        ]
    )
    def get(self, user_id):
        return um_sharing_model.getSharingModelValues(user_id)

    @swagger.operation(
        summary="Initializes the user's sharing model information",
        notes="Initializes the user's sharing model information",
        produces=["application/json"],
        authorizations=[],
        parameters=[
            {
                "name": "user_id",
                "description": "User ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            },
            {
                "name": "body",
                "description": "...",
                "required": True,
                "paramType": "body",
                "type": "string"
            }
        ])
    def post(self, user_id):
        data = request.get_json()
        return um_sharing_model.initSharingModelValues(user_id, data)

    @swagger.operation(
        summary="Updates the user's shared resources values",
        notes="Updates the user's shared resources values",
        produces=["application/json"],
        authorizations=[],
        parameters=[
            {
                "name": "user_id",
                "description": "User ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            },
            {
                "name": "body",
                "description": "...",
                "required": True,
                "paramType": "body",
                "type": "string"
            }
        ])
    def put(self, user_id):
        data = request.get_json()
        return um_sharing_model.updateSharingModelValues(user_id, data)

    @swagger.operation(
        summary="Deletes the shared resources values from a user",
        notes="Deletes the shared resources values from a user",
        produces=["application/json"],
        authorizations=[],
        parameters=[
            {
                "name": "user_id",
                "description": "User ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            },
            {
                "name": "body",
                "description": "...",
                "required": True,
                "paramType": "body",
                "type": "string"
            }
        ])
    def delete(self, user_id):
        return um_sharing_model.deleteSharingModelValues(user_id)


api.add_resource(SharingModel, '/api/v1/user-management/sharingmodel/<string:user_id>')


def main():
    # get CIMI_API_ENV_VALUE from env
    # CIMI_API_ENV_VALUE = os.environ.get(CIMI_API_ENV_NAME, '...')
    # logs.info('[CIMI_API_ENV_VALUE=' + CIMI_API_ENV_VALUE + ']')
    # START SERVER
    context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=True)


if __name__ == "__main__":
    main()
