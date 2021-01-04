import json
from flask import Flask, jsonify, request, render_template
from jinja2 import TemplateNotFound
import helper
import grant_handler
import client_reg

_app = Flask(__name__)
_helper = helper.ConfigurationSettingsLocal(source='settings.json')

# TODO: Add input-validation function to each route


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
    except Exception as ex:
        print(ex)
        return "Not valid", 400

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
                    'sme': request.form.get('sme'),
                    'payload_encrypt': request.form.get('payload_encrypt')}
        return jsonify(reg_info)
    except json.JSONDecodeError as ex:
        print(ex)
    except Exception as ex:
        print(ex)
        return "Not valid", 400
# -------------------------- Registration process end ---------------------------


if __name__ == '__main__':
    _app.run(debug=True)
