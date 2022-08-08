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
    import time
    import json

    with open("tree.txt", encoding='utf-8') as f:
        file_system = json.loads(f.read())
        dir_list = file_system["children"][0]["children"][0]["children"]
        for dir in dir_list:
            if dir["name"] == "项目文档区":
                new_file = {
                    "id": int(time.time()),
                    "isLeaf": True,
                    "name": "团队介绍.md",
                    "pid": int(time.time())
                }
                target = dir["children"][0]["children"]
                target.append(new_file)
        print(json.dumps(file_system, ensure_ascii=False))
