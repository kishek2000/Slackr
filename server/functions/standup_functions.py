from functions.Errors import AccessError
from functions.helper_functions import *
import datetime
import time
import threading

#Assume length is in seconds
def standup_start(token, channel_id, length):
    
    #Check if valid channel
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Invalid Channel")
        
    #Check if user is in the channel
    
    if check_token_in_channel(token, channel_id) == False:
    
        raise AccessError("User Not In Channel")    
        
  	#Check if another standup is active
  	
    if standup_active(token, channel_id)['standup_active'] == True:
        raise ValueError("Channel Standup Already Active")
  	    
  	#If no errors raised then start the startup
    time_finish = datetime.datetime.now() + datetime.timedelta(seconds = int(length))
    start_standup(channel_id, time_finish)    
  	
  	#Wait for 'length' seconds then end the startup
    t = threading.Timer(int(length), end_standup, [channel_id])
    t.start()

    return time_finish    		

def standup_active(token, channel_id): 
    
    #Check if valid channel
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Invalid Channel")
        
    #Check if user is in the channel
    
    if check_token_in_channel(token, channel_id) == False:
    
        raise AccessError("User Not In Channel")       
    
    
    standup_details = standup_status(channel_id)  
        
    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            try:
                if channel['standup_active'][0] == True:
                    return {'standup_active' : standup_details['standup_active'],
                            'time_finish' : standup_details['time_finish']}
                
            except TypeError:
                continue            
                
                                            
    return {'standup_active' : False, 'time_finish' : None}

    '''
        
    standup_details = standup_status(channel_id)    
    
    if standup_details['time_finish'] is None:
    
        return {'standup_active' : standup_details['standup_active'],
                'time_finish' : standup_details['time_finish']}
                
    return {'standup_active' : standup_details['standup_active'],
            'time_finish' : int(standup_details['time_finish'].strftime('%s'))}
    '''
    
        		
def standup_send(token, channel_id, message):

	#Check if valid channel
    if check_valid_channel_id(channel_id) == False:
        raise ValueError("Invalid Channel")
        
    #Check if message is too long
    if len(message) > 1000:
        raise ValueError("Message too long")
    
    #Check if standup is active in the channel
    
    if standup_active(token, channel_id)['standup_active'] == False:
        raise ValueError("Channel Standup Already Active")
    
    #Check if user is in the channel
    
    if check_token_in_channel(token, channel_id) == False:
    
        raise AccessError("User Not In Channel")
      
    #Otherwise queue message to a standup buffer 
    
    add_to_standup_queue(channel_id, message)
        
    
          

            
