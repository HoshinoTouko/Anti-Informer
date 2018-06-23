from core.encryption.symmetric import V1 as chacha20
from core.encryption.asymmetric import V1 as rsa
import time

def testchacha():
    sk, pk = rsa.generate_key()
    key = "12345678"
    x = chacha20.encrypt(key,sk)
    start = time.time()
    for i in range(1000000):
        chacha20.decrypt(key,x)
    end = time.time()
    print(end - start)
