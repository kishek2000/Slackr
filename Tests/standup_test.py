#################################################################################
##                              STANDUP TESTS                                  ##
#################################################################################

import pytest
import sys
sys.path.append('Server/')
from functions.standup_functions import *
from datetime import datetime
from functions.helper_functions import *
from functions.channel_functions import *
from functions.auth_functions import auth_register

@pytest.fixture
def setup():
    
    reset_data()
    
    user_1_details = auth_register("PokemonMaster@gmail.com", "validP@sswrd1", "Ash", "Ketcham")   
    user_2_details = auth_register("TheRealPokemonMaster@gmail.com", "ValidP@sswordRocks1", "Gary", "Oak")    
    user_3_details = auth_register("FreddieMercury@gmail.com", "We@reTheChampions123", "Freddie", "Mercury")
    
    
    user_1_created_channel_id = channels_create(user_1_details['token'], "ValidChannelName", True)    
    
    return {'user_1_u_id': user_1_details['u_id'], 'user_1_token' : user_1_details['token'],
            'user_2_u_id': user_2_details['u_id'], 'user_2_token' : user_2_details['token'],
            'user_3_u_id': user_3_details['u_id'], 'user_3_token' : user_3_details['token'],
            'channel_created_by_user_1' : user_1_created_channel_id}
      
           
#################################################################################
##                           TESTING standup_start                             ##
#################################################################################

def test_standup_start_correct_details(setup):

    user_1_token = setup['user_1_token']
  
    channel_id = setup['channel_created_by_user_1']
    
    #Should produce no errors
    standup_start(user_1_token, channel_id)
    
def test_standup_invalid_helpers(setup):
    assert check_standup_active(-1) == False
    assert start_standup(-1) == {}
    assert end_standup(-1) == {}
    assert add_to_standup_queue(-1, "hi") == {}
 
def test_standup_attempt_to_start_already_active_standup(setup):

    user_1_token = setup['user_1_token']
  
    channel_id = setup['channel_created_by_user_1']
    
    #Should produce no errors
    standup_start(user_1_token, channel_id)

    #Should produce ValueError as standup is already active
    with pytest.raises(ValueError):
        standup_start(user_1_token, channel_id)
 

def test_standup_start_nonexistant_channel(setup):
    
    user_1_token = setup['user_1_token']

    channel_id = -1
    
    #Should produce ValueError as channel with channel_id = -1 does not exist
    with pytest.raises(ValueError):
        standup_start(user_1_token, channel_id)
        
        
def test_standup_start_unauthorised_user_access(setup):

    user_2_token = setup['user_2_token']

    channel_id = setup['channel_created_by_user_1']
    
    #Should produce AccessError as the user is not a member of the channel
    with pytest.raises(AccessError):
        standup_start(user_2_token, channel_id)
        
     
def test_standup_start_time_finish_greaterThan_time_current(setup):
    
    time_current = datetime.datetime.now()

    user_1_token = setup['user_1_token']
    channel_id = setup['channel_created_by_user_1']
    
    time_finish = standup_start(user_1_token, channel_id)
    
    #Testing if time_finish is greater than the time_current 
    assert((time_finish > time_current) == True)
    
  
def test_standup_start_correct_time_difference(setup):
    
    time_current = datetime.datetime.now()

    user_1_token = setup['user_1_token']
    channel_id = setup['channel_created_by_user_1']
        
    time_finish = standup_start(user_1_token, channel_id)
    
    time_difference = time_finish - time_current 
    
    #Testing if time_finish has a 15 minute differnce in time from time_current 
    assert((time_difference.seconds/60) == 1)


#################################################################################
##                           TESTING standup_send                              ##
#################################################################################

def test_standup_send_valid(setup):
      
    user_1_token = setup['user_1_token']
    channel_id = setup['channel_created_by_user_1']   
    
    #add registered_user_2 to the channel
    user_2_token = setup['user_2_token']
    channel_join(user_2_token, channel_id)   
    
    #registered_user_1 starts the standup
    
    standup_start(user_1_token, channel_id)
    
    #Should produce no error as a valid message is sent by both registered_users during the standup
    
    message = "This is a valid message"
          
    standup_send(user_1_token, channel_id, message)
    standup_send(user_2_token, channel_id, message)  
     
def test_standup_send_nonexistant_channel(setup):
    
    #Start the standup on the channel with channel id channel_id_user_1  
    
    user_token = setup['user_1_token']
    channel_id_1 = setup['channel_created_by_user_1']      
    standup_start(user_token, channel_id_1)
    
    #Should produce ValueError as channel with channel_id = -1 does not exist
    
    channel_id_2 = -1
    
    message = "This is a valid message"
    
    with pytest.raises(ValueError):
        standup_send(user_token, channel_id_2, message)


def test_standup_send_message_too_long(setup):
    
    #Start the standup
    
    user_token = setup['user_1_token']
    channel_id = setup['channel_created_by_user_1']   
    time_finish = standup_start(user_token, channel_id)
    
    #Should produce ValueError as the message is greater than 1000 characters
    
    message = "x" * 1001 
        
    with pytest.raises(ValueError):
        standup_send(user_token, channel_id, message)     
        
        
def test_standup_send_unauthorised_user(setup):
    
    #Start the standup
    
    user_1_token = setup['user_1_token']
    channel_id = setup['channel_created_by_user_1'] 
    time_finish = standup_start(user_1_token, channel_id)
    
    
    #Should produce AccessError as the user is not a member of the channel
    
    user_3_token = setup['user_3_token']
    message = "This is a valid message"
    
    with pytest.raises(AccessError):
        standup_send(user_3_token, channel_id, message)      
        
        
        
def test_standup_send_standup_time_finished(setup):
    
    #Start the standup
    
    user_token = setup['user_1_token']
    channel_id = setup['channel_created_by_user_1']   
    standup_start(user_token, channel_id)
    
    #Sleep 15 minutes
    
    time.sleep(60)  
    
    #Standup time should be finished so now sending a message to the standup should produce
    #an AccessError even if the user sending a message to the standup belongs to the channel
    
    message = "This is a valid message"
    
    with pytest.raises(ValueError):
        standup_send(user_token, channel_id, message)   
