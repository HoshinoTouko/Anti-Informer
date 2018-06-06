"""
@File: symmetric.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-06 14:20
@Desc:
API watch: doc/core/encryption/symmetric.md
"""
from Crypto.Cipher import ChaCha20
from Crypto.Hash import HMAC, SHA512

from core.utils import trans_to_bytes

import config


class V1:
    @classmethod
    def encrypt(cls, key, plaintext):
        # Trans encrypt info to byte
        key = trans_to_bytes(key)
        plaintext = trans_to_bytes(plaintext)

        # Adjust the key to 256 bits
        h = SHA512.new(truncate="256")
        h.update(key)
        key = h.digest()

        # Generate an instance
        cipher = ChaCha20.new(key=key)
        # Encrypt
        return cipher.nonce + cipher.encrypt(plaintext)

    @classmethod
    def encrypt_and_digest(cls, key, plaintext):
        ciphertext = cls.encrypt(key, plaintext)
        h = HMAC.new(ciphertext, digestmod=SHA512)
        return ciphertext, h.digest()

    @classmethod
    def decrypt(cls, key, original_ciphertext):
        # Trans decrypt info to byte
        key = trans_to_bytes(key)
        original_ciphertext = trans_to_bytes(original_ciphertext)

        # Adjust the key to 256 bits
        h = SHA512.new(truncate="256")
        h.update(key)
        key = h.digest()

        # Get nonce and text
        msg_nonce = original_ciphertext[:8]
        ciphertext = original_ciphertext[8:]
        # Decrypt
        cipher = ChaCha20.new(key=key, nonce=msg_nonce)
        return cipher.decrypt(ciphertext)

    @classmethod
    def decrypt_and_verify(cls, key, original_ciphertext, tag):
        # Trans decrypt info to byte
        key = trans_to_bytes(key)
        original_ciphertext = trans_to_bytes(original_ciphertext)
        # Decrypt
        plaintext = cls.decrypt(key, original_ciphertext)
        # Verify
        h = HMAC.new(original_ciphertext, digestmod=SHA512)
        verified = True
        try:
            h.verify(tag)
        except ValueError:
            verified = False
        return plaintext, verified


if __name__ == '__main__':
    message = 'She literature discovered increasing how diminution understood. ' \
              'Though and highly the enough county for man. ' \
              'Of it up he still court alone widow seems. ' \
              'Suspected he remainder rapturous my sweetness. ' \
              'All vanity regard sudden nor simple can. ' \
              'World mrs and vexed china since after often. '
    secret_key = '*Thirty-two byte (256 bits) key*'
    ciphertext, tag = V1.encrypt_and_digest(secret_key, message)
    print(ciphertext, tag)
    plain, verify = V1.decrypt_and_verify(secret_key, ciphertext, tag)
    print(str(plain, encoding=config.encoding))
