from django.http import JsonResponse
from collections import OrderedDict

from server_key.server_key_service import get_public_key
from core.encryption.asymmetric import V1 as rsa
from .service import check_user_signature, get_public_key_by_username
from .models import User

import json
import base64


def register(request):
    # Get post data
    user_name = request.POST.get('name')
    user_public_key = request.POST.get('public_key')
    user_signature = base64.b64decode(request.POST.get('signature'))
    # Check
    # Forbid username 'server'
    if user_name is None or user_public_key is None \
            or user_signature is None or 'server' in user_name:
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
        return JsonResponse({
            'err': 0,
            'server_public_key': get_public_key()
        })
    return JsonResponse({
        'err': 1,
        'msg': 'Signature auth error'
    })


def query(request):
    # Get post data
    if request.method == 'POST':
        user_name = request.POST.get('name')
    else:
        user_name = request.GET.get('name')
    if user_name is None:
        return JsonResponse({
            'err': 0,
            'name': list(User.objects.values_list('username'))
        })
    # Get server public key
    if user_name == 'server':
        return JsonResponse({
            'err': 0,
            'server_public_key': get_public_key()
        })
    # Get other's pk
    payload, signature = get_public_key_by_username(user_name)
    res = dict({
        'err': 0,
        'signature': signature
    }, **payload)
    return JsonResponse(res)
