from helper_functions import *

#====================================== channel/invite [POST] ======================================#
def channel_invite(token, channel_id, u_id):
    ## First make sure the given channel id and u_id are existing, and token is member of channel 
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_valid_u_id(u_id) == False:
        raise ValueError 
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError ## accessing user's token is not part of the given channel

    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if check_token_matches_user(users['u_id'], token) == True:
                    new_user_dict = get_user_details(u_id)
                    channels['all_members'].append(new_user_dict)

#======================================= channel/details [GET] =======================================#
def channel_details(token, channel_id):
    ## First make sure the token is actually in the channel, and the channel id also is valid
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError ## accessing user's token is not part of the given channel
        
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if check_token_matches_user(users['u_id'], token) == True:
                    return {channels['name'], channels['owner_members'], channels['all_members']}

#======================================= channel/messages [GET] =======================================#
def channel_messages(token, channel_id, start):
    ## First make sure the token is actually in the channel, and the channel id also is valid
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError ## because token user not actually in requested channel id's channel
    
    total_messages = 0
    for messages in all_channels_messages:
        if channel_id == messages['channel_id']:
            if start > messages['total_messages']:
                raise ValueError ## because start exceeds total messages in the channel
            else:
                ## Let us assume for now that the messages will be sorted correctly by time of sending, 
                ## and that the first index (0) will be the most recent message
                if start + 50 == total_messages:
                    end = -1
                else:
                    end = start + 50
                return {messages['messages'][start:start+50], end}

#======================================= channel/leave [POST] =======================================#
def channel_leave(token, channel_id):
    ## First make sure the token is actually in the channel, and the channel id also is valid
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError ## because token user not actually in requested channel id's channel
    
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for member in channels['all_members']:
                if check_token_matches_user(member['u_id'], token) == True:
                    del member



