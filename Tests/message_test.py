## Created by Liam 1/10/19
## Last edited 19/10/19
## Status: ........
## Might need to add tests where a member is made an admin. This will add more tokens :(
## Also the private/public channel differences, if any
import pytest
import sys
from datetime import date, time, datetime
import time
sys.path.append('server/')
from functions.message_functions import *
from functions.auth_functions import auth_register
from functions.channel_functions import channel_messages, channels_create, channel_invite, channel_join, channel_leave
from functions.helper_functions import get_total_channel_messages, reset_data, all_channels_details

@pytest.fixture()
def setup():
    reset_data()
    # Setting up
    a_info = auth_register("userA@userA.com", "Go0dPa>sword", "User", "A")
    a_id = a_info['u_id']
    token_a = a_info['token']
    b_info = auth_register("userB@userB.com", "Go0dPa>sword", "User", "B")
    b_id = b_info['u_id']
    token_b = b_info['token']
    channel_a = channels_create(token_a, "Channel A", False)
    channel_b = channels_create(token_b, "Channel B", True)    
    channel_invite(token_a, channel_a, b_id)
    channel_join(token_a, channel_b)
    channel_dead = channels_create(token_a, "empty test", True) # Check to see if this channel is empty
    return {"token_a": token_a, "token_b": token_b, "channel_a": channel_a, "channel_b": channel_b, "channel_dead": channel_dead, "a_id": a_id, "b_id": b_id}
   
def channel_is_empty(channel_id):
    return get_total_channel_messages(channel_id) == 0

   
################################################################################
##                           TESTING message_send                             ##
################################################################################
    
def test_message_send_max_length(setup):
    # Testing message of maximum length
    message_send(setup["token_a"], setup["channel_a"], "x"*1000)
    print(channel_messages(setup["token_a"], setup["channel_a"], 0))
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "x"*1000)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["u_id"] == setup["a_id"])
    #assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["time_created"] == time.time())
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == False)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"] == [])
    
def test_message_send_too_big(setup):
    # Testing message that's too big
    with pytest.raises(ValueError):
        message_send(setup["token_a"], setup["channel_a"], "x"*1001)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_send_no_channel(setup):
    # Testing message sent to nonexistant channel
    with pytest.raises(ValueError):
        message_send(setup["token_a"], -1, "Hello")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_send_symbols(setup):
    # Testing weird characters
    message_send(setup["token_a"], setup["channel_a"], "Testing All Character Types: 54, ][")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Testing All Character Types: 54, ][")

def test_message_send_special_characters(setup):
    message_send(setup["token_a"], setup["channel_a"], "1\n2\0 3\b 4 \\") # This should just be that straight message?
    #CHECK#
    
def test_message_send_thrice(setup):
    message_send(setup["token_a"], setup["channel_a"], "a")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "a")
    message_send(setup["token_a"], setup["channel_a"], "b")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][1]["message"] == "a")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "b")
    message_send(setup["token_a"], setup["channel_a"], "c")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][2]["message"] == "a")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][1]["message"] == "b")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "c")
    
def test_message_send_empty(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_send(setup["token_a"], setup["channel_a"], "")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_send_spaces(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_send(setup["token_a"], setup["channel_a"], "     ")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_send_not_in_channel(setup):
    # Testing editing a message in a channel without being in that channel
    channel_leave(setup["token_b"], setup["channel_a"])
    with pytest.raises(AccessError):
        message_send(setup["token_b"], setup["channel_a"], "I can't hear you")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))   

def test_message_send_bad_token(setup):
    # Testing bad token
    with pytest.raises(AccessError):
        message_send("", setup["channel_a"], "Hello")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_send_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_send("", -1, "x"*1001)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    

################################################################################
##                      TESTING message_sendlater                            ##
################################################################################
    '''
    Some of these tests will fail on a slow computer - eg if it takes >1 second to compute some operations    
    '''
