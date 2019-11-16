""" search_function """
# Written by Harry Wilson
import sys
sys.path.append("/Server/functions/")
from functions.helper_functions import all_channels_messages, get_user_from_token, all_channels_details
from functions.Errors import ValueError
def search(token, query_str):
    """ search_function """
    found_messages = {"messages": []}
    #Checking for valid query_str
    if query_str == '':
        raise ValueError("Invalid query_str")

    # Find messages that match the query_str from all the channels the user has joined
    for channel in all_channels_details:
        for users in channel['all_members']:
            if users['u_id'] == get_user_from_token(token):
                current_channel_id = channel['channel_id']
                for message_channel_id in all_channels_messages:
                    print (all_channels_messages)
                    if current_channel_id == message_channel_id['channel_id']:
                        message_list = message_channel_id['messages']
                        for message in message_list:
                            if query_str in message['message']:
                                found_messages['messages'].append(message)
    return found_messages
