from base64 import b64decode
from os import urandom, getenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from src.app.utils.helpers.logs import get_logger
from src.app.configs.constants import TESTING_ENV
from src.app.utils.helpers.server import terminate_server

log = get_logger(__name__)


class AESCipherService(object):

    def __init__(self):
        if not TESTING_ENV:
            self.aes_key = self.parse_aes_key_from_environ()
        else:
            self.aes_key = self.generate_random_bytes()

    @staticmethod
    def parse_aes_key_from_environ() -> bytes:
        if not (aes_key := getenv("_B64_AES_KEY")):
            log.error("Missing B64_AES_KEY environment variable")
            terminate_server()

        try:
            key_bytes = b64decode(aes_key)
        except Exception:
            log.error("Invalid Base64 encoding for AES key")
            terminate_server()

        if len(key_bytes) not in (16, 24, 32):
            log.error("Invalid AES key length")
            terminate_server()

        return key_bytes

    @staticmethod
    def generate_random_bytes(length: int = 16) -> bytes:
        return urandom(length)

    def encrypt(self, data: bytes) -> bytes:
        iv = self.generate_random_bytes()
        cipher = Cipher(algorithms.AES(self.aes_key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return iv + ciphertext + encryptor.tag

    def decrypt(self, data: bytes) -> bytes:
        iv, ciphertext, tag = data[:16], data[16:-16], data[-16:]
        cipher = Cipher(algorithms.AES(self.aes_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()


aes_cipher_service = AESCipherService()
