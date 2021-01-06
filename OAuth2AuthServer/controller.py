import json
from flask import Flask, jsonify, request, render_template
from jinja2 import TemplateNotFound
import helper
import grant_handler
import client_reg
from urllib import parse
from typing import Dict

_app = Flask(__name__)
_helper = helper.ConfigurationSettingsLocal(source='settings.json')

# TODO: Add input-validation function to each route


@_app.route('/auth', methods=['GET'])
def get_auth():
    try:
        handler = grant_handler.GrantHandler(decode_input(jsonify(request.args).json))
        output = handler.respond_all_grant()
        return jsonify(encode_output(output))
    except TypeError as ex:
        print(ex)
        return 'type error', 400
    except Exception as ex:
        print(ex)
        return 'invalid parameter', 400


@_app.route('/auth', methods=['POST'])
def post_auth():
    try:
        handler = grant_handler.GrantHandler(decode_input(json.loads(request.data)))
        output = handler.respond_all_grant()
        return jsonify(encode_output(output))
    except Exception as ex:
        print(ex)
        return "Not valid", 400


def decode_input(json_input: json) -> Dict:
    for item in json_input:
        json_input[item] = parse.unquote_plus(json_input[item])
    return json_input


def encode_output(dict_output: Dict) -> Dict:
    for item in dict_output:
        dict_output[item] = parse.quote_plus(dict_output[item])
    return dict_output


# -------------------------- Registration process begin -------------------------
# Perform the GUI display here to avoid CORS restriction during prototyping
# TODO: In production, all registration processes need to be moved to a separated
#       website for the rule of "segregation of duty" and to avoid "backdoor".


@_app.route('/reg/gui')
def post_reg_gui():
    try:
        title = 'Client Registration'
        return render_template('index.html', title=title)
    except TemplateNotFound as ex:
        print(ex)
    except Exception as ex:
        print(ex)
        return "Not valid", 400


@_app.route('/reg/api', methods=['POST'])
def post_reg_api():
    try:
        reg_info = {'department': request.form.get('department'),
                    'scope': request.form.get('scope'),
                    'sme_name': request.form.get('sme_name'),
                    'payload_encrypt': request.form.get('payload_encrypt')}
        reg = client_reg.ClientRegistration(reg_info)
        output = reg.register_client()
        # All URL encoding/decoding should be done at controller level.
        return jsonify(encode_output(output))
    except json.JSONDecodeError as ex:
        print(ex)
    except Exception as ex:
        print(ex)
        return "Not valid", 400
# -------------------------- Registration process end ---------------------------


if __name__ == '__main__':
    _app.run(debug=True)
