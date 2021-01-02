import json
from typing import Any, Dict


class GrantHandler(object):
    def __init__(self, grant_content: Dict):
        self._grant_content = grant_content
        self._grant_response = {}

    def respond_all_grant(self) -> Any:
        try:
            if self._grant_content['grant_type'] == 'client_credentials':
                return self.respond_client_credential_grant()
            else:
                pass
        except AttributeError as ex:
            print(ex)
        except TypeError as ex:
            print(ex)
        except Exception as ex:
            print(ex)

    # Handling grant request for 3rd party authentication.
    def respond_code_grant(self):
        pass

    # Handling grant request for agent clients.
    def respond_token_grant(self):
        pass

    # Handling grant request for user's web pages.
    def respond_password_grant(self):
        pass

    # Handling grant request for machine-to-machine (M2M).
    def respond_client_credential_grant(self) -> Any:
        self._grant_response = {"token_type": "Bearer"}
        return self._grant_response

    # Handling grant request for renewing tokens.
    def respond_refresh_token_grant(self):
        pass
