## Created by Liam 1/10/19
## Last edited 4/10/19
## Status: ....xxxx
## Might need to add tests where a member is made an admin. This will add more tokens :(
import pytest

@pytest.fixture()
def setup():
    # Setting up
    a_id, a_token = auth_register("userA@userA.com", "Go0dPa>sword", "User", "A")
    b_id, b_token = auth_register("userB@userB.com", "Go0dPa>sword", "User", "B")
    channel_a = channels_create(a_token, "Channel A", False)
    channel_b = channels_create(b_token, "Channel B", True)    
    channel_invite(a_token, channel_a, b_id)
    channel_join(a_tokne, channel_b)
    dead_channel = channels_create(token, "empty test", True) # Check to see if this channel is empty
    return [a_token, b_token, channel_a, channel_b, dead_channel]
    #       setup[0], setup[1], setup[2], setup[3], setup[4]
   
   
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
    
def test_message_remove_empty(setup):
    # Testing deletion of no prior messages
    with pytest.raises(ValueError):
        message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
        #CHECK NOTHING HAPPENED
    
def test_message_remove_one_message(setup):
    # Testing deletion of one message
    message_send(setup[0], setup[2], "Hello")
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    #CHECK#
    
def test_message_remove_two_messages_first(setup):
    # Testing deletion of first message
    message_send(setup[0], setup[2], "Hello")
    message_send(setup[0], setup[2], "There")
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][1]["message_id"]) # 'Hello'
    #CHECK#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"]) # 'There'
    #CHECK#
    
def test_message_remove_two_messages_second(setup):    
    # Testing deletion of second message
    message_send(setup[0], setup[2], "Hello")
    message_send(setup[0], setup[2], "There")
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"]) # 'There'
    #CHECK#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][1]["message_id"]) # 'Hello'
    #CHECK#
    
def test_message_remove_middle_mssage(setup):
    # Testing deletion of middle message
    message_send(setup[0], setup[2], "Hello")
    message_send(setup[0], setup[2], "There")
    message_send(setup[0], setup[2], "World")
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][1]["message_id"]) # 'There'
    #CHECK#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][1]["message_id"]) # 'Hello'
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"]) # 'World'
    #CHECK#
    
def test_message_remove_other_person(setup):
    # Testing deletion of message sent by another person
    message_send(setup[0], setup[2], "Hello")
    with pytest.raises(AccessError):
        message_remove(setup[1], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
        #CHECK NOTHING HAPPENED#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    #CHECK#
        
def test_message_remove_admin_deletes_other_person(setup):
    # Testing deletion of a message sent by another person by an admin
    message_send(setup[1], setup[2], "Hello")
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    #CHECK#

def test_message_remove_bad_token(setup):        
    # Testing deletion of message with bad token
    message_send(setup[0], setup[2], "Hello")
    with pytest.raises(AccessError):
        message_remove("", message_id)
        #CHECK NOTHING HAPPENED#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
        
def test_message_remove_already_deleted(setup):
    # Testing deletion of already deleted message
    message_send(setup[0], setup[2], "Hello")
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    #CHECK#
    with pytest.raises(ValueError):
        message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
        #CHECK NOTHING HAPPENED#

def test_message_remove_nonexistant(setup):
    # Testing removal of a nonexistant message
    with pytest.raises(ValueError):
        message_remove(setup[0], -1)
        #CHECK#

def test_message_remove_send_later(setup):
    # Testing removal of a message that hasn't been sent yet
    message_send_later(setup[0], setup[2], "Hello", time()+5)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    #CHECK NOTHING HAPPENED#
    sleep(6)
    #CHECK#

def test_message_remove_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_remove("", -1)
        #CHECK#

################################################################################
##                          TESTING message_edit                              ##
################################################################################

    '''
    message_id to be replaced when I know howtf that's represented
    '''
    
def test_message_edit_no_messages(setup):
    with pytest.raises(ValueError):
        message_edit(setup[0], 42, "b"*1000) # A plausible but missing message_id

def test_message_edit_max_lenght(setup):
    # Testing message of max length
    message_send(setup[0], setup[2], "a")
    message_edit(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], "b"*1000)
    #CHECK#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])

def test_message_edit_too_big(setup):
    # Testing message of too long a length
    message_send(setup[0], setup[2], "a")
    with pytest.raises(ValueError):
        message_edit(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], "b"*1001)
        #CHECK NOTHING HAPPENED#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])

