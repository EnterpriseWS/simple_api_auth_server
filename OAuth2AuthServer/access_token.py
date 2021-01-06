from typing import Any, Dict
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from datetime import datetime
import auth_repo
import jwt


class AccessTokenJwt(object):
    def __init__(self, client_id: int = 0):
        self._private_key = None
        self._public_key = None

    def assemble_jwt(self, headers: Dict, payload: Dict, payload_encrypt: bool = False) -> str:
        # NOTE: Currently the payload encryption is disabled.
        # TODO: Add payload encryption to the later version.
        try:
            jwt_str = jwt.encode(payload, self._private_key, algorithm='RS256', headers=headers)
            # TODO: Determine if it is needed to validate the token before returning it.
            # verified_str = jwt.decode(jwt_str, self._public_key, algorithms='RS256', verify=True)
            return jwt_str
        except AttributeError as ex:
            print(ex)
            raise ex
        except Exception as ex:
            print(ex)
            raise ex

    # TODO: Mark the method below as restricted use when it is necessary.
    def verify_jwt(self, jwt_str: str, public_key: str = None, client_id: int = 0) -> bool:
        verified = False
        try:
            if client_id > 0 and public_key is None:
                public_key = self.get_public_key(client_id)
            if len(jwt_str) > 5 and public_key is not None:
                claims = jwt.decode(jwt_str, public_key, algorithms='RS256', verify=True)
                if len(claims) > 0:
                    verified = True
                    return verified
        except Exception as ex:
            print(ex)
            raise ex

    def generate_rsa_keys(self) -> Dict:
        keypair = rsa.generate_private_key(backend=default_backend(),
                                           public_exponent=65537,
                                           key_size=2048)
        self._public_key = keypair.public_key().public_bytes(encoding=serialization.Encoding.PEM,
                                                             format=serialization.PublicFormat.SubjectPublicKeyInfo)
        # TODO: Determine a proper key format for saving into database.
        # self._public_key = keypair.public_key().public_bytes(serialization.Encoding.OpenSSH,
        #                                                      serialization.PublicFormat.OpenSSH)
        self._private_key = keypair.private_bytes(encoding=serialization.Encoding.PEM,
                                                  format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                  encryption_algorithm=serialization.NoEncryption())
        return {'private_key': self._private_key,
                'public_key': self._public_key}

    def get_private_key(self, client_id: int = 0) -> str:
        if client_id == 0 and self._private_key is not None:
            return self._private_key
        repo = auth_repo.AuthRepositoryOp()
        try:
            self._private_key = ((repo.read(client_id))['private_key']).encode()
            return self._private_key
        except Exception as ex:
            print(ex)
            raise ex
        finally:
            repo.close()

    def get_public_key(self, client_id: int = 0):
        if client_id == 0 and self._private_key is not None:
            return self._private_key
        repo = auth_repo.AuthRepositoryOp()
        try:
            self._public_key = ((repo.read(client_id))['public_key']).encode()
            return self._public_key
        except Exception as ex:
            print(ex)
            raise ex
        finally:
            repo.close()

    def save_all_keys(self, client_id: int,
                      eff_date: datetime = datetime.min,
                      exp_date: datetime = datetime.min) -> None:
        # TODO: Check what key format is proper for database.
        # private_key_str = self._private_key.decode('utf-8')
        # public_key_str = self._public_key.decode('utf-8')
        repo = auth_repo.AuthRepositoryOp()
        try:
            repo.write(client_id,
                       bytes.decode(self._private_key),
                       bytes.decode(self._public_key),
                       eff_date, exp_date,
                       None)
        except Exception as ex:
            print(ex)
            raise ex
        finally:
            repo.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tk = AccessTokenJwt('abc-0123456')
    tk.generate_rsa_keys()
    tk.save_all_keys(101)
    tk.get_public_key(101)
    tk.get_private_key()
    print(tk.assemble_jwt({}, {'mypayload': 'nothing'}))
