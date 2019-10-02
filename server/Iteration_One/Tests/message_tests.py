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
    
    # Testing message that's too big
    with pytest.raises(ValueError):
        message_send(token, channel_id, "x"*1001)
    #CHECK NOTHING HAPPENED#
        
    # Testing message sent to nonexistant channel
    with pytest.raises(ValueError):
        message_send(token, -1, "Hello")
    #CHECK NOTHING HAPPENED#
      
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
    #CHECK NOTHING HAPPENED#
        
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_send("", -1, "x"*1001)
    #CHECK NOTHING HAPPENED#

def test_message_send_later():
    '''
    Some of these tests will fail on a slow computer - eg if it takes >1 second to compute some operations    
    '''

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
    
    # Testing message isn't sent prematurely
    message_send_later(token, channel_id, "Hello", time()+10)
    #CHECK ISN'T THERE#
    sleep(5)
    #CHECK ISN'T THERE#
    sleep(5)
    #CHECK IS THERE#
    
    # Testing empty message
    message_send_later(token, channel_id, "", time()+3) # This might raise an exception, idk
    sleep(3)
    #CHECK#
    
    # Testing message with time in the past
    with pytest.raises(ValueError):
        message_send_later(token, channel_id, "Hello", time()-1)
    #CHECK NOTHING HAPPENED#
    
    # Testing message that's too big
    with pytest.raises(ValueError):
        message_send_later(token, channel_id, "x"*1001, time()+2)
    #CHECK NOTHING HAPPENED#
    sleep(2)
    #CHECK NOTHING HAPPENED#
    
    # Testing message sent to nonexistant channel
    with pytest.raises(ValueError):
        message_send_later(token, -1, "Hello", time()+2)
    #CHECK NOTHING HAPPENED#
    sleep(2)
    #CHECK NOTHING HAPPENED#
        
    # Testing bad token
    with pytest.raises(Exception):
        message_send_later("", channel_id, "Hello", time()+2) # This probably raises an exception. Which one, idk
    #CHECK NOTHING HAPPENED#
    sleep(2)
    #CHECK NOTHING HAPPENED#
    
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_send_later("", -1, "x"*1001, time()-1)
    #CHECK NOTHING HAPPENED#

def test_message_remove():

def test_message_edit():

def test_message_react():

def test_message_unreact():

def test_message_pin():

def test_message_unpin():
