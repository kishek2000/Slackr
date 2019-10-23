from functions.Errors import AccessError
from .helper_functions import *
import datetime
import time
import threading

def standup_start(token, channel_id):
    
    #Check if valid channel
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Invalid Channel")
        
    #Check if user is in the channel
    
    if check_token_in_channel(token, channel_id) == False:
    
        raise AccessError("User Not In Channel")    
        
  	#Check if another standup is active
    for channel in all_channels_messages:
        if channel_id == channel['channel_id'] and channel['standup_active'] == True:
            
            raise ValueError("Channel Standup Already Active")
      		
            #If no errors raised then start the startup
        elif channel_id == channel['channel_id'] and channel['standup_active'] == False:
            
            channel['standup_active'] = True
	
            #Wait for 15 minutes then end the startup
            t = threading.Timer(60, end_standup_timer, [channel_id])
            t.start()
    
            return datetime.datetime.now() + datetime.timedelta(minutes = 1)     		
    
        		
def standup_send(token, channel_id, message):

	#Check if valid channel
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Invalid Channel")
        
    #Check if message is too long
    if len(message) > 1000:
        raise ValueError("Message too long")
    
    #Check if standup is active in the channel
    
    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            if channel['standup_active'] == False:
                raise ValueError("Channel Standup Inactive")
    
    #Check if user is in the channel
    
    if check_token_in_channel(token, channel_id) == False:
    
        raise AccessError("User Not In Channel")
      
    #Otherwise queue message to a standup buffer 
    
    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            channel['standup_buffer'] = channel['standup_buffer'] + ": " + message
            
def end_standup_timer(channel_id):
    
    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            channel['standup_active'] = False
     
            
