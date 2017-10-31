'''
REST API
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python3
import sys
import um_profiling, um_sharing_model, um_assesment

from flask import Flask, request, Response, json
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


@app.route('/api/', methods=['GET'])
def default_route():
    data = {
        'app': 'User Management Module REST API',
        'status': 'Running'
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


# Assesment process
@app.route('/api/assesment-process', methods=['GET', 'POST', 'DELETE'])
def assesment_process():
    data = {}
    if request.method == 'GET':
        data = um_assesment.status()
    elif request.method == 'POST':
        data = um_assesment.start()
    elif request.method == 'DELETE':
        data = um_assesment.stop()
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


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

api.add_resource(Profiling, '/api/profiling/<string:user_id>')


# SharingModel Route
class SharingModel(Resource):
    def get(self):
        return um_sharing_model.getSharingModel()

    def post(self):
        data = request.get_json()
        return um_sharing_model.initSharingModel(data)

    def put(self):
        data = request.get_json()
        return um_sharing_model.updateSharingModel(data)

api.add_resource(SharingModel, '/api/sharingmodel')


# def main():
#     try:
#         total = len(sys.argv)
#         cmdargs = str(sys.argv)
#         print("> The total numbers of args passed to the script: %d " % total)
#         print("> Args list: %s " % cmdargs)
#         print("> Script name: %s" % str(sys.argv[0]))
#         print("> Starting server in port " + sys.argv[1] + " ...")
#         app.run(host='0.0.0.0', port=sys.argv[1])
#     except:
#         print("> Starting server in default port 5002 ...")
#         app.run(host='0.0.0.0', port='5002')


def main():
    app.run(host='0.0.0.0', debug=True)



if __name__ == "__main__":
    main()
