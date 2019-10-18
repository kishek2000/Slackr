from helper_functions import *
from Errors import AccessError

#====================================== channel/invite [POST] ======================================#
def channel_invite(token, channel_id, u_id):
    print("======+DEBUG - CHANNELS/INVITE =========")
    print("given token is")
    print(token)
    print("END OF DUMP")
    ## First make sure the given channel id, u_id and token are existing, and token is member of channel 
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_valid_u_id(u_id) == False:
        raise ValueError 
    if check_valid_token(token) == False:
        raise AccessError
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError ## accessing user's token is not part of the given channel
    if check_user_in_channel(u_id, channel_id) == True:
        raise ValueError ## invited user already in channel

    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if users['u_id'] == get_user_from_token(token):
                    new_user_dict = get_user_details(get_token_from_user(u_id))
                    channels['all_members'].append(new_user_dict)
                    break
#======================================= channel/details [GET] =======================================#
def channel_details(token, channel_id):
    ## First make sure the token is actually in the channel, and the channel id also is valid
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_valid_token(token) == False:
        raise AccessError
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError ## accessing user's token is not part of the given channel
        
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if check_token_matches_user(users['u_id'], token) == True:
                    return {'name': channels['name'], 'owner_members': channels['owner_members'], 'all_members': channels['all_members']}

#======================================= channel/messages [GET] =======================================#
def channel_messages(token, channel_id, start):
    ## First make sure the token is actually in the channel, and the channel id also is valid
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_valid_token(token) == False:
        raise AccessError
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
                increment = 50
                if start + increment == total_messages or total_messages < increment:
                    end = -1
                    increment = total_messages
                else:
                    end = start + increment
                print("this is the return dict:")
                print({messages['messages'][start:start+increment]})
                return {messages['messages'][start:start+increment], start, end}

#======================================= channel/leave [POST] =======================================#
def channel_leave(token, channel_id):
    ## First make sure the token is actually in the channel, and the channel id also is valid
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_valid_token(token) == False:
        raise AccessError
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError ## because token user not actually in requested channel id's channel
    
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for member in channels['all_members']:
                if check_token_matches_user(member['u_id'], token) == True:
                    del member
                    break

#======================================= channel/join [POST] ========================================#
def channel_join(token, channel_id):
    ## First make sure the token is not actually in the channel, and the channel id also is valid
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_valid_token(token) == False:
        raise AccessError
    if check_token_in_channel(token, channel_id) == True:
        raise ValueError ## because token user already in the channel 
    
    ## This function specifically lets all members to join publics, but only admins to join private 
    ## channel ids that are given as a destination

    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            if channels['is_public'] == False:
                print("This here is the list of users:")
                print(list_of_users)
                print("Now, here is what get user permission tells us:")
                print({'u_id': get_user_from_token(token), 'permission_id': get_user_permission(get_user_from_token(token))})
                if get_user_permission(get_user_from_token(token)) > 2:
                    raise AccessError ## because token user is not an admin or owner
                else:
                    new_user_dict = get_user_details(get_user_from_token(token))
                    channels['owner_members'].append(new_user_dict)
            else: 
                new_user_dict = get_user_details(get_user_from_token(token))
                channels['all_members'].append(new_user_dict)

#===================================== channel/addowner [POST] ======================================#
def channel_addowner(token, channel_id, u_id):
    ## First make sure the given channel id and u_id are existing, and token is owner of channel 
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_valid_u_id(u_id) == False:
        raise ValueError 
    if check_valid_token(token) == False:
        raise AccessError
    if get_user_permission(get_user_from_token(token)) != 1:
        raise AccessError ## accessing user's permission not owner status
    if check_token_in_channel(token, channel_id) == False:
        raise AccessError ## accessing user's token not in channel

    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['owner_members']:
                if u_id == users['u_id']:
                    raise ValueError ## since u_id given is already owner of channel 
                elif check_token_matches_user(users['u_id'], token) == True: ## implies token must be owner of channel
                    new_user_dict = get_user_details(get_token_from_user(u_id))
                    channels['owner_members'].append({'u_id': new_user_dict['u_id'], 'name_first': new_user_dict['name_first'], 'name_last': new_user_dict['name_last']})
                    channels['all_members'].append({'u_id': new_user_dict['u_id'], 'name_first': new_user_dict['name_first'], 'name_last': new_user_dict['name_last']})
                    break
    
#==================================== channel/removeowner [POST] ====================================#
def channel_removeowner(token, channel_id, u_id):
    ## First make sure the given channel id and u_id are existing, and token is owner of channel 
    if check_valid_channel_id(channel_id) == False:
        raise ValueError
    if check_valid_u_id(u_id) == False:
        raise ValueError 
    if check_valid_token(token) == False:
        raise AccessError
    if check_token_in_channel(token, channel_id) == False: 
        print("failed to find token in channel:")
        print(token, channel_id)

    ## or get_user_permission(get_user_from_token(token)) > 1:
        raise AccessError ## accessing user's token is not member of channel or owner of Slackr

    ## check to make sure that both the token user and user id given are both owners of the channel
    token_owner_of_channel = False
    user_owner_of_channel = False
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['owner_members']:
                print (users)
                if check_token_matches_user(users['u_id'], token) == True:
                    token_owner_of_channel = True
                    if user_owner_of_channel == True:
                        break
                if u_id == users['u_id']:
                    user_owner_of_channel = True
                    if token_owner_of_channel == True:
                        break            
    if user_owner_of_channel == False:
        raise ValueError ## because user given to remove is not an owner of the channel currently
    if token_owner_of_channel == False:
        raise ValueError ## because token user accessing remove is not owner of channel currently

    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['owner_members']:
                if u_id == users['u_id']:
                    del users 

#==================================== channels/list [GET] ====================================#
def channels_list(token):
    ## Make sure token is in fact existing first. 
    if check_valid_token(token) == False:
        raise AccessError
    returning_list = []
    u_id = get_user_from_token(token)
    for channels in all_channels_details:
        for users in channels['all_members']:
            if users['u_id'] == u_id:
                returning_list.append({'channel_id': channels['channel_id'], 'name': channels['name']})
                break
            else:
                continue
    print("Returning list is this:")
    print(returning_list)
    return returning_list

#=================================== channels/listall [GET] ==================================#
def channels_listall(token):
    ## Make sure token is in fact existing first. 
    if check_valid_token(token) == False:
        raise AccessError
    returning_list = []
    for channels in all_channels_details:
        returning_list.append({'channel_id': channels['channel_id'], 'name': channels['name']})
    return returning_list

#=================================== channels/create [POST] ==================================#
def channels_create(token, name, is_public):
    channel_id = generate_channel_id()
    if len(name) > 20:
        raise ValueError ## can't be having names above 20 chars!!
    name_first, name_last = get_name_from_token(token)
    full_name = get_name_from_token(token)
    name_first = full_name['name_first']
    name_last = full_name['name_last']
    u_id = get_user_from_token(token)
    all_channels_details.append({'channel_id': channel_id, 'name': name, 'owner_members':[{'u_id': u_id, 'name_first': name_first, 'name_last': name_last}], 'all_members':[{'u_id': u_id, 'name_first': name_first, 'name_last': name_last}], 'is_public': is_public})
    return channel_id
