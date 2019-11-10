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
from functions.helper_functions import check_valid_token, check_valid_channel_id
from functions.helper_functions import check_token_in_channel, generate_message_id
from functions.helper_functions import get_user_from_token, all_channels_messages
from functions.helper_functions import find_message_info, get_user_app_permission
from functions.helper_functions import has_user_reacted, VALID_REACTS
from functions.Errors import AccessError

def authorise(function):
    def wrapper(*args, **kwargs):
        argsList = list(args)
        if not check_valid_token(argsList[0]):
            raise AccessError("Token is Invalid")
        return function(*args, **kwargs)
    return wrapper

@authorise
def message_send(token, channel_id, message):
    '''Add message to the list of messages in a channel'''
    if len(message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if not check_valid_channel_id(channel_id):
        raise ValueError("Channel ID is invalid")
    if not check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    if len(message) <= 0 or message.isspace():
        raise ValueError("Message must contain a nonspace character")
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

def message_sendlater_send_message(token, channel_id, message, message_id):
    '''Behaves like message_send, but does not generate its own message_id'''
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

@authorise
def message_sendlater(token, channel_id, message, time_sent):
    '''Behaves like message_send, but only sends the message at the specified time'''
    if len(message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if not check_valid_channel_id(channel_id):
        raise ValueError("Channel ID is invalid")
    if not check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    if len(message) <= 0 or message.isspace():
        raise ValueError("Message must contain a nonspace character")
    if time.time() > time_sent:
        raise ValueError("Time is invalid")
    message_id = generate_message_id()
    params = [token, channel_id, message, message_id]
    timer = threading.Timer(time_sent - time.time(), message_sendlater_send_message, params)
    timer.start()
    return message_id

@authorise
def message_remove(token, message_id):
    '''Removes the message from list of messages in channel'''
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_token_in_channel(token, channel['channel_id']):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    channel["messages"].remove(message)
    channel["total_messages"] -= 1

@authorise
def message_edit(token, message_id, new_message):
    '''Changes the string in the message, or removes it if new_message is ""'''
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if len(new_message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if not check_token_in_channel(token, channel['channel_id']):
        raise AccessError("Token not in channel")
    if new_message.isspace():
        raise ValueError("Message must contain a nonspace character (or be empty)")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if new_message == "":
        channel["messages"].remove(message)
        channel["total_messages"] -= 1
        return
    message["message"] = new_message

@authorise
def message_react(token, message_id, react_id):
    '''
    Create a react entry for message if one doesn't exist,
    otherwise appends uid to list of uids that have reacted to the message
    '''
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_token_in_channel(token, channel['channel_id']):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if react_id not in VALID_REACTS:
        raise ValueError("Not a valid react_id")
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

@authorise
def message_unreact(token, message_id, react_id):
    '''
    Removes uid from list of uids reacted
    Removes react entry if this was the only uid reacted to that message
    '''
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_token_in_channel(token, channel['channel_id']):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if react_id not in VALID_REACTS:
        raise ValueError("Not a valid react_id")
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

@authorise
def message_pin(token, message_id):
    '''Sets message['is_pinned'] to True'''
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_token_in_channel(token, channel['channel_id']):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if message["is_pinned"]:
        raise ValueError("Message already pinned")
    message["is_pinned"] = True

@authorise
def message_unpin(token, message_id):
    '''Sets message['ispinned'] to False'''
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_token_in_channel(token, channel['channel_id']):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if not message["is_pinned"]:
        raise ValueError("Message isn't pinned")
    message["is_pinned"] = False
