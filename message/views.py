from django.http import JsonResponse
from collections import OrderedDict

from session.service import auth_and_delete
from user.models import User
from message.models import Message
from core.encryption.asymmetric import V1 as rsa
from server_key.server_key_service import get_private_key

import config
import json
import base64


def send(requests):
    sender = requests.POST.get('sender')
    receiver = requests.POST.get('receiver')
    message = requests.POST.get('message')
    is_block = requests.POST.get('is_block') == 'True'
    token = requests.POST.get('token')
    signature = base64.b64decode(requests.POST.get('signature'))

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
    if not auth_and_delete(sender, token):
        return JsonResponse({
            'err': 1,
            'msg': 'Invalid token'
        })
    # Check signature
    payload = OrderedDict()
    payload['sender'] = sender
    payload['receiver'] = receiver
    payload['message'] = message
    payload['is_block'] = is_block
    payload['token'] = token
    if not rsa.verify(sender_instance.public_key, json.dumps(payload), signature):
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
    is_read = requests.POST.get('is_read') == 'True'
    token = requests.POST.get('token')
    signature = base64.b64decode(requests.POST.get('signature'))
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
    if not auth_and_delete(receiver, token):
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
    
    msg_instances = Message.objects.filter(receiver=receiver_instance, is_read=is_read)
    ret_msg = list(msg_instances.values())

    for i in range(len(msg_instances)):
        ret_msg[i]['sender'] = msg_instances[i].sender.username
        ret_msg[i]['receiver'] = msg_instances[i].receiver.username
        ret_msg[i]['created_at'] = str(msg_instances[i].created_at)
        msg_instances[i].is_read = True
        msg_instances[i].save()

    payload = OrderedDict()
    payload['msg'] = ret_msg
    server_signature = str(
        base64.b64encode(rsa.sign(get_private_key(), json.dumps(payload['msg']))),
        encoding=config.encoding
    )
    res = dict({
        'err': 0,
        'signature': server_signature
    }, **payload)
    return JsonResponse(res)
