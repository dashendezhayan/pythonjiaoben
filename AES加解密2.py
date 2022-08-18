from Crypto.Cipher import AES
import os
from Crypto import Random
import base64
import binascii
"""
aes加密算法
padding : PKCS7
"""

class AESUtil:
    __BLOCK_SIZE_16 = BLOCK_SIZE_16 = AES.block_size

    @staticmethod
    def encryt(string, key, iv):
        """
        加密文本
        :param string: 文本
        :param key: 密钥
        :param iv: 偏移量/初始向量
        :return: 密文
        """
        cipher = AES.new(key, AES.MODE_CBC, iv)
        x = AESUtil.__BLOCK_SIZE_16 - (len(string) % AESUtil.__BLOCK_SIZE_16)
        # 如果最后一块不够16位需要用字符进行补全
        if x != 0:
            string = string + chr(x) * x
        msg = cipher.encrypt(string.encode('utf-8'))

        # msg = base64.urlsafe_b64encode(msg).replace('=', '')
        # msg = base64.b64encode(msg)
        return msg

    @staticmethod
    def decrypt(en_str, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # en_str += (len(en_str) % 4)*"="
        # decryptByts = base64.urlsafe_b64decode(en_str)
        # decryptByts = base64.b64decode(en_str)
        # msg = cipher.decrypt(decryptByts)

        msg = cipher.decrypt(en_str)
        padding_len = msg[len(msg) - 1]
        return msg[0:-padding_len]


if __name__ == "__main__":
    # import hashlib
    # key = hashlib.md5().hexdigest()   # 随机生产一个md5值，32位
    string='32060b2862970300017d10003b4a53411b274dc6d6b6ee44d3c7a80f'
    string=string[24:]
    string=bytes.fromhex(string)
    print(string)
    key = b'4845727543536D5570716A3843596451'
    iv = b'70716A3843596451'
    # key = b"42644f344d537878517033326b507754"  # 32位
    # iv = b"517033326b507754"  # 16位

    # key = b"5477506bb323370517878534d344f6442"  # 32位
    # iv = b"7878534d344f6442"  # 16位
    #res = AESUtil.encryt(string, key, iv)
    #print(binascii.b2a_hex(res))
    text=AESUtil.decrypt(string, key, iv)
    print(text)
    print(binascii.b2a_hex(text))