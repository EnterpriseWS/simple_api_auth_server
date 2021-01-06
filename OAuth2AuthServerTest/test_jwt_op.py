# import unittest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta
import jwt


def jwt_encode_decode():
    headers = {'kid': 'aa-123456'}
    payload = {'whatelse': 'nothing'}
    nbf = datetime.now().timestamp()
    exp = (datetime.now() + timedelta(minutes=60)).timestamp()
    keypair = rsa.generate_private_key(backend=default_backend(),
                                       public_exponent=65537,
                                       key_size=2048)
    public_key = keypair.public_key().public_bytes(encoding=serialization.Encoding.PEM,
                                                   format=serialization.PublicFormat.SubjectPublicKeyInfo)
    public_key_str = bytes.decode(public_key)
    public_key_bytes = public_key_str.encode()
    private_key = keypair.private_bytes(encoding=serialization.Encoding.PEM,
                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                        encryption_algorithm=serialization.NoEncryption())
    private_key_str = bytes.decode(private_key)
    private_key_bytes = private_key_str.encode()
    try:
        token = jwt.encode(payload, private_key, algorithm='RS256', headers=headers)
        claims = jwt.decode(token, public_key_str, algorithms='RS256', verify=True)
        print(str(claims))
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    jwt_encode_decode()

