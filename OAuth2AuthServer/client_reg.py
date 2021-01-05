import sys
import uuid
from typing import Dict
import client_repo


class ClientRegistration(object):
    def __init__(self):
        self._reg_info = {}

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
