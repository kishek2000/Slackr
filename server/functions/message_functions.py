'''
message_functions written by Liam
- @authorise
- message_send
- message_sendlater
    - message_sendlater_send_messsage
- message_remove
- message_edit
- message_react
- message_unreact
- message_pin
- message_unpint
'''

import sys
import datetime
import time
import threading
sys.path.append("/Server/functions/")
from functions.helper_functions import all_channels_messages, find_message_info
from functions.helper_functions import generate_message_id, get_user_from_token
from functions.helper_functions import get_user_app_permission, has_user_reacted
from functions.Errors import AccessError, ValueError, authorise_channel_id, authorise_token
from functions.Errors import token_in_channel, valid_react, authorise_message_id
from functions.Errors import check_user_is_admin, valid_message, check_user_can_change_message

@authorise_token
@authorise_channel_id
@token_in_channel
@valid_message
def message_send(token=None, channel_id=None, message=None):
    '''Add message to the list of messages in a channel'''        
    message_id = generate_message_id()
    uid = get_user_from_token(token)
    for channel in all_channels_messages:
        if channel["channel_id"] == channel_id:
            channel["total_messages"] += 1
            channel["messages"].insert(0, {
                "message_id": message_id,
                "u_id": uid,
                "message": message,
                "time_created": int(datetime.datetime.now().strftime('%s')),
                "reacts": [],
                "is_pinned": False
            })
    return message_id

def message_sendlater_send_message(token=None, channel_id=None, message=None, message_id=None):
    '''Behaves like message_send, but does not generate its own message_id
    Also, checks already done when message_sendlater is called.'''
    uid = get_user_from_token(token)
    for channel in all_channels_messages:
        if channel["channel_id"] == channel_id:
            channel["total_messages"] += 1
            channel["messages"].insert(0, {
                "message_id": message_id,
                "u_id": uid,
                "message": message,
                "time_created": int(datetime.datetime.now().strftime('%s')),
                "reacts": [],
                "is_pinned": False
            })

@authorise_token
@authorise_channel_id
@token_in_channel
@valid_message
def message_sendlater(token=None, channel_id=None, message=None, time_sent=None):
    '''Behaves like message_send, but only sends the message at the specified time'''
    if time.time() > time_sent:
        raise ValueError("Time is invalid")
    message_id = generate_message_id()
    params = [token, channel_id, message, message_id]
    timer = threading.Timer(time_sent - time.time(), message_sendlater_send_message, params)
    timer.start()
    return message_id

@authorise_token
@authorise_message_id
@check_user_can_change_message
def message_remove(token=None, message_id=None):
    '''Removes the message from list of messages in channel'''
    info = find_message_info(message_id)
    message = info['message']
    channel = info['channel']
    channel["messages"].remove(message)
    channel["total_messages"] -= 1

@authorise_token
@authorise_message_id
@check_user_can_change_message
@valid_message
def message_edit(token=None, message_id=None, message=None):
    '''Changes the string in the message, or removes it if new_message is ""'''
    info = find_message_info(message_id)
    old_message = info['message']
    channel = info['channel']
    if message == "":
        channel["messages"].remove(old_message)
        channel["total_messages"] -= 1
        return
    old_message["message"] = message

@authorise_token
@authorise_message_id
@valid_react
def message_react(token=None, message_id=None, react_id=None):
    '''
    Create a react entry for message if one doesn't exist,
    otherwise appends uid to list of uids that have reacted to the message
    '''
    info = find_message_info(message_id)
    message = info['message']
    uid = get_user_from_token(token)
    if has_user_reacted(uid, react_id, message):
        raise ValueError("Already reacted")
    for react in message['reacts']:
        if react["react_id"] == react_id:
            react["u_ids"].append(uid)
            return
    message["reacts"].append({
        "react_id": react_id,
        "u_ids": [uid]
    })

@authorise_token
@authorise_message_id
@valid_react
def message_unreact(token=None, message_id=None, react_id=None):
    '''
    Removes uid from list of uids reacted
    Removes react entry if this was the only uid reacted to that message
    '''
    info = find_message_info(message_id)
    message = info['message']
    uid = get_user_from_token(token)
    for react in message['reacts']:
        if react["react_id"] == react_id:
            for user in react["u_ids"]:
                if user == uid:
                    react["u_ids"].remove(uid)
                    if react["u_ids"] == []:
                        message["reacts"].remove(react)
                    return
            break
    raise ValueError("Haven't reacted")

@authorise_token
@authorise_message_id
@check_user_is_admin
def message_pin(token=None, message_id=None):
    '''Sets message['is_pinned'] to True'''
    info = find_message_info(message_id)
    message = info['message']
    channel = info['channel']
    if message["is_pinned"]:
        raise ValueError("Message already pinned")
    message["is_pinned"] = True

@authorise_token
@authorise_message_id
@check_user_is_admin
def message_unpin(token=None, message_id=None):
    '''Sets message['ispinned'] to False'''
    info = find_message_info(message_id)
    message = info['message']
    channel = info['channel']
    if not message["is_pinned"]:
        raise ValueError("Message isn't pinned")
    message["is_pinned"] = False
