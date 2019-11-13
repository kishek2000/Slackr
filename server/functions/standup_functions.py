'''
File contains standup related functions
'''

import datetime
import threading
from functions.Errors import AccessError
from functions.helper_functions import (check_valid_channel_id, check_token_in_channel, 
                                        add_to_standup_queue, all_channels_messages)
from functions.message_functions import message_send

#===============================================================================#
#============================= STANDUP DECORATORS ==============================#
#===============================================================================#


def authorise_standup_start(function):
    def wrapper(**kwargs):
        if check_valid_channel_id(kwargs['channel_id']) is False:
            raise ValueError("Invalid Channel")
        if check_token_in_channel(kwargs['token'], kwargs['channel_id']) is False:
            raise AccessError("User Not In Channel")
        if standup_active(token=kwargs['token'], channel_id=kwargs['channel_id'])['standup_active'] is True:
            raise ValueError("Channel Standup Already Active")
        return function(kwargs['token'], kwargs['channel_id'], kwargs['length'])
    return wrapper

def authorise_standup_active(function):
    def wrapper(**kwargs):
        if check_valid_channel_id(kwargs['channel_id']) is False:
            raise ValueError("Invalid Channel")
        if check_token_in_channel(kwargs['token'], kwargs['channel_id']) is False:
            raise AccessError("User Not In Channel")
        return function(kwargs['token'], kwargs['channel_id'])
    return wrapper
    
def authorise_standup_send(function):    
    def wrapper(**kwargs):
        if check_valid_channel_id(kwargs['channel_id']) is False:
            raise ValueError("Invalid Channel")
        if len(kwargs['message']) > 1000:
            raise ValueError("Message too long")
        if standup_active(token=kwargs['token'], channel_id=kwargs['channel_id'])['standup_active'] is False:
            raise ValueError("Channel Standup Already Active")
        if check_token_in_channel(kwargs['token'], kwargs['channel_id']) is False:
            raise AccessError("User Not In Channel")
        return function(kwargs['token'], kwargs['channel_id'], kwargs['message'])
    return wrapper
#===============================================================================#
#============================== STANDUP FUNCTIONS ==============================#
#===============================================================================#


@authorise_standup_start
def standup_start(token=None, channel_id=None, length=None, **kwargs):
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

@authorise_standup_active
def standup_active(token=None, channel_id=None):
    '''Function checks if a standup is active/inactive'''

    #standup_details = standup_status(channel_id)

    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
          #  try:
            if channel['standup_details']['standup_active'] is True:
                return {'standup_active' : channel['standup_details']['standup_active'],
                        'time_finish' : channel['standup_details']['time_finish']}

          #  except TypeError:
          #     continue


    return {'standup_active' : False, 'time_finish' : None}

@authorise_standup_send
def standup_send(token=None, channel_id=None, message=None):
    '''Functions sends a message to be buffered in the standup queue'''
  
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
    

