import sys
import datetime
import time
import threading
sys.path.append("/Server/functions/")
from functions.helper_functions import check_valid_token, check_valid_channel_id, check_token_in_channel, generate_message_id, get_user_from_token, all_channels_messages, find_message_info, get_user_app_permission, has_user_reacted, valid_reacts
from functions.Errors import AccessError

# Helper Functions to write: get_channel_from_message_id
# user_reacted_to_react_id, message_is_pinned

def message_send(token, channel_id, message):
    # Need to somehow check for special characters (\n and the like)
    if len(message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if not check_valid_token(token):
        raise AccessError("Token is invalid")
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
    if not check_valid_token(token):
        raise AccessError("Token is invalid")
    if not check_valid_channel_id(channel_id):
        raise ValueError("Channel ID is invalid")
    if not check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    if len(message) <= 0 or message.isspace():
        raise ValueError("Message must contain a nonspace character")
    # This is a hack solution to enable the case where time_sent = current time
    #if time_sent < datetime.datetime.now(timezone.utc):
    if time.time() > time_sent:
        raise ValueError("Time is invalid")
    message_id = generate_message_id()
    timer = threading.Timer(time_sent - time.time(), message_sendlater_send_message, [token, channel_id, message, message_id])
    timer.start()
    return message_id

def message_remove(token, message_id):
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_valid_token(token):
        raise AccessError("Token is invalid")
    if not check_token_in_channel(token, channel['channel_id']):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    channel["messages"].remove(message)
    channel["total_messages"] -= 1

def message_edit(token, message_id, new_message):
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if len(new_message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if not check_valid_token(token):
        raise AccessError("Token is invalid")
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

def message_react(token, message_id, react_id):
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_valid_token(token):
        raise AccessError("Token is invalid")
    if not check_token_in_channel(token, channel['channel_id']):
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
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_valid_token(token):
        raise AccessError("Token is invalid")
    if not check_token_in_channel(token, channel['channel_id']):
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
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_valid_token(token):
        raise AccessError("Token is invalid")
    if not check_token_in_channel(token, channel['channel_id']):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if message["is_pinned"]:
        raise ValueError("Message already pinned")
    message["is_pinned"] = True

def message_unpin(token, message_id):
    info = find_message_info(message_id)
    if info is None:
        raise ValueError("Message ID is invalid")
    message = info['message']
    channel = info['channel']
    if not check_valid_token(token):
        raise AccessError("Token is invalid")
    if not check_token_in_channel(token, channel['channel_id']):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if message["u_id"] != uid and get_user_app_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if not message["is_pinned"]:
        raise ValueError("Message isn't pinned")
    message["is_pinned"] = False
