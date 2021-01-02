import json
from typing import Any


class GrantHandler(object):
    def __init__(self, json_obj: Any):
        _json = json_obj

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
    def respond_client_credential_grant(self):
        pass

    # Handling grant request for renewing tokens.
    def respond_refresh_token_grant(self):
        pass
