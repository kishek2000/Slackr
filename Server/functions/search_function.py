from .helper_functions import *

def search(token, query_str):
    
    foundMessages = []
        
    # Find messages that match the query_str from all the channels the user has joined
    for channel in all_channel_messages:
        for users in channels['all_members']:
                if users['token'] == get_user_from_token(token):
                    for message in channel["messages"]:
                        if query_str in message["message"]:
                            foundMessages.append({"channel_id": channel["channel_id"], "message_id": message["message_id"], "message": message}
    return foundMessages
