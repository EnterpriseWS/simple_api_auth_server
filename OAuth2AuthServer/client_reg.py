import sys
import uuid
from typing import Dict
import client_repo
import auth_repo
from datetime import datetime, timedelta
import access_token
from urllib import parse


class ClientRegistration(object):
    def __init__(self, reg_info: Dict = None):
        self._reg_info = reg_info
        self._client_repo_data = {}

    def register_client(self) -> Dict:
        try:
            client_repo.ClientRepositoryOp()
            client_uuid = str(uuid.uuid4())
            token = access_token.AccessTokenJwt()
            keys = token.generate_rsa_keys()
            eff_date = datetime.now()
            exp_date = datetime.now() + timedelta(days=365)
            db_op = client_repo.ClientRepositoryOp()
            db_op.write(client_uuid,
                        self._reg_info['department'],
                        self._reg_info['scope'],
                        self._reg_info['sme_name'],
                        keys['public_key'],
                        eff_date,
                        exp_date)
            self._client_repo_data = db_op.read(client_uuid)
            token.save_all_keys(self._client_repo_data['id'],
                                self._client_repo_data['eff_date'],
                                self._client_repo_data['exp_date'])
            client_secret = token.assemble_jwt({'kid': client_uuid},
                                               {'scope': self._client_repo_data['scope'],
                                                'nbf': eff_date.timestamp(),
                                                'exp': exp_date.timestamp(),
                                                'enc': self._reg_info['payload_encrypt']})
            return {'client_secret': parse.quote_plus(client_secret),
                    'public_key': parse.quote_plus(keys['public_key'])}
        except Exception as ex:
            print(ex)

    def set_eff_datetime(self, eff_datetime: datetime):
        pass

    def get_client_reg_info(self):
        pass
