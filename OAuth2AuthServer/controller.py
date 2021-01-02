import sys
import json
from typing import Any
from flask import Flask, jsonify, request
import helper
import grant_handler

_app = Flask(__name__)
_helper = helper.ConfigurationSettingsLocal(source='settings.json')


@_app.route('/auth', methods=['GET'])
def get_auth():
    try:
        grant_content = jsonify(request.args).json
        handler = grant_handler.GrantHandler(grant_content)
        return jsonify(handler.respond_all_grant())
    except TypeError as ex:
        print(ex)
        return 'type error', 400
    except Exception as ex:
        print(ex)
        return 'invalid parameter', 400


@_app.route('/auth', methods=['POST'])
def post_auth():
    try:
        grant_type = (json.loads(request.data))['grant_type']
        if grant_type == 'client_credentials':
            return jsonify({'grant_type': 'Got it2'})
    except Exception:
        return "Not valid", 400


if __name__ == '__main__':
    _app.run(debug=True)
