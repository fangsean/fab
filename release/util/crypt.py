# -*- coding:utf-8 -*-
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import hashlib


class prpcrypt():
    # 编码
    __final__code = "utf-8"
    # 补全码
    __final__build = '\0'

    def __init__(self, key):
        self.__key__ = self.__md5__(key)
        self.__mode__ = AES.MODE_CBC

    def __md5__(self, text):
        """
        由于hash不处理unicode编码的字符串（python3默认字符串是unicode）
            所以这里判断是否字符串，如果是则进行转码
            初始化md5、将url进行加密、然后返回加密字串
        """
        if isinstance(text, str):
            text = text.encode(self.__final__code)
        md = hashlib.md5()
        md.update(text)
        return md.hexdigest()[0:16]

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.__key__, self.__mode__, self.__key__)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + (self.__final__build * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.__key__, self.__mode__, self.__key__)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text
        # return str(plain_text).rstrip('\0')

    @staticmethod
    def get_password(key, passwd):
        pc = prpcrypt(key)  # 初始化密钥
        d = pc.decrypt(passwd)
        return d.decode(prpcrypt.__final__code)

    @staticmethod
    def encrypt_password(key, passwd):
        pc = prpcrypt(key)  # 初始化密钥
        e = pc.encrypt(passwd)
        return e.decode(prpcrypt.__final__code)


# if __name__ == '__main__':
#     pc = prpcrypt('nqtown')  # 初始化密钥
#     e = pc.encrypt("nanquan@2017")
#     d = pc.decrypt(e)
#     print(d.decode("utf-8"))
#     print(e.decode("utf-8"))
