import pytest
from datetime import datetime

'''
Assume an accepted password has the following requirements (A function called 
is_valid_password() will check against these requirements and return either True or False) :-
    
    - Passoword length between 5 and 20 characters inclusive
    - At least 1 upper character
    - At least 1 lower case character
    - At least 1 number
    - At least 1 special character
    
'''

@pytest.fixture
def registered_user_1():
    return auth_register("PokemonMaster@gmail.com", "validp@ssword", "Ash", "Ketcham")

@pytest.fixture
def registered_user_2():
    return auth_register("FreddieMercury.com", "ValidP@sswordQueen", "Freddie", "Mercury")
    
@pytest.fixture
def registered_user_3():
    return auth_register("TheRealPokemonMaster@gmail.com", "ValidP@sswordRocks", "Gary", "Oak")
   
    
@pytest.fixture
def channel_id_user_1(registered_user_1):
    return channels_create(registered_user_1['token'], "ValidChannelName", True)    
    
       
######TESTS FOR standup_start#######


def test_standup_start_correct_details(channel_id_user_1, registered_user_1):

    user_1_token = registered_user_1['token']
  
    channel_id = 1
    
    #Should produce no errors
    standup_start(user_1_token, channel_id_user_1)

    
    
def test_standup_start_nonexistant_channel(registered_user_1):
    
    user_token = registered_user_1['token']

    channel_id = "Nonexistant channnel"
    
    #Should produce ValueError as channel with channel_id = -1 does not exist
    with pytest.raises(ValueError):
        standup_start(user_token, channel_id)
        
        
def test_standup_start_unauthorised_user_access(channel_id_user_1, registered_user_2):

    user_token = registered_user_2['token']

    channel_id = channel_id_user_1
    
    #Should produce AccessError as the user is not a member of the channel
    with pytest.raises(AccessError):
        standup_start(user_token, channel_id)
        
     
def test_standup_start_time_finish_greater_than_time_current(channel_id_user_1, registered_user_1):
    
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
    
    #Testing if time_finish has a 15 minute differnce in time from time_current 
    assert(((time_finish.minute % 60) - (time_current.minute % 60)) == 15 or 
           ((time_finish.minute % 60) - (time_current.minute % 60)) == -15 )


######TESTS FOR standup_send#######   


def test_standup_send_valid_inputs__and_multiple_users(channel_id_user_1, registered_user_1, registered_user_2):
    
    #Start the standup
    
    user_token_1 = registered_user_1['token']
    user_token_2 = registered_user_2['token']
    
    channel_id = channel_id_user_1     
     
    channel_join(user_token_2, channel_id)   
    
    time_finish = standup_start(user_1_token, channel_id)
    
    #Should produce no error
    
    message = "This is a valid message"
          
    standup_send(user_token_1, channel_id, message)
    standup_send(user_token_2, channel_id, message)  
     
def test_standup_send_nonexistant_channel(channel_id_user_1, registered_user_1):
    
    #Start the standup
    
    user_token = registered_user_1['token']
    channel_id_1 = channel_id_user_1      
    time_finish = standup_start(user_token, channel_id_1)

    
    #Should produce ValueError as channel with channel_id = -1 does not exist
    
    channel_id_2 = "Nonexistant channel"
    
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
    
    user_token_2 = registered_user_3['token']
    message = "This is a valid message"
    
    with pytest.raises(AccessError):
        standup_send(user_token_2, channel_id, message)      
        
        
        
def test_standup_send_standup_time_finished(channel_id_user_1, registered_user_1):
    
    #Start the standup
    
    user_token = registered_user_1['token']
    channel_id = channel_id_user_1     
    time_finish = standup_start(user_token, channel_id)
    

    
    #Sleep 15 minutes
    sleep(900)
           
    time_current = datetime.now()       
    
    
    #Standup time should be finished so now sending a message to the standup should produce an AccessError even if the user belongs to the channel
    
    message = "This is a valid message"
    
    with pytest.raises(AccessError):
        standup_send(user_token, channel_id, message)   
        
        
        
        
        
