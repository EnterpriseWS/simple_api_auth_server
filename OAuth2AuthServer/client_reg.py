import sys
import uuid
from typing import Dict
import client_repo
import auth_repo
import datetime


class ClientRegistration(object):
    def __init__(self):
        self._reg_info = {}
        self._client_repo_data = {}
        self._auth_repo_data = {}

    def set_eff_datetime(self, eff_datetime: datetime):
        pass

    def register_client(self, reg_info: Dict) -> Dict:
        # {'department': request.form.get('department'),
        # 'scope': request.form.get('scope'),
        # 'sme': request.form.get('sme'),
        # 'payload_encrypt': request.form.get('payload_encrypt')}
        self._reg_info = reg_info
        client_uuid = uuid.uuid4()
        db_op = client_repo.ClientRepositoryOp()

    def get_client_reg_info(self):
        pass
