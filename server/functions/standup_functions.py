'''
File contains standup related functions
'''

import datetime
import threading
from functions.Errors import AccessError
from functions.helper_functions import (check_valid_channel_id, check_token_in_channel, 
                                        add_to_standup_queue, all_channels_messages,
                                        valid_channel_id)
from functions.message_functions import message_send

#===============================================================================#
#============================= STANDUP DECORATORS ==============================#
#===============================================================================#

def check_standup_active_true(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if standup_active(token=user_details['token'], 
                          channel_id=user_details['channel_id'])['standup_active'] is True:
            raise ValueError("Channel Standup Already Active")
        return function(*args, **kwargs)
    return wrapper

def check_standup_active_false(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if standup_active(token=user_details['token'], 
                          channel_id=user_details['channel_id'])['standup_active'] is False:
            raise ValueError("Channel Standup Already Active")
        return function(*args, **kwargs)
    return wrapper

def token_in_channel(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if check_token_in_channel(user_details['token'], user_details['channel_id']) is False:
            raise AccessError("User Not In Channel")
        return function(*args, **kwargs)
    return wrapper

#===============================================================================#
#=============================== STANDUP FUNCTIONS ==============================#
#===============================================================================#

@valid_channel_id
@token_in_channel
@check_standup_active_true
def standup_start(token=None, channel_id=None, length=None):
    '''Function starts a standup in a channel if inactive'''

  	#If no errors raised then start the startup
    time_finish = datetime.datetime.now() + datetime.timedelta(seconds=int(length))
    
    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            #channel['standup_active'] = [None, None]
            channel['standup_details']['standup_active'] = True
            channel['standup_details']['time_finish'] = time_finish

  	#Wait for 'length' seconds then end the startup
    threading_timer = threading.Timer(int(length), end_standup, [channel_id, token])
    threading_timer.start()

    return time_finish

@valid_channel_id
@token_in_channel
def standup_active(token=None, channel_id=None):
    '''Function checks if a standup is active/inactive'''
    
    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:

            if channel['standup_details']['standup_active'] is True:
                return {'standup_active' : channel['standup_details']['standup_active'],
                        'time_finish' : channel['standup_details']['time_finish']}


    return {'standup_active' : False, 'time_finish' : None}

@valid_channel_id
@token_in_channel
@check_standup_active_false
def standup_send(token=None, channel_id=None, message=None):
    '''Functions sends a message to be buffered in the standup queue'''

    if len(message) > 1000:
        raise ValueError("Message too long")

    message_send(token, channel_id, "Standup: " + message)
    
    add_to_standup_queue(channel_id, message)
    
    
def end_standup(channel_id, token):

    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            channel['standup_details']['standup_active'] = False    
            channel['standup_details']['time_finish'] = None 
            standup_summary = channel['standup_buffer']
            channel['standup_buffer'] = ''
    
    message_send(token, channel_id, "Standup Summary" + standup_summary)
            
    return {}   
