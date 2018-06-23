from core.encryption.asymmetric import V1 as rsa
import time

def testrsa():
    with open("benchmark/rfc8017.txt", 'r') as f:
        message = f.read()
    sk, pk = rsa.generate_key()
    encrypt_session_key, ciphertext, tag = rsa.encrypt(pk, message)
    plain, verify = rsa.decrypt(sk, encrypt_session_key, ciphertext, tag)
    print(str(plain))
