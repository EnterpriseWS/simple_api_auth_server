import sys
import uuid
from typing import Dict
import client_repo


class ClientRegistration(object):
    def __init__(self, reg_info: Dict):
        self._reg_info = reg_info

    def register_client(self) -> Dict:
        # {'department': request.form.get('department'),
        # 'scope': request.form.get('scope'),
        # 'sme': request.form.get('sme'),
        # 'payload_encrypt': request.form.get('payload_encrypt')}
        db_op = client_repo.ClientRepositoryOp()
        client_uuid = uuid.uuid4()


class ClientSecret(object):
    def __int__(self, client_uuid: str):
        self._client_uuid = client_uuid
        self._client_private_key = ''
        self._client_public_key = ''

    def create_client_secret(self) -> str:
        pass

    def create_client_access_token(self):
        pass

    def create_client_secret_keys(self) -> None:
        pass

    def save_client_secret_keys(self) -> None:
        pass