def test_message_sendlater_max_length(setup):
    # Testing message of maximum length delivered on time
    message_sendlater(setup["token_a"], setup["channel_a"], "x"*1000, time.time()+5)
    time.sleep(6)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "x"*1000)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["u_id"] == setup["a_id"])
    #assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["time_created"] == time.time())
    
def test_message_sendlater_current_time(setup):
    # Testing message of maximum length sent at current time
    with pytest.raises(ValueError):
        message_sendlater(setup["token_a"], setup["channel_a"], "x"*1000, time.time())
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_sendlater_on_time(setup):
    # Testing message isn't sent prematurely
    message_sendlater(setup["token_a"], setup["channel_a"], "Hello", time.time()+10)
    assert(channel_is_empty(setup["channel_a"]))
    time.sleep(5)
    assert(channel_is_empty(setup["channel_a"]))
    time.sleep(5)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Hello")
    #assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["time_created"] == time.time())
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_sendlater_empty_message(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_sendlater(setup["token_a"], setup["channel_a"], "", time.time()+3)
    time.sleep(4)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_sendlater_spaces(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_sendlater(setup["token_a"], setup["channel_a"], "     ", time.time()+3)
    time.sleep(4)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_sendlater_time_past(setup):
    # Testing message with time in the past
    with pytest.raises(ValueError):
        message_sendlater(setup["token_a"], setup["channel_a"], "Hello", time.time()-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_intermediate_messages(setup):
    # Testing message order is right when messages are sent before later message is sent
    message_sendlater(setup["token_a"], setup["channel_a"], "c", time.time()+10)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    message_sendlater(setup["token_a"], setup["channel_a"], "b", time.time()+5)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    message_send(setup["token_a"], setup["channel_a"], "a")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "a")
    time.sleep(6)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][1]["message"] == "a")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "b")
    time.sleep(5)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][2]["message"] == "a")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][1]["message"] == "b")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "c")
    
def test_message_sendlater_too_big(setup):
    # Testing message that's too big
    with pytest.raises(ValueError):
        message_sendlater(setup["token_a"], setup["channel_a"], "x"*1001, time.time()+2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(3)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_sendlater_no_channel(setup):
    # Testing message sent to nonexistant channel
    with pytest.raises(ValueError):
        message_sendlater(setup["token_a"], -1, "Hello", time.time()+2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(3)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_not_in_channel(setup):
    # Testing editing a message in a channel without being in that channel
    channel_leave(setup["token_b"], setup["channel_a"])
    with pytest.raises(AccessError):
        message_sendlater(setup["token_b"], setup["channel_a"], "I can't hear you", time.time()+1)
    time.sleep(2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))   
        
def test_message_sendlater_bad_token(setup):
    # Testing bad token
    with pytest.raises(AccessError):
        message_sendlater("", setup["channel_a"], "Hello", time.time()+2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(3)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_sendlater_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_sendlater("", -1, "x"*1001, time.time()-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                         TESTING message_remove                             ##
################################################################################
    
def test_message_remove_empty(setup):
    # Testing deletion of no prior messages
    with pytest.raises(ValueError):
        message_remove(setup["token_a"], 0)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_remove_one_message(setup):
    # Testing deletion of one message
    message_id = message_send(setup["token_a"], setup["channel_a"], "Hello")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_remove_two_messages_first(setup):
    # Testing deletion of first message
    message_id_1 = message_send(setup["token_a"], setup["channel_a"], "Hello")
    message_id_2 = message_send(setup["token_a"], setup["channel_a"], "There")
    message_remove(setup["token_a"], message_id_1) # 'Hello'
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "There")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["u_id"] == setup["a_id"])
    #assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["time_created"] == time.time())
    message_remove(setup["token_a"], message_id_2) # 'There'
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_remove_two_messages_second(setup):    
    # Testing deletion of second message
    message_id_1 = message_send(setup["token_a"], setup["channel_a"], "Hello")
    message_id_2 = message_send(setup["token_a"], setup["channel_a"], "There")
    message_remove(setup["token_a"], message_id_2) # 'There'
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Hello")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["u_id"] == setup["a_id"])
    #assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["time_created"] == time.time())
    message_remove(setup["token_a"], message_id_1) # 'Hello'
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_remove_middle_mssage(setup):
    # Testing deletion of middle message
    message_id_1 = message_send(setup["token_a"], setup["channel_a"], "Hello")
    message_id_2 = message_send(setup["token_a"], setup["channel_a"], "There")
    message_id_3 = message_send(setup["token_a"], setup["channel_a"], "World")
    message_remove(setup["token_a"], message_id_2) # 'There'
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "World")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][1]["message"] == "Hello")
    message_remove(setup["token_a"], message_id_1) # 'Hello'
    message_remove(setup["token_a"], message_id_3) # 'World'
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_remove_other_person(setup):
    # Testing deletion of message sent by another person
    message_id = message_send(setup["token_a"], setup["channel_a"], "Hello")
    with pytest.raises(AccessError):
        message_remove(setup["token_b"], message_id)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Hello")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_remove_admin_deletes_other_person(setup):
    # Testing deletion of a message sent by another person by an admin
    message_id = message_send(setup["token_b"], setup["channel_a"], "Hello")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_not_in_channel(setup):
    # Testing editing a message in a channel without being in that channel
    channel_leave(setup["token_b"], setup["channel_a"])
    message_id = message_send(setup["token_a"], setup["channel_a"], "Remove this")
    with pytest.raises(AccessError):
        message_remove(setup["token_b"], message_id)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Remove this")
    message_remove(setup["token_a"], message_id)    
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))    

