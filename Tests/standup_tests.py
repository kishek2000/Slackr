#################################################################################
##                              STANDUP TESTS                                  ##
#################################################################################

import pytest
from datetime import datetime
import sys
sys.path.append("Server/")
from functions.standup_functions import *

@pytest.fixture
def registered_user_1():
    return auth_register("PokemonMaster@gmail.com", "validp@ssword1", "Ash", "Ketcham")

@pytest.fixture
def registered_user_2():
    return auth_register("FreddieMercury@gmail.com", "ValidP@sswordQueen1", "Freddie", "Mercury")
    
@pytest.fixture
def registered_user_3():
    return auth_register("TheRealPokemonMaster@gmail.com", "ValidP@sswordRocks1", "Gary", "Oak")
    
@pytest.fixture #channel created by registered_user_1
def channel_id_user_1(registered_user_1): 
    return channels_create(registered_user_1['token'], "ValidChannelName", True)    
           
#################################################################################
##                           TESTING standup_start                             ##
#################################################################################

def test_standup_start_correct_details(channel_id_user_1, registered_user_1):

    user_1_token = registered_user_1['token']
  
    channel_id = channel_id_user_1
    
    #Should produce no errors
    standup_start(user_1_token, channel_id_user_1)
 

def test_standup_start_nonexistant_channel(registered_user_1):
    
    user_token = registered_user_1['token']

    channel_id = -1
    
    #Should produce ValueError as channel with channel_id = -1 does not exist
    with pytest.raises(ValueError):
        standup_start(user_token, channel_id)
        
        
def test_standup_start_unauthorised_user_access(channel_id_user_1, registered_user_2):

    user_token = registered_user_2['token']

    channel_id = channel_id_user_1
    
    #Should produce AccessError as the user is not a member of the channel
    with pytest.raises(AccessError):
        standup_start(user_token, channel_id)
        
     
def test_standup_start_time_finish_greaterThan_time_current(channel_id_user_1, registered_user_1):
    
    time_current = datetime.now()

    user_token = registered_user_1['token']
    channel_id = channel_id_user_1
    
    time_finish = standup_start(user_token, channel_id)
    
    #Testing if time_finish is greater than the time_current 
    assert((time_finish > time_current) == True)
    
  
def test_standup_start_correct_time_difference(channel_id_user_1, registered_user_1):
    
    time_current = datetime.now()

    user_token = registered_user_1['token']
    channel_id = channel_id_user_1
        
    time_finish = standup_start(user_token, channel_id)
    
    time_difference = time_finish - time_current 
    
    #Testing if time_finish has a 15 minute differnce in time from time_current 
    assert((time_difference.seconds/60) == 15)

#################################################################################
##                           TESTING standup_send                              ##
#################################################################################

def test_standup_send_valid(channel_id_user_1, registered_user_1, registered_user_2):
      
    user_token_1 = registered_user_1['token']
    channel_id = channel_id_user_1     
    
    #add registered_user_2 to the channel
    user_token_2 = registered_user_2['token']
    channel_join(user_token_2, channel_id)   
    
    #registered_user_1 starts the standup
    
    standup_start(user_token_1, channel_id)
    
    #Should produce no error as a valid message is sent by both registered_users during the standup
    
    message = "This is a valid message"
          
    standup_send(user_token_1, channel_id, message)
    standup_send(user_token_2, channel_id, message)  
     
def test_standup_send_nonexistant_channel(channel_id_user_1, registered_user_1):
    
    #Start the standup on the channel with channel id channel_id_user_1  
    
    user_token = registered_user_1['token']
    channel_id_1 = channel_id_user_1      
    standup_start(user_token, channel_id_1)
    
    #Should produce ValueError as channel with channel_id = -1 does not exist
    
    channel_id_2 = -1
    
    message = "This is a valid message"
    
    with pytest.raises(ValueError):
        standup_send(user_token, channel_id_2, message)


def test_standup_send_message_too_long(channel_id_user_1, registered_user_1):
    
    #Start the standup
    
    user_token = registered_user_1['token']
    channel_id = channel_id_user_1     
    time_finish = standup_start(user_token, channel_id)
    
    #Should produce ValueError as the message is greater than 1000 characters
    
    message = "x" * 1001 
        
    with pytest.raises(ValueError):
        standup_send(user_token, channel_id, message)     
        
        
def test_standup_send_unauthorised_user(channel_id_user_1, registered_user_1, registered_user_3):
    
    #Start the standup
    
    user_token_1 = registered_user_1['token']
    channel_id = channel_id_user_1    
    time_finish = standup_start(user_token_1, channel_id)
    
    
    #Should produce AccessError as the user is not a member of the channel
    
    user_token_3 = registered_user_3['token']
    message = "This is a valid message"
    
    with pytest.raises(AccessError):
        standup_send(user_token_3, channel_id, message)      
        
        
        
def test_standup_send_standup_time_finished(channel_id_user_1, registered_user_1):
    
    #Start the standup
    
    user_token = registered_user_1['token']
    channel_id = channel_id_user_1     
    standup_start(user_token, channel_id)
    
    #Sleep 15 minutes
    
    sleep(900)  
    
    #Standup time should be finished so now sending a message to the standup should produce
    #an AccessError even if the user sending a message to the standup belongs to the channel
    
    message = "This is a valid message"
    
    with pytest.raises(AccessError):
        standup_send(user_token, channel_id, message)   