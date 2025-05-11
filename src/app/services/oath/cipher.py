from pyotp import random_base32
from src.infra.aes_cipher import aes_cipher_infra


class OTPCipherService:
    cipher = aes_cipher_infra

    def generate_secret(self) -> tuple[str, str]:
        """
        Generate a random b32 secret key and its hash.
        """
        raw_secret = random_base32()
        hash_secret = self.cipher.encrypt_b64(raw_secret)
        return raw_secret, hash_secret

    def decrypt_secret(self, hash_secret: str) -> str:
        """
        Decrypt the hash secret to get the raw secret.
        """
        return self.cipher.decrypt_b64(hash_secret)
