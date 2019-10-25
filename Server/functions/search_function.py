from functions.helper_functions import *

def search(token, query_str):
    
    foundMessages = []
    #Checking for valid query_str
    if query_str == '':
        raise ValueError("Invalid query_str")
        
    # Find messages that match the query_str from all the channels the user has joined
    for channel in all_channels_details:
        for users in channel['all_members']:
                if users['u_id'] == get_user_from_token(token):
                    current_channel_id = channel['channel_id']
                    for message_channel_id in all_channels_messages:
                        if current_channel_id == message_channel_id['channel_id']:
                            message_list = message_channel_id['messages']
                            for message in message_list:
                                if query_str in message['message']:
                                    foundMessages.append({"channel_id": current_channel_id, "message_id": message['message_id'], "message": message['message']})
    return foundMessages

