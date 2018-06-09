"""
@File: asymmetric.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-07 22:12
@Desc: 
"""
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512

from core.utils import trans_to_bytes
from core.encryption.symmetric import V1 as chacha20

import config


class V1:
    @classmethod
    def generate_key(cls):
        key = RSA.generate(config.rsa_key_length)
        private_key = key.export_key(pkcs=8)
        public_key = key.publickey().export_key(pkcs=8)
        return private_key, public_key

    @classmethod
    def encrypt(cls, public_key, plaintext):
        # Convert to bytes
        public_key = trans_to_bytes(public_key)
        plaintext = trans_to_bytes(plaintext)
        # Generate a session key and encrypt the message
        session_key = get_random_bytes(32)
        ciphertext, tag = chacha20.encrypt_and_digest(session_key, plaintext)
        # Encrypt session key
        recipient_key = RSA.import_key(public_key)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        encrypt_session_key = cipher_rsa.encrypt(session_key)

        return encrypt_session_key, ciphertext, tag

    @classmethod
    def decrypt(cls, private_key, enc_session_key, ciphertext, tag=None):
        # Convert to bytes
        private_key = trans_to_bytes(private_key)
        enc_session_key = trans_to_bytes(enc_session_key)
        ciphertext = trans_to_bytes(ciphertext)
        # Load key and decrypt session key
        private_key_instance = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key_instance)
        session_key = cipher_rsa.decrypt(enc_session_key)
        # Decrypt ciphertext
        verify = False
        if tag is None:
            plain = chacha20.decrypt(session_key, ciphertext)
        else:
            plain, verify = chacha20.decrypt_and_verify(session_key, ciphertext, tag)

        return plain, verify

    @classmethod
    def sign(cls, private_key, text_to_sign):
        # Convert to byte
        private_key = trans_to_bytes(private_key)
        text_to_sign = trans_to_bytes(text_to_sign)
        # Sign
        signature_rsa = pkcs1_15.new(RSA.import_key(private_key))
        signature = signature_rsa.sign(SHA512.new(text_to_sign))

        return signature

    @classmethod
    def verify(cls, public_key, text_to_verify, signature):
        # Convert to byte
        public_key = trans_to_bytes(public_key)
        text_to_verify = trans_to_bytes(text_to_verify)
        signature = trans_to_bytes(signature)
        # Verify
        verify = False
        try:
            pkcs1_15.new(
                RSA.import_key(public_key)
            ).verify(
                SHA512.new(text_to_verify), signature
            )
            verify = True
        except Exception as e:
            print(str(e))
        return verify


def testcase():
    private_key, public_key = V1.generate_key()
    message = 'She literature discovered increasing how diminution understood. ' \
              'Though and highly the enough county for man. ' \
              'Of it up he still court alone widow seems. ' \
              'Suspected he remainder rapturous my sweetness. ' \
              'All vanity regard sudden nor simple can. ' \
              'World mrs and vexed china since after often. '
    encrypt_session_key, ciphertext, tag = V1.encrypt(private_key, message)
    # print(encrypt_session_key, ciphertext, tag)

    plain, verify = V1.decrypt(private_key, encrypt_session_key, ciphertext, tag)
    print(plain, verify)

    signature = V1.sign(private_key, message)
    print(len(signature))
    print(V1.verify(public_key, message + '1', signature))


if __name__ == '__main__':
    testcase()