def test_message_remove_bad_token(setup):        
    # Testing deletion of message with bad token
    message_id = message_send(setup["token_a"], setup["channel_a"], "Hello")
    with pytest.raises(AccessError):
        message_remove("", message_id)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Hello")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_remove_already_deleted(setup):
    # Testing deletion of already deleted message
    message_id = message_send(setup["token_a"], setup["channel_a"], "Hello")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    with pytest.raises(ValueError):
        message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_nonexistant(setup):
    # Testing removal of a nonexistant message
    with pytest.raises(ValueError):
        message_remove(setup["token_a"], -1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_sendlater(setup):
    # Testing removal of a message that hasn't been sent yet
    message_id = message_sendlater(setup["token_a"], setup["channel_a"], "Hello", time.time()+5)
    with pytest.raises(ValueError):
        message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(6)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Hello")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_remove("", -1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                          TESTING message_edit                              ##
################################################################################
    
def test_message_edit_no_messages(setup):
    with pytest.raises(ValueError):
        message_edit(setup["token_a"], 42, "b"*1000) # A plausible but missing message_id
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_max_length(setup):
    # Testing message of max length
    message_id = message_send(setup["token_a"], setup["channel_a"], "a")
    message_edit(setup["token_a"], message_id, "b"*1000)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "b"*1000)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_too_big(setup):
    # Testing message of too long a length
    message_id = message_send(setup["token_a"], setup["channel_a"], "a")
    with pytest.raises(ValueError):
        message_edit(setup["token_a"], message_id, "b"*1001)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "a")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_empty_message(setup):
    # Testing editing an empty message
    message_id = message_send(setup["token_a"], setup["channel_a"], "a")
    with pytest.raises(ValueError):
        message_edit(setup["token_a"], message_id, "")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "a")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_edit_spaces(setup):
    # Testing editing an empty message
    message_id = message_send(setup["token_a"], setup["channel_a"], "a")
    with pytest.raises(ValueError):
        message_edit(setup["token_a"], message_id, "     ")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "a")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_edit_other_person(setup):
    # Testing when editor did not post the message, and is not admin
    message_id = message_send(setup["token_a"], setup["channel_a"], "Hello")
    with pytest.raises(AccessError):
        message_edit(setup["token_b"], message_id, "World")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Hello")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_edit_admin_edits_other_person(setup):
    # Testing when editor did not post the message, but is an admin
    message_id = message_send(setup["token_b"], setup["channel_a"], "Edit this!")
    message_edit(setup["token_a"], message_id, "Edited")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Edited")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_nonexistant(setup):
    # Testing editing a nonexistant message
    with pytest.raises(ValueError):
        message_edit(setup["token_a"], -1, "Edited")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_edit_not_in_channel(setup):
    # Testing editing a message in a channel without being in that channel
    channel_leave(setup["token_b"], setup["channel_a"])
    message_id = message_send(setup["token_a"], setup["channel_a"], "Edit this")
    with pytest.raises(AccessError):
        message_edit(setup["token_b"], message_id, "Edited")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Edit this")
    message_remove(setup["token_a"], message_id)    
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))    
    
