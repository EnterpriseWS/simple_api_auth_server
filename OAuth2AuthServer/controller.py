import json
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from jinja2 import TemplateNotFound
import helper
import grant_handler
import client_reg
from urllib import parse
from typing import Dict

app = FastAPI()
_helper = helper.ConfigurationSettingsLocal(source='settings.json')

# TODO: Add input-validation function to each route


@app.route('/auth', methods=['GET'])
async def get_auth():
    try:
        handler = grant_handler.GrantHandler(decode_input(jsonable_encoder(Request.args).json))
        output = handler.respond_all_grant()
        return jsonable_encoder(encode_output(output))
    except TypeError as ex:
        print(ex)
        return 'type error', 400
    except Exception as ex:
        print(ex)
        return 'invalid parameter', 400


@app.route('/auth', methods=['POST'])
async def post_auth():
    try:
        handler = grant_handler.GrantHandler(decode_input(json.loads(Request.data)))
        output = handler.respond_all_grant()
        return jsonable_encoder(encode_output(output))
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


@app.get('/reg/gui', response_class=HTMLResponse)
async def get_reg_gui(request: Request):
    try:
        title = 'Client Registration'
        templates = Jinja2Templates(directory="templates")
        return templates.TemplateResponse('index.html', {'request': request, 'title': title})
    except TemplateNotFound as ex:
        print(ex)
    except Exception as ex:
        print(ex)
        return "Not valid", 400


@app.post('/reg/api')
async def post_reg_api(request: Request):
    try:
        form_data = await request.form()
        reg_info = {'department': form_data.get('department'),
                    'scope': form_data.get('scope'),
                    'sme_name': form_data.get('sme_name'),
                    'payload_encrypt': form_data.get('payload_encrypt')}
        reg = client_reg.ClientRegistration(reg_info)
        output = reg.register_client()
        # All URL encoding/decoding should be done at controller level.
        encoded_output = encode_output(output)
        encoded_return_value = jsonable_encoder(encoded_output)
        return encoded_return_value
    except json.JSONDecodeError as ex:
        print(ex)
    except Exception as ex:
        print(ex)
        return "Not valid", 400
# -------------------------- Registration process end ---------------------------


if __name__ == '__main__':
    uvicorn.run('controller:app', port=8000, log_level='info', reload=False)