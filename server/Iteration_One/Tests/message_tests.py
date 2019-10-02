## Created by Liam 1/10/19
## Last edited 2/10/19
## Status: ....xxxx
## Might need to add tests where a member is made an admin
import pytest

def test_message_send():
    # Setting up
    u_id, token = auth_register("email@email.com", "Password132", "Liam", "Staples")
    channel_id = channels_create(token, "test", False)
    dead_channel = channels_create(token, "empty test", True) # Check to see if this channel is empty
    
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
    
    auth_logout(token)

def test_message_send_later():
    '''
    Some of these tests will fail on a slow computer - eg if it takes >1 second to compute some operations    
    '''

    # Setting up
    u_id, token = auth_register("email@email.com", "Password132", "Liam", "Staples")
    channel_id = channels_create(token, "test", False)
    dead_channel = channels_create(token, "empty test", True) # Check to see if this channel is empty
    
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
    sleep(4)
    #CHECK#
    
    # Testing message with time in the past
    with pytest.raises(ValueError):
        message_send_later(token, channel_id, "Hello", time()-1)
    #CHECK NOTHING HAPPENED#
    
    # Testing message that's too big
    with pytest.raises(ValueError):
        message_send_later(token, channel_id, "x"*1001, time()+2)
    #CHECK NOTHING HAPPENED#
    sleep(3)
    #CHECK NOTHING HAPPENED#
    
    # Testing message sent to nonexistant channel
    with pytest.raises(ValueError):
        message_send_later(token, -1, "Hello", time()+2)
    #CHECK NOTHING HAPPENED#
    sleep(3)
    #CHECK NOTHING HAPPENED#
        
    # Testing bad token
    with pytest.raises(Exception):
        message_send_later("", channel_id, "Hello", time()+2) # This probably raises an exception. Which one, idk
    #CHECK NOTHING HAPPENED#
    sleep(3)
    #CHECK NOTHING HAPPENED#
    
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_send_later("", -1, "x"*1001, time()-1)
    #CHECK NOTHING HAPPENED#
    
    auth_logout(token)

def test_message_remove():
    # Setting up
    a_id, a_token = auth_register("email@email.com", "Password132", "Liam", "Staples")
    b_id, b_token = auth_register("Buser@Buser.com", "BuserbUSER", "B", "User")
    channel_a = channels_create(a_token, "Channel A", False)
    channel_b = channels_create(b_token, "Channel B", True)    
    message_send(a_token, channel_b, "Hello")
    message_send(b_token, channel_b, "There")
    
    # Testing deletion of no prior messages
    with pytest.raises(ValueError):
        message_remove(a_token, messages[0]['message_id'])
    
    # Testing deletion of one message
    message_send(a_token, channel_a, "Hello")
    message_remove(a_token, messages[0]['message_id'])
    #CHECK#
    
    # Testing deletion of first message
    message_send(a_token, channel_a, "Hello")
    message_send(a_token, channel_a, "There")
    message_remove(a_token, messages[0]['message_id'])
    #CHECK#
    message_remove(a_token, messages[0]['message_id'])
    #CHECK#
    
    # Testing deletion of second message
    message_send(a_token, channel_a, "Hello")
    message_send(a_token, channel_a, "There")
    message_remove(a_token, messages[1]['message_id'])
    #CHECK#
    message_remove(a_token, messages[0]['message_id'])
    #CHECK#
    
    # Testing deletion of middle message
    message_send(a_token, channel_a, "Hello")
    message_send(a_token, channel_a, "There")
    message_send(a_token, channel_a, "World")
    message_remove(a_token, messages[1]['message_id'])
    #CHECK#
    message_remove(a_token, messages[0]['message_id'])
    message_remove(a_token, messages[0]['message_id'])
    #CHECK#
    
    # Testing deletion of message sent by another person
    message_send(a_token, channel_a, "Hello")
    with pytest.raises(AccessError):
        message_remove(b_token, messages[0]['message_id'])
        #CHECK#
        
    # Testing deletion of a message sent by another person by an admin
    message_send(b_token, channel_a, "Hello")
    message_remove(a_token, messages[1]['message_id'])
        
    # Testing deletion of message with bad token
    message_send(a_token, channel_a, "Hello")
    with pytest.raises(AccessError):
        message_remove("", messages[0]['message_id'])
        #CHECK#
        
    # Testing deletion of already deleted message
    with pytest.raises(ValueError):
        message_remove(a_token, messages[0]['message_id'])
        #CHECK#
        
    # Testing removal of a nonexistant message
    with pytest.raises(ValueError):
        message_remove(a_token, -1)
        #CHECK#
        
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_remove("", messages[0]['message_id'])
        #CHECK#
        
    auth_logout(a_token)
    auth_logout(b_token)

def test_message_edit():
    # Setting Up
    a_id, a_token = auth_register("email@email.com", "Password132", "Liam", "Staples")
    b_id, b_token = auth_register("Buser@Buser.com", "BUSERbuser", "B", "User")
    channel_a = channels_create(a_token, "Channel A", False)
    channel_b = channels_create(b_token, "Channel B", True)
    message_send(a_token, channel_b, "Hello")
    message_send(b_token, channel_b, "There")
    
    # Testing message of max length
    message_send(a_token, channel_a, "a")
    message_edit(a_token, messages[0]['message_id'], "b"*1000)
    #CHECK#
    
    # Testing message of too long a length
    with pytest.raises(ValueError):
        message_send(a_token, channel_a, "a")
        message_edit(a_token, messages[0]['message_id'], "b"*1001)
    
    # Testing editing an empty message
    message_send(a_token, channel_a, "a")
    message_edit(a_token, messages[0]['message_id'], "") # Dunno if this is an exception or not
    #CHECK#
    
    # Testing when editor did not post the message, and is not admin
    with pytest.raises(ValueError):
        message_edit(b_token, messages[0]['message_id'], "World")
    #CHECK#
    
    # Testing when editor did not post the message, but is an admin
    message_send(b_token, channel_a, "Edit this!")
    message_edit(a_token, messages[0]['message_id'], "Edited")
    #CHECK#
    
    # Testing editing a nonexistant message
    with pytest.raises(ValueError):
        message_edit(a_token, -1, "Edited")
    #CHECK#
    
    # Testing editing a message with bad token
    with pytest.raises(AccessError):
        message_edit("", messages[0]['message_id'], "Edited
    #CHECK
    
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_edit("", -1, "")
    #CHECK#
    
    auth_logout(a_token)
    auth_logout(b_token)

def test_message_react():

def test_message_unreact():

def test_message_pin():

def test_message_unpin():
