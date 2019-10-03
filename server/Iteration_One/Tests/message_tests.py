## Created by Liam 1/10/19
## Last edited 3/10/19
## Status: ....xxxx
## Might need to add tests where a member is made an admin. This will add more tokens :(
import pytest

@pytest.fixture()
def setup():
    # Setting up
    a_id, a_token = get_data()['uid'], get_data()['token']
    b_id, b_token = get_data_two()['uid'], get_data_two()['token']
    channel_a = channels_create(a_token, "Channel A", False)
    channel_b = channels_create(b_token, "Channel B", True)    
    dead_channel = channels_create(token, "empty test", True) # Check to see if this channel is empty
    return [a_token, b_token, channel_a, channel_b, dead_channel]
   
   
################################################################################
##                           TESTING message_send                             ##
################################################################################
    
def test_message_send_max_length(setup):
    # Testing message of maximum length
    message_send(setup[0], setup[2], "x"*1000)
    #CHECK#
    
def test_message_send_too_big(setup):
    # Testing message that's too big
    with pytest.raises(ValueError):
        message_send(setup[0], setup[2] "x"*1001)
    #CHECK NOTHING HAPPENED#
        
def test_message_send_no_channel(setup):
    # Testing message sent to nonexistant channel
    with pytest.raises(ValueError):
        message_send(setup[0], -1, "Hello")
    #CHECK NOTHING HAPPENED#

def test_message_send_symbols(setup):
    # Testing weird characters
    message_send(setup[0], setup[2], "Testing All Character Types: 54, ][")
    #CHECK#

def test_message_send_special_characters(setup):
    message_send(setup[0], setup[2], "1\n2\0 3\b 4") # This should just be that straight message?
    #CHECK#
    
