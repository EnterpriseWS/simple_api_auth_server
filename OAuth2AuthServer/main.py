import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# This is a sample Python script.
# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def gen_pki_keys():
    # generate private/public key pair
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
                                   key_size=2048)
    # get public key in OpenSSH format
    public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
                                               serialization.PublicFormat.OpenSSH)
    # get private key in PEM container format
    pem = key.private_bytes(encoding=serialization.Encoding.PEM,
                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                            encryption_algorithm=serialization.NoEncryption())
    # decode to printable strings
    private_key_str = pem.decode('utf-8')
    public_key_str = public_key.decode('utf-8')
    print('Private key = ')
    print(private_key_str)
    print('Public key = ')
    print(public_key_str)


def gen_jwt_token():
    private_key = open('jwt-key').read()
    token = jwt.encode({'user_id': 123}, private_key, algorithm='RS256').decode('utf-8')
    print('Jwt Token = ')
    print (token)
    # private_key = b'-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS...'
    # public_key = b'-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC...'
    # encoded = jwt.encode({'some': 'payload'}, private_key, algorithm='RS256')
    # print(encoded)
    # decoded = jwt.decode(encoded, public_key, algorithms='RS256', verify=True)
    # print(decoded)
    # # Reading the Claimset and header without Validation
    # print(jwt.decode(encoded, verify=False))
    # print(jwt.get_unverified_header(encoded))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    gen_pki_keys()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
