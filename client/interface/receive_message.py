from client import token_service, server_connect_service, message_service
from client.userdata_service import load_unencrypted_data


def receive_message_interface(my_pass, is_read=False):
    me = load_unencrypted_data('name')
    message_service.receive_message(
        me, my_pass, is_read=is_read
    )
    return