def test_message_edit_empty_message(setup):
    # Testing editing an empty message
    message_send(setup[0], setup[2], "a")
    with pytest.raises(ValueError):
        message_edit(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], "")
        #CHECK NOTHING HAPPENED#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_edit_spaces(setup):
    # Testing editing an empty message
    message_send(setup[0], setup[2], "a")
    with pytest.raises(ValueError):
        message_edit(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], "     ")
        #CHECK NOTHING HAPPENED#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_edit_other_person(setup):
    # Testing when editor did not post the message, and is not admin
    message_send(setup[0], setup[2], "Hello")
    with pytest.raises(ValueError):
        message_edit(setup[1], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], "World")
        #CHECK NOTHING HAPPENED#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_edit_admin_edits_other_person(setup):
    # Testing when editor did not post the message, but is an admin
    message_send(setup[1], setup[2], "Edit this!")
    message_edit(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], "Edited")
    #CHECK#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])

def test_message_edit_nonexistant(setup):
    # Testing editing a nonexistant message
    with pytest.raises(ValueError):
        message_edit(setup[0], -1, "Edited")
        #CHECK NOTHING HAPPENED#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_edit_bad_token(setup):
    # Testing editing a message with bad token
    message_send(setup[0], setup[2], "Edit this")
    with pytest.raises(AccessError):
        message_edit("", channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], "Edited")
        #CHECK NOTHING HAPPEND#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_edit_send_later(setup):
    # Testing editing of a message that hasn't been sent yet
    message_send_later(setup[0], setup[2], "Hello", time()+5)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], "There")
    #CHECK NOTHING HAPPENED#
    sleep(6)
    #CHECK#
    
def test_message_edit_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_edit("", -1, "")
        #CHECK NOTHING HAPPENED#
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])

################################################################################
##                          TESTING message_react                             ##
################################################################################

    '''
    No defined data type for reacts, so can't yet write asserts
    '''

def test_message_react_normal(setup):
    # Testing normal scenario
    message_send(setup[0], setup[2], "Who's down to clown?")
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_react_to_another(setup):
    # Testing reacting to another person's message
    message_send(setup[0], setup[2], "Who's down to clown?")
    message_react(setup[1], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_react_no_message(setup):
    # Testing reacting to no message
    with pytest.raises(ValueError):
        message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
        
def test_message_react_not_in_channel(setup):
    # Testing reacting to a message in a channel without being in that channel
    channel_leave(setup[1], setup[2])
    message_send(setup[0], setup[2], "React to this")
    with pytest.raises(ValueError):
        mesage_react(setup[1], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])    
        
def test_message_react_bad_react(setup):
    # Testing trying to react to a nonexistant react_id
    message_send(setup[0], setup[2], "Give me a -1!")
    with pytest.raises(ValueError):
        mesage_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], -1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])    
    
def test_message_react_same_twice(setup):
    # Testing someone reacting to the same message twice
    message_send(setup[0], setup[2], "Bring in the reacts")
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    with pytest.raises(ValueError):
        message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
        
def test_message_react_same_different_people(setup):
    # Testing two people using the same react on the same message
    message_send(setup[0], setup[2], "Bring in the reacts")
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    with pytest.raises(ValueError):
        message_react(setup[0], channel_messages(setup[1], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])