def test_message_edit_bad_token(setup):
    # Testing editing a message with bad token
    message_id = message_send(setup["token_a"], setup["channel_a"], "Edit this")
    with pytest.raises(AccessError):
        message_edit("", message_id, "Edited")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "Edit this")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_edit_sendlater(setup):
    # Testing editing of a message that hasn't been sent yet
    message_id = message_sendlater(setup["token_a"], setup["channel_a"], "Hello", time.time()+5)
    with pytest.raises(ValueError):
        message_edit(setup["token_a"], message_id, "There")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(6)
    message_edit(setup["token_a"], message_id, "There")
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["message"] == "There")
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))  
      
def test_message_edit_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_edit("", -1, "")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                          TESTING message_react                             ##
################################################################################

def test_message_react_normal(setup):
    # Testing normal scenario
    message_id = message_send(setup["token_a"], setup["channel_a"], "Who's down to clown?")
    message_react(setup["token_a"], message_id, 1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_react_to_another(setup):
    # Testing reacting to another person's message
    message_id = message_send(setup["token_a"], setup["channel_a"], "Who's down to clown?")
    message_react(setup["token_b"], message_id, 1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["b_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_react_no_message(setup):
    # Testing reacting to no message
    with pytest.raises(ValueError):
        message_react(setup["token_a"], 1, 1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_react_not_in_channel(setup):
    # Testing reacting to a message in a channel without being in that channel
    channel_leave(setup["token_b"], setup["channel_a"])
    print(all_channels_details)
    message_id = message_send(setup["token_a"], setup["channel_a"], "React to this")
    with pytest.raises(AccessError):
        message_react(setup["token_b"], message_id, 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"] == [])
    message_remove(setup["token_a"], message_id)    
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_react_bad_react(setup):
    # Testing trying to react to a nonexistant react_id
    message_id = message_send(setup["token_a"], setup["channel_a"], "Give me a -1!")
    with pytest.raises(ValueError):
        message_react(setup["token_a"], message_id, -1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"] == [])
    message_remove(setup["token_a"], message_id)   
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"])) 
    
def test_message_react_same_twice(setup):
    # Testing someone reacting to the same message twice
    message_id = message_send(setup["token_a"], setup["channel_a"], "Bring in the reacts")
    message_react(setup["token_a"], message_id, 1)
    with pytest.raises(ValueError):
        message_react(setup["token_a"], message_id, 1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_react_same_different_people(setup):
    # Testing two people using the same react on the same message
    message_id = message_send(setup["token_a"], setup["channel_a"], "Bring in the reacts")
    message_react(setup["token_a"], message_id, 1)
    message_react(setup["token_b"], message_id, 1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"], setup["b_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_two_different_reacts(setup):
    # Testing two different reacts on the same message
    message_id = message_send(setup["token_a"], setup["channel_a"], "Bring in the reacts")
    message_react(setup["token_a"], message_id, 1)
    message_react(setup["token_a"], message_id, 2)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 2)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][1]["react_id"] == 2)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_react_bad_token(setup):
    # Testing message_react with a bad token
    message_id = message_send(setup["token_a"], setup["channel_a"], "Helllo")
    with pytest.raises(AccessError):
        message_react("", message_id, 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"] == [])
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_react_disaster(setup):
    # Testing the worst case scenario
    with pytest.raises(Exception):
        message_react("", -1, -1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                         TESTING message_unreact                            ##
################################################################################

def test_message_unreact_no_message(setup):
    # Testing unreacting to no messages
    with pytest.raises(ValueError):
        message_unreact(setup["token_a"], 1, 1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_no_react(setup):
    # Testing unreacting to a message that wasn't reacted.
    message_id = message_send(setup["token_a"], setup["channel_a"], "Darn tests")
    with pytest.raises(ValueError):
        message_unreact(setup["token_a"], message_id, 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"] == [])
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_unreact_normal(setup):
    # Testing normal scenario
    message_id = message_send(setup["token_a"], setup["channel_a"], "Who's down to clown?")
    message_react(setup["token_a"], message_id, 1)
    message_unreact(setup["token_a"], message_id, 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"] == [])
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unreact_to_another(setup):
    # Testing unreacting a message someone else (but not you) reacted to
    message_id = message_send(setup["token_a"], setup["channel_a"], "Who's down to clown?")
    message_react(setup["token_a"], message_id, 1)
    with pytest.raises(ValueError):
        message_unreact(setup["token_b"], message_id, 1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unreact_wrong_react_id(setup):
    # Testing unreacting a reacted message with the wrong reaction
    message_id = message_send(setup["token_a"], setup["channel_a"], "Who's down to clown?")
    message_react(setup["token_a"], message_id, 1)
    with pytest.raises(ValueError):
        message_unreact(setup["token_a"], message_id, 2)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unreact_bad_react_id(setup):
    # Testing unreacting to a bad react id
    message_id = message_send(setup["token_a"], setup["channel_a"], "Who's down to clown?")
    message_react(setup["token_a"], message_id, 1)
    with pytest.raises(ValueError):
        message_unreact(setup["token_a"], message_id, -1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_twice(setup):
    # Testing unreacting twice on the same message
    message_id = message_send(setup["token_a"], setup["channel_a"], "Who's down to clown?")
    message_react(setup["token_a"], message_id, 1)
    message_react(setup["token_b"], message_id, 1)
    message_unreact(setup["token_a"], message_id, 1)
    message_unreact(setup["token_b"], message_id, 1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 0)
    with pytest.raises(ValueError):
        message_unreact(setup["token_a"], message_id, 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"] == [])
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unreact_two_reacts_same_order(setup):
    # Testing unreacting twice, for two different reacts, in the order it was reacted to
    message_id = message_send(setup["token_a"], setup["channel_a"], "Who's down to clown?")
    message_react(setup["token_a"], message_id, 1)
    message_react(setup["token_a"], message_id, 2)
    message_unreact(setup["token_a"], message_id, 1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 2)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_unreact(setup["token_a"], message_id, 2)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"] == [])
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unreact_two_reacts_different_order(setup):
    # Testing unreacting twice, for two different reacts, in the opposite order to what it was reacted to
    message_id = message_send(setup["token_a"], setup["channel_a"], "Who's down to clown?")
    message_react(setup["token_a"], message_id, 2)
    message_react(setup["token_a"], message_id, 1)
    message_unreact(setup["token_a"], message_id, 2)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_unreact(setup["token_a"], message_id, 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"] == [])
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unreact_not_in_channel(setup):
    # Testing unreacting to a message in another channel
    channel_leave(setup["token_b"], setup["channel_a"])
    message_id = message_send(setup["token_a"], setup["channel_a"], "React to this")
    message_react(setup["token_a"], message_id, 1)
    with pytest.raises(AccessError):
        message_unreact(setup["token_b"], message_id, 1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unreact_bad_token(setup):
    # Testing unreacting with a bad token
    message_id = message_send(setup["token_a"], setup["channel_a"], "Five clues, for five keys, for five locks")
    message_react(setup["token_a"], message_id, 1)
    with pytest.raises(AccessError):
        message_unreact("", message_id, 1)
    assert(len(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(setup["token_a"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unreact_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_unreact("", -1, -1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                           TESTING message_pin                              ##
################################################################################

def test_message_pin_no_message(setup):
    # Testing pinning with no messages
    with pytest.raises(ValueError):
        message_pin(setup["token_a"], 1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_pin_normal(setup):
    # Testing pinning normally
    message_id = message_send(setup["token_a"], setup["channel_a"], "HeLeELOO")
    message_pin(setup["token_a"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == True)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_pin_twice(setup):
    # Testing pinning a message twice
    message_id = message_send(setup["token_a"], setup["channel_a"], "fml")
    message_pin(setup["token_a"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == True)
    with pytest.raises(ValueError):
        message_pin(setup["token_a"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == True)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_pin_not_admin(setup):
    # Testing pinnning a message when you aren't an admin
    message_id = message_send(setup["token_a"], setup["channel_a"], "Tam steals Chosen souls")
    with pytest.raises(AccessError):
        message_pin(setup["token_b"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_pin_not_in_channel(setup):
    # Testing pinning a message in another channel
    channel_leave(setup["token_a"], setup["channel_a"])
    message_id = message_send(setup["token_b"], setup["channel_a"], "It's a sled")
    with pytest.raises(AccessError):
        message_pin(setup["token_a"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == False)
    message_remove(setup["token_b"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_pin_bad_token(setup):
    # Testing pinning a message with a bad token
    message_id = message_send(setup["token_a"], setup["channel_a"], "Dumbledore Dies")
    with pytest.raises(AccessError):
        message_pin("", message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_pin_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_pin("", -1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
################################################################################
##                          TESTING message_unpin                             ##
################################################################################

def test_message_unpin_no_message(setup):
    # Testing unpinning a message when there are no messages
    with pytest.raises(ValueError):
        message_unpin(setup["token_a"], 1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
        
def test_message_unpin_not_pinned(setup):
    # Testing unpinning a message that wasn't pinned
    message_id = message_send(setup["token_a"], setup["channel_a"], "Tekeli-Li")
    with pytest.raises(ValueError):
        message_unpin(setup["token_a"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unpin_normal(setup):
    # Testing normal case
    message_id = message_send(setup["token_a"], setup["channel_a"], "Truth! Justice! Freedom! Reasonably Priced Love! And a Hard-Boiled Egg!")
    message_pin(setup["token_a"], message_id)
    message_unpin(setup["token_a"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unpin_twice(setup):
    # Testing unpinning the same message twice
    message_id = message_send(setup["token_a"], setup["channel_a"], "Twoo Wuv")
    message_pin(setup["token_a"], message_id)
    message_unpin(setup["token_a"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == False)
    with pytest.raises(ValueError):
        message_unpin(setup["token_a"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unpin_not_an_admin(setup):
    # Testing unpinning a message when you aren't an admin
    message_id = message_send(setup["token_a"], setup["channel_a"], "Someone gently rapping")
    message_pin(setup["token_a"], message_id)
    with pytest.raises(AccessError):
        message_unpin(setup["token_b"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == True)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unpin_not_in_channel(setup):
    # Testing unpinning a message when you don't have access to a channel
    channel_leave(setup["token_a"], setup["channel_a"])
    message_id = message_send(setup["token_b"], setup["channel_a"], "GOD Over Djinn")
    message_pin(setup["token_b"], message_id)
    with pytest.raises(AccessError):
        message_unpin(setup["token_a"], message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == True)
    message_remove(setup["token_b"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unpin_bad_token(setup):
    # Testing unpinning a message with a bad token
    message_id = message_send(setup["token_a"], setup["channel_a"], "Wanna Orange?")
    with pytest.raises(AccessError):
        message_unpin("", message_id)
    assert(channel_messages(setup["token_b"], setup["channel_a"], 0)["messages"][0]["is_pinned"] == False)
    message_remove(setup["token_a"], message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    
def test_message_unpin_disaster(setup):
    # Testing the worst case scenario
    with pytest.raises(Exception):
        message_unpin("", -1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
