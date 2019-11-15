'''
File contains standup related functions
'''

import datetime
import threading
from functions.Errors import (authorise_channel_id, token_in_channel, ValueError)
from functions.helper_functions import (add_to_standup_queue, all_channels_messages)
from functions.message_functions import message_send


#===============================================================================#
#=============================== STANDUP FUNCTIONS ==============================#
#===============================================================================#

@authorise_channel_id
@token_in_channel
def standup_start(token=None, channel_id=None, length=None):
    '''Function starts a standup in a channel if inactive'''

    #Check is another standup
    if standup_active(token=token, channel_id=channel_id)['standup_active'] is True:
        raise ValueError("Channel Standup Already Active")

  	#If no errors raised then start the startup
    time_finish = datetime.datetime.now() + datetime.timedelta(seconds=int(length))

    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            #channel['standup_active'] = [None, None]
            channel['standup_details']['standup_active'] = True
            channel['standup_details']['time_finish'] = time_finish

  	#Wait for 'length' seconds then end the startup
    threading_timer = threading.Timer(length, end_standup, [channel_id, token])
    threading_timer.start()

    return time_finish

@authorise_channel_id
@token_in_channel
def standup_active(token=None, channel_id=None):
    '''Function checks if a standup is active/inactive'''

    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:

            if channel['standup_details']['standup_active'] is True:
                return {'standup_active' : channel['standup_details']['standup_active'],
                        'time_finish' : channel['standup_details']['time_finish']}
    return {'standup_active' : False, 'time_finish' : None}

@authorise_channel_id
@token_in_channel
def standup_send(token=None, channel_id=None, message=None):
    '''Functions sends a message to be buffered in the standup queue'''

    #Check if a standup is active to send a message
    if standup_active(token=token, channel_id=channel_id)['standup_active'] is False:
        raise ValueError("No Standup Active")

    if len(message) > 1000:
        raise ValueError("Message too long")

    message_send(token=token, channel_id=channel_id, message=("Standup: " + message))

    add_to_standup_queue(channel_id, message)


def end_standup(channel_id, token):
    '''Function ends a standup after its time has elapsed'''
    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            channel['standup_details']['standup_active'] = False
            channel['standup_details']['time_finish'] = None
            standup_summary = channel['standup_buffer']
            channel['standup_buffer'] = ''

    message_send(token=token, channel_id=channel_id, message=("Standup Summary" + standup_summary))

    return {}
