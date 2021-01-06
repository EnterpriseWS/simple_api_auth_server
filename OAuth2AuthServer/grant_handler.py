import json
from typing import Any, Dict
import client_repo
import access_token
import jwt
from datetime import datetime, timedelta
import base64

JWT_MIN_LEN = 5 # 2 dots and 3 letters
JWT_MAX_LIVE = 30 # token maximum live time
RESPONSE_TEMPLATE_CLIENT_CREDENTIAL = {'token_type': 'Bearer',
                                       'expires_in': 0,
                                       'access_token': ''}
RESPONSE_TEMPLATE_REFRESH_TOKEN = {'token_type': 'Bearer',
                                   'expires_in': 0,
                                   'access_token': '',
                                   'refresh_token': ''}
# TODO: Needs to setup the template of other grant types.


class GrantHandler(object):
    def __init__(self, grant_content: Dict):
        self._grant_content = grant_content
        self._grant_response = {}

    def respond_all_grant(self) -> Any:
        try:
            if self._grant_content['grant_type'] == 'client_credentials':
                payload = None
                if self._grant_content['payload'] is not None:
                    payload = json.loads(base64.b64decode(self._grant_content['payload']))
                return self.respond_client_credential_grant(payload)
            else:
                pass
        except AttributeError as ex:
            print(ex)
        except TypeError as ex:
            print(ex)
        except Exception as ex:
            print(ex)

    # Handling grant request for 3rd party authentication.
    def respond_code_grant(self, payload: Dict = None):
        pass

    # Handling grant request for agent clients.
    def respond_token_grant(self, payload: Dict = None):
        pass

    # Handling grant request for user's web pages.
    def respond_password_grant(self, payload: Dict = None):
        pass

    # Handling grant request for machine-to-machine (M2M).
    def respond_client_credential_grant(self, payload: Dict = None) -> Dict:
        self._grant_response = RESPONSE_TEMPLATE_CLIENT_CREDENTIAL
        client_uuid = self._grant_content['client_id']
        verified = False
        try:
            if client_uuid is not None:
                repo = client_repo.ClientRepositoryOp()
                repo_info = repo.read(client_uuid)
                client_secret = self._grant_content['client_secret']
                if client_secret is not None and len(client_secret) > JWT_MIN_LEN:
                    ''' For security consideration and minimize database access,
                        use jwt library directly without using access_token.py'''
                    claims = jwt.decode(client_secret, repo_info['current_pubkey'], algorithms='RS256', verify=True)
                    if len(claims) > 0:
                        # TODO: Verify if the client_uuid matches the value of "kid" within jwt token.
                        token = access_token.AccessTokenJwt()
                        token.get_private_key(repo_info['id'])
                        # TODO: If value of "enc" is "True", payload of JWT token needs to be encrypted.
                        nbf = datetime.now().timestamp()
                        exp = (datetime.now() + timedelta(minutes=JWT_MAX_LIVE)).timestamp()
                        actual_payload = {'scope': repo_info['scope'],
                                          'nbf': nbf,
                                          'exp': exp}
                        if payload is not None:
                            for item in payload:
                                # Unconditionally overwrite the value if the item already exists.
                                actual_payload[item] = payload[item]
                        self._grant_response['expires_in'] = str(exp)
                        self._grant_response['access_token'] = \
                            token.assemble_jwt({'kid': client_uuid}, actual_payload)
            return self._grant_response
        except jwt.InvalidSignatureError as ex:
            print(ex)
        except Exception as ex:
            print(ex)

    # Handling grant request for renewing tokens.
    def respond_refresh_token_grant(self, payload: Dict = None):
        pass
