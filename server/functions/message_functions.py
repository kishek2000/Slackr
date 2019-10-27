import sys
sys.path.append("/Server/functions/")
from functions.helper_functions import check_valid_token, check_valid_channel_id, check_token_in_channel, generate_message_id, get_user_from_token, all_channels_messages, find_message_info, get_user_app_permission, has_user_reacted, valid_reacts
from functions.Errors import AccessError
import datetime
import time
import threading

# Helper Functions to write: get_channel_from_message_id
# user_reacted_to_react_id, message_is_pinned

def message_send(token, channel_id, message):
    # Need to somehow check for special characters (\n and the like)
    if len(message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Channel ID is invalid")
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError("Token not in channel")
    if len(message) <= 0 or message.isspace() == True:
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

def message_sendlater(token, channel_id, message, time_sent):
    if len(message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Channel ID is invalid")
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError("Token not in channel")
    if len(message) <= 0 or message.isspace() == True:
        raise ValueError("Message must contain a nonspace character")
    # This is a hack solution to enable the case where time_sent = current time
    #if time_sent < datetime.datetime.now(timezone.utc):
    if time.time() > time_sent:
        raise ValueError("Time is invalid")
    message_id = generate_message_id()
    #t = threading.Timer(time_sent - datetime.datetime.now(), message_sendlater_send_message, [token, channel_id, message, message_id])
    t = threading.Timer(time_sent - time.time(), message_sendlater_send_message, [token, channel_id, message, message_id])
    t.start()
    return message_id
    
def message_remove(token, message_id):
    info = find_message_info(message_id)
    if info == None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel['channel_id']) == False:
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    channel["messages"].remove(message)
    channel["total_messages"] -= 1
    
def message_edit(token, message_id, new_message):
    info = find_message_info(message_id)
    if info == None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if len(new_message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel['channel_id']) == False:
        raise AccessError("Token not in channel")
    if len(new_message) <= 0 or new_message.isspace() == True:
        raise ValueError("Message must contain a nonspace character")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    message["message"] = new_message

def message_react(token, message_id, react_id):
    info = find_message_info(message_id)
    if info == None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel['channel_id']) == False:
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if react_id not in valid_reacts:
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
    
def message_unreact(token, message_id, react_id):
    info = find_message_info(message_id)
    if info == None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel['channel_id']) == False:
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if react_id not in valid_reacts:
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
    
def message_pin(token, message_id):
    info = find_message_info(message_id)
    if info == None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel['channel_id']) == False:
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if message["is_pinned"] == True:
        raise ValueError("Message already pinned")
    message["is_pinned"] = True
    
def message_unpin(token, message_id):
    info = find_message_info(message_id)
    if info == None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel['channel_id']) == False:
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if message["is_pinned"] == False:
        raise ValueError("Message isn't pinned")
    message["is_pinned"] = False