from helper_functions import *

# Helper Functions to write: message_id_exists, get_channel_from_message_id
# user_reacted_to_react_id, message_is_pinned

def message_send(token, channel_id, message):
    # Need to somehow check for special characters (\n and the like)
    if len(message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Channel ID is invalid")
    if check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    if len(message) <= 0 or message.isspace() == True:
        raise ValueError("Message must contain a nonspace character")
        
    
    return message_id

def message_send_later(token, channel_id, message, time_sent):
    if len(message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Channel ID is invalid")
    if check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    if len(message) <= 0 or message.isspace() == True:
        raise ValueError("Message must contain a nonspace character")
    if time_sent < time():
        raise ValueError("Time is invalid")
    return message_id
    
def message_remove(token, message_id):
    if message_id_exists(message_id):
        raise ValueError("Message ID is invalid")
    channel_id = get_channel_from_message_id(message_id)
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if get_user_id_from_message_id(message_id) != uid && get_user_permission(uid) == 3:
        raise AccessError("Do not have permission")
    
def message_edit(token, message_id, message):
    if message_id_exists(message_id):
        raise ValueError("Message ID is invalid")
    channel_id = get_channel_from_message_id(message_id)
    if len(message) > 1000:
        raise ValueError("Message must be 1000 characters or less")
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    if len(message) <= 0 or message.isspace() == True:
        raise ValueError("Message must contain a nonspace character")
    uid = get_user_from_token(token)
    if get_user_id_from_message_id(message_id) != uid && get_user_permission(uid) == 3:
        raise AccessError("Do not have permission") 
    
def message_react(token, message_id, react_id):
    if message_id_exists(message_id):
        raise ValueError("Message ID is invalid")
    channel_id = get_channel_from_message_id(message_id)
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if get_user_id_from_message_id(message_id) != uid && get_user_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if react_id not in valid_reacts:
        raise ValueError("Not a valid react_id")
    if user_reacted_to_react_id(uid, react_id):
        raise ValueError("Already reacted")
    
def message_unreact(token, message_id, react_id):
    if message_id_exists(message_id):
        raise ValueError("Message ID is invalid")
    channel_id = get_channel_from_message_id(message_id)
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if get_user_id_from_message_id(message_id) != uid && get_user_permission(uid) == 3:
        raise AccessError("Do not have permission") 
    if react_id not in valid_reacts:
        raise ValueError("Not a valid react_id")
    if not user_reacted_to_react_id(uid, react_id):
        raise ValueError("Haven't reacted")
    
def message_pin(token, message_id):
    if message_id_exists(message_id):
        raise ValueError("Message ID is invalid")
    channel_id = get_channel_from_message_id(message_id)
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if get_user_id_from_message_id(message_id) != uid && get_user_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if message_is_pinned(message_id):
        raise ValueError("Message already pinned"]
    
def message_unpin(token, message_id):
    if message_id_exists(message_id):
        raise ValueError("Message ID is invalid")
    channel_id = get_channel_from_message_id(message_id)
    if check_valid_token(token) == False:
        raise AccessError("Token is invalid")
    if check_token_in_channel(token, channel_id):
        raise AccessError("Token not in channel")
    uid = get_user_from_token(token)
    if get_user_id_from_message_id(message_id) != uid && get_user_permission(uid) == 3:
        raise AccessError("Do not have permission")
    if message_is_pinned(message_id):
        raise ValueError("Message isn't pinned"]
