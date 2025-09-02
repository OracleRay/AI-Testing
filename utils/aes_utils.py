import json

import hashlib
import base64

import abc
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class BaseAESCipher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encrypt(self, dec, iv):
        """
        加密接口
        @param dec:
        @param iv:
        @return:
        """

    @abc.abstractmethod
    def decrypt(self, enc):
        """
        解密接口
        @param enc:
        @return:
        """


class DataSerializeMixin(object):

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    @staticmethod
    def _unpad(dec):
        try:
            return dec[:-ord(dec[len(dec) - 1:])]
        except:
            return dec

    @staticmethod
    def _paste(data):
        msg = data.encode('utf8')
        repair = 16 - len(msg) % 16
        paste = bytes([repair])
        if repair != 0:
            msg = msg + paste * (repair)
        else:
            msg = msg + repair
        return msg

    def decrypt_string(self, enc):
        """
        将密文数据解密成str
        @param enc: 密文
        @return: 明文
        """
        enc = base64.b64decode(enc)
        return self.decrypt(enc).decode('utf8')

    def decrypt_json(self, enc):
        """
        将密文数据解密到进行序列化
        @param enc: 密文
        @return: 明文
        """
        enc = base64.b64decode(enc)
        data = json.loads(self.decrypt(enc).decode('utf8'))

        return data

    def encrypt_string(self, dec):
        """
        加密str数据
        @param dec: 明文
        @return: 密文
        """
        iv = hashlib.sha256(DataSerializeMixin.str_to_bytes(dec)).digest()
        iv = iv[:AES.block_size]
        enc = self.encrypt(dec, iv)
        return base64.b64encode(iv + enc)

    def encrypt_json(self, dec):
        """
        将数据装换成json加密
        @param dec: 明文
        @return: 密文
        """
        dec = json.dumps(dec)
        iv = hashlib.sha256(DataSerializeMixin.str_to_bytes(dec)).digest()
        iv = iv[:AES.block_size]
        enc = self.encrypt(dec, iv)
        return base64.b64encode(iv + enc)


class AESGCMCipher(BaseAESCipher, DataSerializeMixin):
    def __init__(self, key, key_size):
        KEY_SIZE_MAP = {
            "AES-128": 16,
            "AES-192": 24,
            "AES-256": 32
        }
        self.bs = AES.block_size
        self.key = hashlib.sha256(DataSerializeMixin.str_to_bytes(key)).digest()[0:KEY_SIZE_MAP[key_size]]

    def decrypt(self, enc):
        aesgcm = AESGCM(self.key)
        iv = enc[:AES.block_size]
        data = aesgcm.decrypt(iv, enc[AES.block_size:], None)

        return self._unpad(data)

    def encrypt(self, dec, iv):
        aesgcm = AESGCM(self.key)
        dec = self._paste(dec)
        data = aesgcm.encrypt(iv, dec, None)
        return data


class AESCommonCipher(BaseAESCipher, DataSerializeMixin):
    def __init__(self, key: str, mode: str = "GCM", key_size: str = 'AES-128'):
        """

        @param key: AES_KEY
        @param mode: AES_MODE
        {

        }
        """
        MODE_MAP = {
            "ECB": AES.MODE_ECB,
            "CBC": AES.MODE_CBC,
            "CFB": AES.MODE_CFB,
            "OFB": AES.MODE_OFB,
            "CTR": AES.MODE_CTR,
            "OPENPGP": AES.MODE_OPENPGP
        }
        KEY_SIZE_MAP = {
            "AES-128": 16,
            "AES-192": 24,
            "AES-256": 32
        }
        self.bs = AES.block_size
        self.key = hashlib.sha256(AESCommonCipher.str_to_bytes(key)).digest()[0:KEY_SIZE_MAP[key_size]]
        self.mode = MODE_MAP[mode]

    def decrypt(self, enc):
        """
        解密AES密文
        @param enc: 传入密文
        @return:
        """
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, self.mode, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def encrypt(self, dec, iv):
        """
        对明文数据进行AES加密
        @param dec: 加密数据
        @param iv: 偏移
        @return:
        """
        cipher = AES.new(self.key, self.mode, iv)
        dec = self._paste(dec)
        return cipher.encrypt(dec)


def create_cipher_class(key, mode='GCM', key_size='AES-128'):
    if mode == "GCM":
        return AESGCMCipher(key, key_size)
    return AESCommonCipher(key, mode, key_size)


AESCipher = create_cipher_class


def str_jm(data):
    encrypt = data
    cipher = AESCipher("AESTEST")
    str_data = cipher.decrypt_string(encrypt)
    print("明文:{}".format(str_data))


def aes_cryption(type, data, AES_KEY):
    cipher = AESCipher(AES_KEY)
    if type == 'decode':
        json_data = cipher.decrypt_json(data)
        return json_data
    elif type == 'encode':
        enc = cipher.encrypt_json(data)
        return enc.decode('utf-8')
    else:
        return


if __name__ == '__main__':
    a = aes_cryption(type='decode',
                     data='94KI7cmuncyTRSW5UYA/rnwCCtJRWxc8ZLhVfD0sQ4mdiSqBfaTegUZYjrgCpIITf993IIdPb9y4XJyyDMRQ28HjEP0HK2sCovZqiHeHiflADp2leQI2rRKZVn6zGG4PMph9ogv9hgbrkfz7mLd30HdIr1lqpzM+hZ18muyKi6pT222daQVoLUiUPq4rmRkVdNQlwp8XcBbMleDVXymyZXKpSEhzo3yPEQWy5VwXhJuS2cF7bGN92ccpEplYx/OROfV7fvkzLFYh/IRj9SoEsE/Cr5lQiPKeoSFeLlJT12oF4meEbR9LvuEa8z8gpJ4HkklqJgrkSAghK1JyqtkWdNw7rmgCmz9rVucatwcwVYVRU442tzaLleOQui1FOzoYd9C5qoDC9L9bA3ms0xnpUlogEV23e1et/eY3KTDodwMWO7BNvkpSeASjcuq/83LJwtLMInaXVPCzCPJ17LS8QS7C7N42dxb5XsXfBj8OOuFZb71cX6QWKF3OkKMof56VWSqPbCoZ2QNGA3/jhNolondUFJPFjAHuqMPPTiFJMFoLEP3+oU3A6W7MlCafd+uq6KcWF5LF0ngq4Vf4VqB7QMpCO8UG6Jv+ZXdAYG+mWiXNr8KVJZ/iLDzp65FRor6qeV9UTubCtdchL7Rrw1SjUnoToq9vqbnNVmqqfx5/jjYbluD3K1xzTrScDuSpfKX09C59jWOa8BOhiYKNPQCTAh+rbTbB5t7OErfDIekVG0E=',
                     AES_KEY='9x6a3dRng05wB6UrG1s5oM6d7f3x564ss5Et3m3878l06f27nM56183XZTX31GK5')
    print(a)
