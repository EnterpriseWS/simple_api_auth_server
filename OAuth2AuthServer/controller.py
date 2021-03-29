from typing import Any
import json
import time
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


@app.middleware('http')
async def check_connection(request: Request, call_next):
    start_time = time.time()
    # TODO: Insert some logic here before any request begins
    response = await call_next(request)
    # TODO: Insert some logic here before any response returns
    end_time = time.time()
    return response


@app.get('/auth')
async def get_auth(grant_type: str,
                   client_id: str,
                   client_secret: str,
                   scope: str,
                   payload: str):
    try:
        request_dict = {'grant_type': grant_type,
                        'client_id': client_id,
                        'client_secret': client_secret,
                        'scope': scope,
                        'payload': payload}
        return await generate_auth(request_dict)
    except TypeError as ex:
        print(ex)
        return 'type error', 401
    except Exception as ex:
        print(ex)
        return 'invalid parameter', 400


@app.post('/auth')
async def post_auth(request: Request):
    try:
        request_dict = await request.json()
        return await generate_auth(request_dict)
    except TypeError as ex:
        print(ex)
        return 'type error', 401
    except Exception as ex:
        print(ex)
        return "Not valid", 400


async def generate_auth(request_dict: Dict) -> Any:
    handler = grant_handler.GrantHandler(decode_input(request_dict))
    output = handler.respond_all_grant()
    return jsonable_encoder(encode_output(output))


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
        return jsonable_encoder(encoded_output)
    except json.JSONDecodeError as ex:
        print(ex)
    except Exception as ex:
        print(ex)
        return "Not valid", 400
# -------------------------- Registration process end ---------------------------


if __name__ == '__main__':
    # Assign reload=False to avoid uvicorn detecting SQLite file change
    uvicorn.run('controller:app', port=8000, log_level='info', reload=False)
