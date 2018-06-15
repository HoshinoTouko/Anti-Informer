from django.http import JsonResponse
from collections import OrderedDict

from session.service import auth_and_delete
from user.models import User
from message.models import Message
from core.encryption.asymmetric import V1 as rsa
from server_key.server_key_service import get_private_key

import json


def send(requests):
    sender = requests.POST.get('sender')
    receiver = requests.POST.get('receiver')
    message = requests.POST.get('message')
    is_block = requests.POST.get('is_block') == 'True'
    token = requests.POST.get('token')
    signature = requests.POST.get('signature')

    # Check post data
    if None in [sender, receiver, message, is_block, token, signature]:
        return JsonResponse({
            'err': 1,
            'msg': 'Something lost'
        })
    try:
        sender_instance = User.objects.get(username=sender)
        receiver_instance = User.objects.get(username=receiver)
    except Exception as e:
        return JsonResponse({
            'err': 1,
            'msg': 'User error' + str(e)
        })
    # Check token
    if not auth_and_delete(token):
        return JsonResponse({
            'err': 1,
            'msg': 'Invalid token'
        })
    # Check signature
    payload = OrderedDict()
    payload['sender'] = sender
    payload['receiver'] = receiver
    payload['is_block'] = is_block
    payload['token'] = token
    if not rsa.verify(sender.public_key, json.dumps(payload), signature):
        return JsonResponse({
            'err': 1,
            'msg': 'Invalid signature'
        })
    # Create message
    Message.objects.create(
        sender=sender_instance,
        receiver=receiver_instance,
        message=message,
        is_block=is_block
    )
    return JsonResponse({
        'err': 0
    })


def receive(requests):
    receiver = requests.POST.get('receiver')
    is_read = requests.POST.get('is_read') == True
    token = requests.POST.get('token')
    signature = requests.POST.get('signature')
    # Check post data
    if None in [receiver, token, signature]:
        return JsonResponse({
            'err': 1,
            'msg': 'Something lost'
        })
    try:
        receiver_instance = User.objects.get(username=receiver)
    except Exception as e:
        return JsonResponse({
            'err': 1,
            'msg': 'User error' + str(e)
        })
    # Check token
    if not auth_and_delete(token):
        return JsonResponse({
            'err': 1,
            'msg': 'Invalid token'
        })
    # Check signature
    payload = OrderedDict()
    payload['receiver'] = receiver
    payload['token'] = token
    if not rsa.verify(receiver_instance.public_key, json.dumps(payload), signature):
        return JsonResponse({
            'err': 1,
            'msg': 'Invalid signature'
        })

    msg = Message.objects.filter(receiver=receiver, is_read=is_read)
    for m in msg:
        m.is_read = True
    msg = msg.values()

    payload = OrderedDict()
    payload['msg'] = msg
    server_signature = rsa.sign(get_private_key(), json.dumps(payload))
    res = dict({
        'err': 0,
        'signature': server_signature
    }, **payload)
    return JsonResponse(res)
