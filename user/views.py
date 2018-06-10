from django.http import JsonResponse
from collections import OrderedDict

from server_key.server_key_service import get_public_key
from core.encryption.asymmetric import V1 as rsa
from .service import check_user_signature, pack_server_public_key
from .models import User

import json
import base64


def start_public_key_upload(request):
    # Get post data
    user_name = request.POST.get('name')
    user_public_key = request.POST.get('public_key')
    user_signature = base64.b64decode(request.POST.get('signature'))
    # Check
    if user_name is None or user_public_key is None \
            or user_signature is None:
        return JsonResponse({'err': 1, 'msg': 'Post data error'})

    payload = OrderedDict()
    payload['name'] = user_name
    payload['public_key'] = user_public_key
    payload_str = json.dumps(payload)
    # Verify
    verify = check_user_signature(user_public_key, payload_str, user_signature)
    if verify:
        User.objects.create(
            username=user_name,
            public_key=user_public_key,
            signature=str(base64.b64encode(user_signature), encoding='utf-8'),
        )
        payload, server_signature = pack_server_public_key(user_public_key)
        return JsonResponse({
            'err': 0,
            'payload': payload,
            'signature': server_signature
        })
    return JsonResponse({
        'err': 1,
        'msg': 'Signature auth error'
    })



