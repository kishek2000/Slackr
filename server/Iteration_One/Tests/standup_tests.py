import pytest
from datetime import datetime

######TESTS FOR standup_start#######

'''

Assume there is a channel with a channel_id = 1. In this channel, assume there are
3 users with the respective tokens "x", "y" and "z". 

Assume there is a user with a token "a" who does not belong to the channel with channel_id = 1

Assume there is no channel with a channel_id = -1


'''

def test_standup_start_correct_details():

    user_1_token = "x"
    user_2_token = "y"
    user_3_token = "z"
    
    channel_id = 1
    
    #Should produce no errors
    standup_start(user_1_token, channel_id)
    standup_start(user_2_token, channel_id)
    standup_start(user_3_token, channel_id)
    
    
def test_standup_start_nonexistant_channel():
    
    user_token = "x"

    channel_id = -1
    
    #Should produce ValueError as channel with channel_id = -1 does not exist
    with pytest.raises(ValueError):
        standup_start(user_token, channel_id)
        
        
def test_standup_start_unauthorised_user_access():

    user_token = "a"

    channel_id = 1
    
    #Should produce AccessError as the user is not a member of the channel
    with pytest.raises(AccessError):
        standup_start(user_token, channel_id)
        
     
def test_standup_start_time_finish_greater_than_time_current():
    
    time_current = datetime.now()

    user_token = "x"
    channel_id = 1
    
    time_finish = standup_start(user_token, channel_id)
    
    #Testing if time_finish is greater than the time_current 
    assert((time_finish > time_current) == True)
    
  
def test_standup_start_correct_time_difference():
    
    time_current = datetime.now()

    user_token = "x"
    channel_id = 1   
    
    time_finish = standup_start(user_token, channel_id)
    
    #Testing if time_finish has a 15 minute differnce in time from time_current 
    assert(((time_finish.minute % 60) - (time_current.minute % 60)) == 15 or 
           ((time_finish.minute % 60) - (time_current.minute % 60)) == -15 )


######TESTS FOR standup_send#######   

'''

Assume there is a channel with a channel_id = 1. In this channel, assume there are
3 users with the respective tokens "x", "y" and "z". 

Assume there is a user with a token "a" who does not belong to the channel with channel_id = 1

Assume there is no channel with a channel_id = -1


'''

def test_standup_send_valid_inputs():
    
    #Start the standup
    
    user_token_1 = "x"
    channel_id = 1      
    time_finish = standup_start(user_1_token, channel_id)
    
    #Should produce no errors
    
    message = "This is a valid message"
    user_token_2 = "y"
    user_token_3 = "z"
        
    standup_send(user_token_1, channel_id, message)
    standup_send(user_token_2, channel_id, message) 
    standup_send(user_token_3, channel_id, message) 
     
def test_standup_send_nonexistant_channel():
    
    #Start the standup
    
    user_token = "x"
    channel_id_1 = 1      
    time_finish = standup_start(user_token, channel_id_1)

    
    #Should produce ValueError as channel with channel_id = -1 does not exist
    
    channel_id_2 = -1
    
    message = "This is a valid message"
    
    with pytest.raises(ValueError):
        standup_send(user_token, channel_id_2, message)


def test_standup_send_message_too_long():
    
    #Start the standup
    
    user_token = "x"
    channel_id = 1      
    time_finish = standup_start(user_token, channel_id)
    
    #Should produce ValueError as the message is greater than 1000 characters
    
    message = "x" * 1001 
        
    with pytest.raises(ValueError):
        standup_send(user_token, channel_id, message)     
        
        
def test_standup_send_unauthorised_user():
    
    #Start the standup
    
    user_token_1 = "x"
    channel_id = 1      
    time_finish = standup_start(user_token_1, channel_id)
    
    
    #Should produce AccessError as the user is not a member of the channel
    
    user_token_2 = "a"
    message = "This is a valid message"
    
    with pytest.raises(AccessError):
        standup_send(user_token_2, channel_id, message)      
        
        
        
def test_standup_send_standup_time_finished():
    
    #Start the standup
    
    user_token = "x"
    channel_id = 1      
    time_finish = standup_start(user_token, channel_id)
    
    time_current = datetime.now()
    
    #Loops until the time_current is past 15 minutes fromcd time_finish
    while (((time_finish.minute % 60) - (time_current.minute % 60)) < 15 or 
           ((time_finish.minute % 60) - (time_current.minute % 60)) > -15 )):
           
        time_current = datetime.now()       
    
    
    #After the loop, the standup time should be finished so now sending a message to the standup 
    #should produce an AccessError even if the user belongs to the channel
    
    message = "This is a valid message"
    
    with pytest.raises(AccessError):
        standup_send(user_token, channel_id, message)   
        
        
        
        
        
