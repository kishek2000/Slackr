from helper_functions import *

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
    return message_id
    
def message_remove(token, message_id):
    pass
    
def message_edit(token, message_id, message):
    pass
    
def message_react(token, message_id, react_id):
    pass
    
def message_unreact(token, message_id, react_id):
    pass
    
def message_pin(token, message_id):
    pass
    
def message_unpin(token, message_id):
    pass
