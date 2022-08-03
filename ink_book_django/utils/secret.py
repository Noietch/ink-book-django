import binascii
from pyDes import des, CBC, PAD_PKCS5


def des_encrypt(s, secret_key="iloveyou"):
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)


def des_decrypt(s, secret_key="iloveyou"):
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de


if __name__ == '__main__':
    pass
