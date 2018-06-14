from django.test import TestCase

from core.encryption.asymmetric import V1 as rsa

import json
import requests
import collections
import base64
import random


def test_start_public_key_upload():
    sk, pk = rsa.generate_key()

    data = collections.OrderedDict()
    data['name'] = 'TestUser' + str(int(random.random() * 10000))
    data['public_key'] = str(pk, encoding='utf-8')
    data_str = json.dumps(data)

    signature = rsa.sign(sk, data_str)

    s = requests.session()
    r = s.post(
        'http://127.0.0.1:8000/user/register',
        data={
            'name': data['name'],
            'public_key': data['public_key'],
            'signature': base64.b64encode(signature)
        }
    )
    print(r.content)
    if json.loads(str(r.content, encoding='utf-8')).get('err') == 1:
        raise Exception('test_start_public_key_upload error')
