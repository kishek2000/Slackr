from functions.Errors import AccessError
from functions.helper_functions import *
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
  	
    if check_standup_active(channel_id) == True:
        raise ValueError("Channel Standup Already Active")
  	    
  	#If no errors raised then start the startup
    start_standup(channel_id)    
  	
  	#Wait for 15 minutes then end the startup
    t = threading.Timer(60 * 15, end_standup, [channel_id])
    t.start()

    return datetime.datetime.now() + datetime.timedelta(minutes = 15)     		
 
        		
def standup_send(token, channel_id, message):

	#Check if valid channel
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Invalid Channel")
        
    #Check if message is too long
    if len(message) > 1000:
        raise ValueError("Message too long")
    
    #Check if standup is active in the channel
    
    if check_standup_active(channel_id) == False:
        raise ValueError("Channel Standup Inactive")
    
    #Check if user is in the channel
    
    if check_token_in_channel(token, channel_id) == False:
    
        raise AccessError("User Not In Channel")
      
    #Otherwise queue message to a standup buffer 
    
    add_to_standup_queue(channel_id, message)
        
    
          

            