def test_message_send_empty(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_send(setup[0], setup[2], "")
    #CHECK NOTHING HAPPENED#

def test_message_send_spaces(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_send(setup[0], setup[2], "     ")
    #CHECK NOTHING HAPPENED#

def test_message_send_bad_token(setup):
    # Testing bad token
    with pytest.raises(Exception):
        message_send("", setup[2], "Hello") # This probably raises an exception. Which one, idk
    #CHECK NOTHING HAPPENED#
        
def test_message_send_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_send("", -1, "x"*1001)
    #CHECK NOTHING HAPPENED#
    

################################################################################
##                      TESTING message_send_later                            ##
################################################################################
    '''
    Some of these tests will fail on a slow computer - eg if it takes >1 second to compute some operations    
    '''
def test_message_send_later_max_length(setup):
    # Testing message of maximum length delivered on time
    message_send_later(setup[0], setup[2], "x"*1000, time()+5)
    sleep(5)
    #CHECK#
    
def test_message_send_later_current_time(setup):
    # Testing message of maximum length sent at current time
    message_send_later(setup[0], setup[2], "x"*1000, time())
    #CHECK#
    
def test_message_send_later_on_time(setup):
    # Testing message isn't sent prematurely
    message_send_later(setup[0], setup[2], "Hello", time()+10)
    #CHECK ISN'T THERE#
    sleep(5)
    #CHECK ISN'T THERE#
    sleep(5)
    #CHECK IS THERE#
    
def test_message_send_later_empty_message(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_send_later(setup[0], setup[2], "", time()+3)
    sleep(4)
    #CHECK NOTHING HAPENED#
    
def test_message_send_later_spaces(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_send_later(setup[0], setup[2], "     ", time()+3)
    sleep(4)
    #CHECK NOTHING HAPENED#
    
def test_message_send_later_time_past(setup):
    # Testing message with time in the past
    with pytest.raises(ValueError):
        message_send_later(setup[0], setup[2], "Hello", time()-1)
    #CHECK NOTHING HAPPENED#

def test_message_send_later_intermediate_messages(setup):
    # Testing message order is right when messages are sent before later message is sent
    message_send_later(setup[0], setup[2], "c", time()+10)
    message_send_later(setup[0], setup[2], "b", time()+5)
    message_send(setup[0], setup[2], "a")
    #CHECK ORDER IS ABC#
    
def test_message_send_later_too_big(setup):
    # Testing message that's too big
    with pytest.raises(ValueError):
        message_send_later(setup[0], setup[2], "x"*1001, time()+2)
    #CHECK NOTHING HAPPENED#
    sleep(3)
    #CHECK NOTHING HAPPENED#
    
def test_message_send_later_no_channel(setup):
    # Testing message sent to nonexistant channel
    with pytest.raises(ValueError):
        message_send_later(setup[0], -1, "Hello", time()+2)
    #CHECK NOTHING HAPPENED#
    sleep(3)
    #CHECK NOTHING HAPPENED#
        
def test_message_send_later_bad_token(setup):
    # Testing bad token
    with pytest.raises(Exception):
        message_send_later("", setup[2], "Hello", time()+2) # This probably raises an exception. Which one, idk
    #CHECK NOTHING HAPPENED#
    sleep(3)
    #CHECK NOTHING HAPPENED#
    
def test_message_send_later_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_send_later("", -1, "x"*1001, time()-1)
    #CHECK NOTHING HAPPENED#

################################################################################
##                         TESTING message_remove                             ##
################################################################################
    '''
    message_id to be replaced when I know howtf that's represented
    '''
    
def test_message_remove_empty(setup):
    # Testing deletion of no prior messages
    with pytest.raises(ValueError):
        message_remove(setup[0], message_id)
        #CHECK NOTHING HAPPENED
    
def test_message_remove_one_message(setup):
    # Testing deletion of one message
    message_send(setup[0], setup[2], "Hello")
    message_remove(setup[0], message_id)
    #CHECK#
    
def test_message_remove_two_messages_first(setup):
    # Testing deletion of first message
    message_send(setup[0], setup[2], "Hello")
    message_send(setup[0], setup[2], "There")
    message_remove(setup[0], message_id) # 'Hello'
    #CHECK#
    message_remove(setup[0], message_id) # 'There'
    #CHECK#
    
def test_message_remove_two_messages_second(setup):    
    # Testing deletion of second message
    message_send(setup[0], setup[2], "Hello")
    message_send(setup[0], setup[2], "There")
    message_remove(setup[0], message_id) # 'There'
    #CHECK#
    message_remove(setup[0], message_id) # 'Hello'
    #CHECK#
    
def test_message_remove_middle_mssage(setup):
    # Testing deletion of middle message
    message_send(setup[0], setup[2], "Hello")
    message_send(setup[0], setup[2], "There")
    message_send(setup[0], setup[2], "World")
    message_remove(setup[0], message_id) # 'There'
    #CHECK#
    message_remove(setup[0], message_id) # 'Hello'
    message_remove(setup[0], message_id) # 'World'
    #CHECK#
    
def test_message_remove_other_person(setup):
    # Testing deletion of message sent by another person
    message_send(setup[0], setup[2], "Hello")
    with pytest.raises(AccessError):
        message_remove(setup[1], message_id)
        #CHECK NOTHING HAPPENED#
        
def test_message_remove_admin_deletes_other_person(setup):
    # Testing deletion of a message sent by another person by an admin
    message_send(setup[1], setup[2], "Hello")
    message_remove(setup[0], message_id)
    #CHECK#

def test_message_remove_bad_token(setup):        
    # Testing deletion of message with bad token
    message_send(setup[0], setup[2], "Hello")
    with pytest.raises(AccessError):
        message_remove("", message_id)
        #CHECK NOTHING HAPPENED#
        
def test_message_remove_already_deleted(setup):
    # Testing deletion of already deleted message
    with pytest.raises(ValueError):
        message_remove(setup[0], message_id) # 'Hello' from the remove_one_message test
        #CHECK#

def test_message_remove_nonexistant(setup):
    # Testing removal of a nonexistant message
    with pytest.raises(ValueError):
        message_remove(setup[0], -1)
        #CHECK#

def test_message_remove_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_remove("", message_id)
        #CHECK#

################################################################################
##                         TESTING message_remove                             ##
################################################################################

    '''
    message_id to be replaced when I know howtf that's represented
    '''
    
def test_message_edit_no_messages(setup):
    with pytest.raises(ValueError):
        message_edit(setup[0], message_id, "b"*1000) # A plausible but missing message_id

def test_message_edit_max_lenght(setup):
    # Testing message of max length
    message_send(setup[0], setup[2], "a")
    message_edit(setup[0], message_id, "b"*1000)
    #CHECK#

def test_message_edit_too_big(setup):
    # Testing message of too long a length
    with pytest.raises(ValueError):
        message_send(setup[0], setup[2], "a")
        message_edit(setup[0], message_id, "b"*1001)

def test_message_edit_empty_message(setup):
    # Testing editing an empty message
    message_send(setup[0], setup[2], "a")
    with pytest.raises(ValueError):
        message_edit(setup[0], message_id, "")
    #CHECK NOTHING HAPPENED#
    
def test_message_edit_spaces(setup):
    # Testing editing an empty message
    message_send(setup[0], setup[2], "a")
    with pytest.raises(ValueError):
        message_edit(setup[0], message_id, "     ")
    #CHECK NOTHING HAPPENED#
    
def test_message_edit_other_person(setup):
    # Testing when editor did not post the message, and is not admin
    message_send(setup[0], setup[2], "Hello")
    with pytest.raises(ValueError):
        message_edit(setup[1], message_id, "World")
    #CHECK#
    
def test_message_edit_admin_edits_other_person(setup):
    # Testing when editor did not post the message, but is an admin
    message_send(setup[1], setup[2], "Edit this!")
    message_edit(setup[0], message_id, "Edited")
    #CHECK#

def test_message_edit_nonexistant(setup):
    # Testing editing a nonexistant message
    with pytest.raises(ValueError):
        message_edit(setup[0], -1, "Edited")
    #CHECK#
    
def test_message_edit_bad_token(setup):
    # Testing editing a message with bad token
    with pytest.raises(AccessError):
        message_edit("", message_id, "Edited
    #CHECK
    
def test_message_edit_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_edit("", -1, "")
    #CHECK#

def test_message_react():

def test_message_unreact():

def test_message_pin():

def test_message_unpin():
