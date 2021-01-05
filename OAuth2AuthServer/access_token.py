from typing import Any, Dict
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import jwt


class AccessTokenJwt(object):
    def __init__(self, identifier: str):
        self._identifier = identifier
        self._private_key = self.load_private_key()
        self._public_key = self.load_public_key()

    def assemble_jwt(self, headers: Dict, payload: Dict, payload_encrypt: bool = False) -> str:
        # NOTE: Currently the payload encryption is disabled.
        # TODO: Add payload encryption to the later version.
        try:
            headers['kid'] = self._identifier
            jwt_str = jwt.encode(payload, self._private_key, algorithm='RS256', headers=headers)
            # TODO: Determine if it is needed to validate the token before returning it.
            # jwt.decode(jwt_str, self._public_key, algorithms='RS256', verify=True)
            return jwt_str
        except AttributeError as ex:
            print(ex)
            raise ex
        except Exception as ex:
            print(ex)
            raise ex

    def create_basic_header(self) -> str:
        pass

    def load_private_key(self) -> Any:
        pass

    def load_public_key(self) -> Any:
        pass

    def create_rsa_keys(self):
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

    def save_all_keys(self):
        # private_key_str = self._private_key.decode('utf-8')
        # public_key_str = self._public_key.decode('utf-8')
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tk = AccessTokenJwt('abc-adsfajsonm')
    tk.create_rsa_keys()
    print(tk.assemble_jwt({}, {'mypayload': 'nothing'}))
