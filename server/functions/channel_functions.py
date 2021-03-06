'''
channel_functions written by Adi!
-> channel_invite
-> channel_details
-> channel_messages
-> channel_leave
-> channel_join
-> channel_addowner
-> channel_removeowner
-> channels_list
-> channels_listall
-> channels_create
'''
from functions.helper_functions import check_token_matches_user, check_user_in_channel
from functions.helper_functions import all_channels_messages, all_channels_details
from functions.helper_functions import get_token_from_user, get_user_from_token
from functions.helper_functions import get_user_app_permission, get_user_channel_permission
from functions.helper_functions import get_user_details, generate_channel_id
from functions.helper_functions import change_user_channel_permission, message_reacts_helper
from functions.helper_functions import check_token_in_channel
from functions.Errors import AccessError, authorise_token, authorise_channel_id, token_in_channel
from functions.Errors import authorise_u_id, ValueError

#====================================== channel/invite [POST] ====================================#
@authorise_token
@authorise_channel_id
@authorise_u_id
@token_in_channel
def channel_invite(token=None, channel_id=None, u_id=None):
    ''' This function invites a given u_id to a channel that the token user is part of '''
    ## Extra check that is specific:
    if check_user_in_channel(u_id, channel_id):
        raise ValueError("Give user id already part of the channel.")
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if users['u_id'] == get_user_from_token(token):
                    new_user_dict = get_user_details(get_token_from_user(u_id))
                    channels['all_members'].append(new_user_dict)
                    if get_user_app_permission(u_id) <= 2:
                        channels['owner_members'].append(new_user_dict)
                        change_user_channel_permission(u_id, get_user_app_permission(u_id), channel_id)
                    else:
                        change_user_channel_permission(u_id, 3, channel_id)
                    break
#======================================= channel/details [GET] ====================================#
@authorise_token
@authorise_channel_id
@token_in_channel
def channel_details(token=None, channel_id=None):
    ''' This function provides the details of a channel that a token user is part of '''
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if check_token_matches_user(users['u_id'], token):
                    return {
                        'name': channels['name'], 'owner_members': channels['owner_members'],
                        'all_members': channels['all_members']
                    }
    return {}
#======================================= channel/messages [GET ===================================#
@authorise_token
@authorise_channel_id
@token_in_channel
def channel_messages(token=None, channel_id=None, start=None):
    ''' This function provides the messages of a channel that a token user is part of '''
    for messages in all_channels_messages:
        if channel_id == messages['channel_id']:
            if start > messages['total_messages']:
                raise ValueError ## because start exceeds total messages in the channel
            increment = 50
            uid = get_user_from_token(token)
            message_reacts_helper(messages["messages"][start:start+increment], uid)
            total = start + increment
            if total == messages['total_messages'] or messages['total_messages'] < increment:
                end = -1
                increment = messages['total_messages']
                if messages['total_messages'] == 0:
                    return {'messages': [], 'start': start, 'end': end}
                if start == increment - 1:
                    return {
                        'messages': [messages['messages'][start]],
                        'start': start, 'end': end
                    }
            else:
                end = start + increment
            return {
                'messages': messages['messages'][start:start+increment], 'start': start,
                'end': end
            }
    return {}
#======================================= channel/leave [POST] ====================================#
@authorise_token
@authorise_channel_id
@token_in_channel
def channel_leave(token=None, channel_id=None):
    ''' This function returns deletes the token user from the channel '''
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for member in channels['all_members']:
                if check_token_matches_user(member['u_id'], token):
                    channels['all_members'].remove(member)

    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for member in channels['owner_members']:
                if check_token_matches_user(member['u_id'], token):
                    channels['owner_members'].remove(member)
                    return

#======================================= channel/join [POST] =====================================#
@authorise_token
@authorise_channel_id
def channel_join(token=None, channel_id=None):
    ''' This function allows a token user to join a channel based on some constraints '''
    ## If the user is already in the channel, then we should have a valueerror:
    if check_token_in_channel(token, channel_id):
            raise ValueError("Accessing user is already in channel")
    ## This function specifically lets all members to join publics, but only admins to join private
    ## channel ids that are given as a destination
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            if not channels['is_public']:
                if get_user_app_permission(get_user_from_token(token)) > 2:
                    raise AccessError("You are not authorised to join this channel") ## because token user is not an admin or owner
                new_user_dict = get_user_details(token)
                channels['owner_members'].append(new_user_dict)
                channels['all_members'].append(new_user_dict)
                u_id = get_user_from_token(token)
                change_user_channel_permission(u_id, 1, channel_id)
            else:
                new_user_dict = get_user_details(token)
                channels['all_members'].append(new_user_dict)
                u_id = get_user_from_token(token)
                if get_user_app_permission(u_id) <= 2:
                    channels['owner_members'].append(new_user_dict)
                    change_user_channel_permission(u_id, get_user_app_permission(u_id), channel_id)
                else:
                    change_user_channel_permission(u_id, 3, channel_id)
                break

