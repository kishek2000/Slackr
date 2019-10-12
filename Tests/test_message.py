## Created by Liam 1/10/19
## Last edited 1/10/19
## Status: Under Construction
import pytest

def test_message_send():
    # Setting up
    u_id, token = auth_register("email@email.com", "Password132", "Liam", "Staples")
    channel_id = channels_create(token, "test", False)
    
    # Testing message of maximum length
    message_send(token, channel_id, "x"*1000)
    #CHECK#
    
    with pytest.raises(ValueError):
        # Testing message that's too big
        message_send(token, channel_id, "x"*1001)
        
    with pytest.raises(ValueError):
        # Testing message sent to nonexistant channel
        message_send(token, -1, "Hello")
        
    # Testing weird characters
    message_send(token, channel_id, "Testing All Character Types: 54, ][")
    #CHECK#
    message_send(token, channel_id, "1\n2\0 3\b 4") # This should just be that straight message?
    #CHECK#
    
    # Testing empty message
    message_send(token, channel_id, "") # This might raise an exception, idk
    #CHECK#
    
    # Testing bad token
    with pytest.raises(Exception):
        message_send("", channel_id, "Hello") # This probably raises an exception. Which one, idk
        
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_send("", -1, "x"*1001)

def test_message_send_later():
    # Setting up
    u_id, token = auth_register("email@email.com", "Password132", "Liam", "Staples")
    channel_id = channels_create(token, "test", False)
    
    # Testing message of maximum length delivered on time
    message_send_later(token, channel_id, "x"*1000, time()+5)
    sleep(5)
    #CHECK#
    
    # Testing message of maximum length sent at current time
    message_send_later(token, channel_id, "x"*1000, time())
    #CHECK#
    
    # Testing message with time in the past
    with pytest.raises(ValueError):
        message_send_later(token, channel_id, "Hello", time()-1)
    
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_send_later("", -1, "x"*1001, time()-1)

def test_message_remove():

def test_message_edit():

def test_message_react():

def test_message_unreact():

def test_message_pin():

def test_message_unpin():
