# core/encryption/asymmetric

## V1

### Key generator

method: ues __built_in_method__

Generate a RSA key pair according to the config in __config.rsa_key_length__.

API reference: http://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html

### Encrypt

- First
Generate a 32 bytes session key.
- Second
Use chacha20 symmetric encryption to encrypt and generate tag.
- Third
Use PKCS1_OAEP protocol to encrypt session key by public key.

method: __PKCS1_OAEP__

API reference: http://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html

### Decrypt

- First
Decrypt session key by private key.
- Second
Use chacha20 symmetric encryption to decrypt and verify tag.

method: __PKCS1_OAEP__

API reference: http://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html

### Sign

- First
Hash the total message.
- Second
Sign.

method: __SHA512__, __pkcs1_15__

API reference: http://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html

### Verify

- First
Hash the total message.
- Second
Verify.

method: __SHA512__, __pkcs1_15__

API reference: http://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
