import os
import binascii


def generate_auth_token(length=32):
    return binascii.hexlify(os.urandom(length)).decode('utf-8')
