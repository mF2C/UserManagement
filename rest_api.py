'''
REST API
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python

import src.um_profiling as um_profiling
import src.um_sharing_model as um_sharing_model
import src.um_assesment as um_assesment
import os
import logs

from flask import Flask, request, Response, json
from flask_restful import Resource, Api

#CIMI_API_ENV_NAME = "CIMI_API"
#CIMI_API_ENV_VALUE = "http://...."

app = Flask(__name__)
api = Api(app)


# 'home' Route
@app.route('/api/v1/', methods=['GET'])
def default_route():
    data = {
        'app': 'User Management Module REST API',
        'status': 'Running'
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


# Assessment Route
# 'data' from request (body) - content:
#   {
#       "operation": "stop"
#   }
class Assessment(Resource):
    def get(self):
        return um_assesment.status()

    # stop / start
    def put(self):
        data = request.get_json()
        if 'operation' not in data:
            logs.error('Error (rest_api.py - Assessment) : PUT : operation not found')
            return Response(json.dumps({'error': 'operation not found'}), status=406, content_type='application/json')
        # operations
        if data['operation'] == 'start':
            return um_assesment.start()
        elif data['operation'] == 'stop':
            return um_assesment.stop()
        else:
            logs.error('Error (rest_api.py - Assessment) : PUT : operation not defined / implemented')
            return Response(json.dumps({'error': 'operation not defined / implemented'}), status=501,
                            content_type='application/json')

api.add_resource(Assessment, '/api/v1/user-management/assesment')


# Profiling Route
class Profiling(Resource):
    def get(self, user_id):
        return um_profiling.getProfiling(user_id)

    def post(self, user_id):
        data = request.get_json()
        return um_profiling.userRegistration(user_id, data)

    def put(self, user_id):
        data = request.get_json()
        return um_profiling.updateProfiling(user_id, data)

    def delete(self, user_id):
        data = request.get_json()
        return um_profiling.deleteProfile(user_id, data)

api.add_resource(Profiling, '/api/v1/user-management/profiling/<string:user_id>')


# SharingModel Route
class SharingModel(Resource):
    def get(self, user_id):
        return um_sharing_model.getSharingModelValues(user_id)

    def post(self, user_id):
        data = request.get_json()
        return um_sharing_model.initSharingModelValues(user_id, data)

    def put(self, user_id):
        data = request.get_json()
        return um_sharing_model.updateSharingModelValues(user_id, data)

    def delete(self, user_id):
        return um_sharing_model.deleteSharingModelValues(user_id)

api.add_resource(SharingModel, '/api/v1/user-management/sharingmodel/<string:user_id>')



def main():
    # get CIMI_API_ENV_VALUE from env
    #CIMI_API_ENV_VALUE = os.environ.get(CIMI_API_ENV_NAME, '...')
    #logs.info('[CIMI_API_ENV_VALUE=' + CIMI_API_ENV_VALUE + ']')
    # start server
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    main()