def test_message_react_two_different_reacts(setup):
    # Testing two different reacts on the same message
    message_send(setup[0], setup[2], "Bring in the reacts")
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 2)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_react_bad_token(setup):
    # Testing message_react with a bad token
    message_send(setup[0], setup[2], "Helllo")
    with pytest.raises(AccessError):
        message_react("", channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
        
def test_message_react_disaster(setup):
    # Testing the worst case scenario
    with pytest.raises(Exception):
        message_react("", -1, -1)

################################################################################
##                         TESTING message_unreact                            ##
################################################################################

def test_message_unreact_no_message(setup):
    # Testing unreacting to no messages
    with pytest.raises(ValueError):
        message_unreact(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)

def test_message_unreact_no_react(setup):
    # Testing unreacting to a message that wasn't reacted.
    message_send(setup[0], setup[2], "Darn tests")
    with pytest.raises(ValueError):
        message_unreact(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
        
def test_message_unreact_normal(setup):
    # Testing normal scenario
    message_send(setup[0], setup[2], "Who's down to clown?")
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_unreact(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unreact_to_another(setup):
    # Testing unreacting a message someone else reacted to
    message_send(setup[0], setup[2], "Who's down to clown?")
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_unreact(setup[1], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unreact_wrong_react_id(setup):
    # Testing unreacting a reacted message with the wrong reaction
    message_send(setup[0], setup[2], "Who's down to clown?")
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    with pytest.raises(ValueError):
        message_unreact(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 2)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unreact_bad_react_id(setup):
    # Testing unreacting to a bad react id
    message_send(setup[0], setup[2], "Who's down to clown?")
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    with pytest.raises(ValueError):
        message_unreact(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], -1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])

def test_message_unreact_twice(setup):
    # Testing unreacting twice on the same message
    message_send(setup[0], setup[2], "Who's down to clown?")
    message_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_unreact(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    with pytest.raises(ValueError):
        message_unreact(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unreact_not_in_channel(setup):
    # Testing unreacting to a message in another channel
    channel_leave(setup[1], setup[2])
    message_send(setup[0], setup[2], "React to this")
    with pytest.raises(ValueError):
        mesage_react(setup[1], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unreact_bad_token(setup):
    # Testing unreacting with a bad token
    message_send(setup[0], setup[2], "Five clues, for five keys, for five locks")
    mesage_react(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    with pytest.raises(AccessError):
        message_unreact("", channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"], 1)
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unreact_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_unreact("", -1, -1)

################################################################################
##                           TESTING message_pin                              ##
################################################################################

    '''
    No defined way to represent pins, so can't yet write asserts
    '''

def test_message_pin_no_message(setup):
    # Testing pinning with no messages
    with pytest.raises(ValueError):
        message_pin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
        
def test_message_pin_normal(setup):
    # Testing pinning normally
    message_send(setup[0], setup[2], "HeLeELOO")
    message_pin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_pin_twice(setup):
    # Testing pinning a message twice
    message_send(setup[0], setup[2], "fml")
    message_pin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    with pytest.raises(ValueError):
        message_pin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_pin_not_admin(setup):
    # Testing pinnning a message when you aren't an admin
    message_send(setup[0], setup[2], "Tam steals Chosen souls")
    with pytest.raises(ValueError):
        message_pin(setup[1], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_pin_not_in_channel(setup):
    # Testing pinning a message in another channel
    channel_leave(setup[0], setup[2])
    message_send(setup[1], setup[2], "It's a sled")
    with pytest.raises(AccessError):
        mesage_pin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[1], channel_messages(setup[1], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_pin_bad_token(setup):
    # Testing pinning a message with a bad token
    message_send(setup[0], setup[2], "Dumbledore Dies")
    with pytest.raises(AccessError):
        message_pin("", channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_pin_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_pin("", -1)
    
################################################################################
##                          TESTING message_unpin                             ##
################################################################################

def test_message_unpin_no_message(setup):
    # Testing unpinning a message when there are no messages
    with pytest.raises(ValueError):
        message_unpin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
        
def test_message_unpin_not_pinned(setup):
    # Testing unpinning a message that wasn't pinned
    message_send(setup[0], setup[2], "the cat would be lost, the tree burned down, and the old lady would be traveling with us now.")
    with pytest.raises(ValueError):
        message_unpin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unpin_normal(setup):
    # Testing normal case
    message_send(setup[0], setup[2], "Truth! Justice! Freedom! Reasonably Priced Love! And a Hard-Boiled Egg!")
    message_pin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_unpin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unpin_twice(setup):
    # Testing unpinning the same message twice
    message_send(setup[0], setup[2], "Twoo Wuv")
    message_pin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_unpin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_unpin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unpin_not_an_admin(setup):
    # Testing unpinning a message when you aren't an admin
    message_send(setup[0], setup[2], "Someone gently rapping")
    message_pin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    with pytest.raises(ValueError):
        message_unpin(setup[1], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unpin_not_in_channel(setup):
    # Testing unpinning a message when you don't have access to a channel
    channel_leave(setup[0], setup[2])
    message_send(setup[1], setup[2], "GOD Over Djinn")
    with pytest.raises(AccessError):
        mesage_unpin(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[1], channel_messages(setup[1], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unpin_bad_token(setup):
    # Testing unpinning a message with a bad token
    message_send(setup[0], setup[2], "Wanna Orange?")
    with pytest.raises(AccessError):
        mesage_unpin("", channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    message_remove(setup[0], channel_messages(setup[0], setup[2], 0)["messages"][0]["message_id"])
    
def test_message_unpin_disaster(setup):
    # Testing the worst case scenario
    with pytest.raises(Exception):
        message_unpin("", -1)
