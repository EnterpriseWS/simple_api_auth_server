import json
from flask import Flask, jsonify, request
import helper

_app = Flask(__name__)
_helper = helper.ConfigurationSettingsLocal(source='settings.json')


@_app.route('/auth', methods=['GET'])
def get_auth():
    grant_type = request.args.get('grant_type')
    if grant_type == 'client_credentials':
        return jsonify({'grant_type': 'Got it'})


@_app.route('/auth', methods=['POST'])
def post_auth():
    grant_type = (json.loads(request.data))['grant_type']
    if grant_type == 'client_credentials':
        return jsonify({'grant_type': 'Got it2'})


if __name__ == '__main__':
    _app.run(debug=True)
