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
#============================== STANDUP FUNCTIONS ==============================#
#===============================================================================#


def standup_start(token, channel_id, length):
    '''Function starts a standup in a channel if inactive'''

    if check_valid_channel_id(channel_id) is False:
        raise ValueError("Invalid Channel")

    if check_token_in_channel(token, channel_id) is False:
        raise AccessError("User Not In Channel")

    if standup_active(token, channel_id)['standup_active'] is True:
        raise ValueError("Channel Standup Already Active")

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

def standup_active(token, channel_id):
    '''Function checks if a standup is active/inactive'''
    
    if check_valid_channel_id(channel_id) is False:
            raise ValueError("Invalid Channel")
            
    if check_token_in_channel(token, channel_id) is False:
        raise AccessError("User Not In Channel")
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


def standup_send(token, channel_id, message):
    '''Functions sends a message to be buffered in the standup queue'''
  
    if check_valid_channel_id(channel_id) is False:
        raise ValueError("Invalid Channel")
    if len(message) > 1000:
        raise ValueError("Message too long")
    if standup_active(token, channel_id)['standup_active'] is False:
        raise ValueError("Channel Standup Already Active")
    if check_token_in_channel(token, channel_id) is False:
        raise AccessError("User Not In Channel")

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
    

