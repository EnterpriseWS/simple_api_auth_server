import sys
import json
from typing import Any
from flask import Flask, jsonify, request
import helper
import grant_handler

_app = Flask(__name__)
_helper = helper.ConfigurationSettingsLocal(source='settings.json')


def convert_query_string_to_json(args: Any) -> Any:
    return jsonify(args)


@_app.route('/auth', methods=['GET'])
def get_auth():
    try:
        grant_type = request.args.get('grant_type')
        handler = grant_handler.GrantHandler(convert_query_string_to_json(request.args))
        if grant_type == 'client_credentials':
            return handler.respond_client_credential_grant()
    except Exception:
        return "Not valid", 400


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