#===================================== channel/addowner [POST] ===================================#
@authorise_token
@authorise_channel_id
@authorise_u_id
def channel_addowner(token=None, channel_id=None, u_id=None):
    ''' This function allows an existing channel owner to add a new channel owner '''
    ## Extra checks that are specific:
    if get_user_app_permission(get_user_from_token(token)) != 1:
        if get_user_channel_permission(channel_id, get_user_from_token(token)) != 1:
            raise AccessError ## accessing user's permission not owner status of app, or owner
                              ## status in channel

    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['owner_members']:
                if u_id == users['u_id']:
                    raise ValueError ## since u_id given is already owner of channel
                if check_token_matches_user(users['u_id'], token): ## token must be channel owner
                    new_user_dict = get_user_details(get_token_from_user(u_id))
                    channels['owner_members'].append({
                        'u_id': new_user_dict['u_id'], 'name_first': new_user_dict['name_first'],
                        'name_last': new_user_dict['name_last'],
                        'profile_img_url': new_user_dict['profile_img_url']
                    })
                    change_user_channel_permission(u_id, 1, channel_id)
                    break

#==================================== channel/removeowner [POST] =================================#
@authorise_token
@authorise_channel_id
@authorise_u_id
def channel_removeowner(token=None, channel_id=None, u_id=None):
    ''' This function allows an existing channel owner to remove an existing channel owner '''
    ## Extra checks that are specific:
    user_app = get_user_app_permission(get_user_from_token(token))
    user_channel = get_user_channel_permission(channel_id, get_user_from_token(token))
    if user_app != 1 and user_channel != 1:
        raise AccessError ## accessing user's permission not owner status of app, or owner status
                          ## in channel
    if get_user_channel_permission(channel_id, u_id) != 1:
        raise ValueError ## user given to remove is not owner of channel currently.

    ## check to make sure that both the token user and user id given are both owners of the channel
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['owner_members']:
                if u_id == users['u_id']:
                    channels['owner_members'].remove(users)
                    change_user_channel_permission(u_id, 3, channel_id)
                    break


#==================================== channels/list [GET] ====================================#
@authorise_token
def channels_list(token=None):
    ''' This function returns the list of channels the token user is part of '''
    returning_list = []
    u_id = get_user_from_token(token)
    for channels in all_channels_details:
        for users in channels['all_members']:
            if users['u_id'] == u_id:
                returning_list.append({
                    'channel_id': channels['channel_id'], 'name': channels['name']
                })
                break
    return returning_list

#=================================== channels/listall [GET] ==================================#
@authorise_token
def channels_listall(token=None):
    ''' This function returns a list of all channels present in the Slackr app '''
    ## Token is completely unneeded in this function besides authorising it is existing. That is
    ## done by the decorator already.
    returning_list = []
    for channels in all_channels_details:
        returning_list.append({'channel_id': channels['channel_id'], 'name': channels['name']})
    return returning_list

#=================================== channels/create [POST] ==================================#
@authorise_token
def channels_create(token=None, name=None, is_public=None):
    ''' This function allows a token user to create a channel '''
    channel_id = generate_channel_id()
    if len(name) > 20:
        raise ValueError("Cannot create a channel with name more than 20 characters.")
    user_details = get_user_details(token)
    name_first = user_details['name_first']
    name_last = user_details['name_last']
    u_id = get_user_from_token(token)
    all_channels_details.append({
        'channel_id': channel_id, 'name': name, 'owner_members':[{
            'u_id': u_id, 'name_first': name_first, 'name_last': name_last,
            'profile_img_url': user_details['profile_img_url']
        }],
        'all_members':[{
            'u_id': u_id, 'name_first': name_first, 'name_last': name_last,
            'profile_img_url': user_details['profile_img_url']
        }],
        'is_public': is_public
    })
    all_channels_messages.append({
        'channel_id': channel_id, 'total_messages': 0, 
        'standup_details': {'standup_active' : False, 'time_finish': None},
        'standup_buffer': '', 'messages': []
    })
    change_user_channel_permission(u_id, 1, channel_id,)
    return channel_id
