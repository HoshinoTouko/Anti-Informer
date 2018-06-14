from .service import create_session
from core.encryption.asymmetric import V1 as rsa
from server_key import server_key_service

from django.http import JsonResponse
from collections import OrderedDict

import json
import base64


def start_new_session(request):
    username = request.POST.get('user')
    if not username:
        return JsonResponse({
            'err': 1,
            'msg': 'No user name'
        })
    session = create_session(username)

    if not session:
        return JsonResponse({
            'err': 1,
            'msg': 'Unknown error'
        })

    server_sk = server_key_service.get_private_key()
    payload = OrderedDict()
    payload['key'] = session.key

    signature = rsa.sign(server_sk, json.dumps(payload))

    res = dict({
        'err': 0,
        'signature': str(base64.b64encode(signature), "utf-8")
    }, **payload)
    return JsonResponse(res)
