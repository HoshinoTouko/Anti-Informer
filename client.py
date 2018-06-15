from core.encryption.asymmetric import V1 as asy
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
try:
    with open(root_dir+"/.data/user/key","r") as fsk:
        sk = fsk.read()
    with open(root_dir+"/.data/user/key.pub","r") as fpk:
        pk = fpk.read()
except IOError:
    try:
        sk, pk = asy.generate_key()
        if not os.path.exists(root_dir+"/.data/user/"):
            os.makedirs(root_dir+"/.data/user/") 
        with open(root_dir+"/.data/user/key","wb+") as fsk:
            fsk.write(sk)
        with open(root_dir+"/.data/user/key.pub","wb+") as fpk:
            fpk.write(pk)
    except IOError:
        print("无法写入密钥，请检查文件系统权限")


