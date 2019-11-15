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
    a_info = auth_register(email="userA@userA.com", password="Go0dPa>sword", name_first="User", name_last="A")
    a_id = a_info['u_id']
    token_a = a_info['token']
    b_info = auth_register(email="userB@userB.com", password="Go0dPa>sword", name_first="User", name_last="B")
    b_id = b_info['u_id']
    token_b = b_info['token']
    channel_a = channels_create(token=token_a, name="Channel A", is_public=False)
    channel_b = channels_create(token=token_b, name="Channel B", is_public=True)
    channel_invite(token=token_a, channel_id=channel_a, u_id=b_id)
    channel_join(token=token_a, channel_id=channel_b)
    channel_dead = channels_create(token=token_a, name="empty test", is_public=True) # Check to see if this channel is empty
    return {"token_a": token_a, "token_b": token_b, "channel_a": channel_a, "channel_b": channel_b, "channel_dead": channel_dead, "a_id": a_id, "b_id": b_id}

def channel_is_empty(channel_id):
    return get_total_channel_messages(channel_id) == 0


################################################################################
##                           TESTING message_send                             ##
################################################################################

def test_message_send_max_length(setup):
    # Testing message of maximum length
    message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="x"*1000)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "x"*1000)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["u_id"] == setup["a_id"])
    #assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["time_created"] == time.time())
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == False)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"] == [])

def test_message_send_too_big(setup):
    # Testing message that's too big
    with pytest.raises(ValueError):
        message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="x"*1001)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_send_no_channel(setup):
    # Testing message sent to nonexistant channel
    with pytest.raises(ValueError):
        message_send(token=setup["token_a"], channel_id=-1, message="Hello")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_send_symbols(setup):
    # Testing weird characters
    message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Testing All Character Types: 54, ][")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Testing All Character Types: 54, ][")

def test_message_send_thrice(setup):
    message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="a")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "a")
    message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="b")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][1]["message"] == "a")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "b")
    message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="c")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][2]["message"] == "a")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][1]["message"] == "b")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "c")

def test_message_send_empty(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_send_spaces(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="     ")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_send_not_in_channel(setup):
    # Testing editing a message in a channel without being in that channel
    channel_leave(token=setup["token_b"], channel_id=setup["channel_a"])
    with pytest.raises(AccessError):
        message_send(token=setup["token_b"], channel_id=setup["channel_a"], message="I can't hear you")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_send_bad_token(setup):
    # Testing bad token
    with pytest.raises(AccessError):
        message_send(token="", channel_id=setup["channel_a"], message="Hello")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_send_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_send(token="", channel_id=-1, message="x"*1001)
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
    message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="x"*1000, time_sent=time.time()+1)
    time.sleep(2)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "x"*1000)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["u_id"] == setup["a_id"])
    #assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["time_created"] == time.time())

def test_message_sendlater_current_time(setup):
    # Testing message of maximum length sent at current time
    with pytest.raises(ValueError):
        message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="x"*1000, time_sent=time.time())
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_on_time(setup):
    # Testing message isn't sent prematurely
    message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello", time_sent=time.time()+4)
    assert(channel_is_empty(setup["channel_a"]))
    time.sleep(2)
    assert(channel_is_empty(setup["channel_a"]))
    time.sleep(2)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Hello")
    #assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["time_created"] == time.time())
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_empty_message(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="", time_sent=time.time()+1)
    time.sleep(2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_spaces(setup):
    # Testing empty message
    with pytest.raises(ValueError):
        message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="     ", time_sent=time.time()+1)
    time.sleep(2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_time_past(setup):
    # Testing message with time in the past
    with pytest.raises(ValueError):
        message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello", time_sent=time.time()-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_intermediate_messages(setup):
    # Testing message order is right when messages are sent before later message is sent
    message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="c", time_sent=time.time()+4)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="b", time_sent=time.time()+2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="a")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "a")
    time.sleep(3)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][1]["message"] == "a")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "b")
    time.sleep(2)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][2]["message"] == "a")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][1]["message"] == "b")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "c")

def test_message_sendlater_too_big(setup):
    # Testing message that's too big
    with pytest.raises(ValueError):
        message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="x"*1001, time_sent=time.time()+1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_no_channel(setup):
    # Testing message sent to nonexistant channel
    with pytest.raises(ValueError):
        message_sendlater(token=setup["token_a"], channel_id=-1, message="Hello", time_sent=time.time()+1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_not_in_channel(setup):
    # Testing editing a message in a channel without being in that channel
    channel_leave(token=setup["token_b"], channel_id=setup["channel_a"])
    with pytest.raises(AccessError):
        message_sendlater(token=setup["token_b"], channel_id=setup["channel_a"], message="I can't hear you", time_sent=time.time()+1)
    time.sleep(2)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_bad_token(setup):
    # Testing bad token
    with pytest.raises(AccessError):
        message_sendlater(token="", channel_id=setup["channel_a"], message="Hello", time_sent=time.time()+1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_sendlater_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_sendlater(token="", channel_id=-1, message="x"*1001, time_sent=time.time()-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                         TESTING message_remove                             ##
################################################################################

def test_message_remove_empty(setup):
    # Testing deletion of no prior messages
    with pytest.raises(ValueError):
        message_remove(token=setup["token_a"], message_id=0)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_one_message(setup):
    # Testing deletion of one message
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_two_messages_first(setup):
    # Testing deletion of first message
    message_id_1 = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello")
    message_id_2 = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="There")
    message_remove(token=setup["token_a"], message_id=message_id_1) # 'Hello'
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "There")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["u_id"] == setup["a_id"])
    #assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["time_created"] == time.time())
    message_remove(token=setup["token_a"], message_id=message_id_2) # 'There'
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_two_messages_second(setup):
    # Testing deletion of second message
    message_id_1 = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello")
    message_id_2 = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="There")
    message_remove(token=setup["token_a"], message_id=message_id_2) # 'There'
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Hello")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["u_id"] == setup["a_id"])
    #assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["time_created"] == time.time())
    message_remove(token=setup["token_a"], message_id=message_id_1) # 'Hello'
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_middle_mssage(setup):
    # Testing deletion of middle message
    message_id_1 = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello")
    message_id_2 = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="There")
    message_id_3 = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="World")
    message_remove(token=setup["token_a"], message_id=message_id_2) # 'There'
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "World")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][1]["message"] == "Hello")
    message_remove(token=setup["token_a"], message_id=message_id_1) # 'Hello'
    message_remove(token=setup["token_a"], message_id=message_id_3) # 'World'
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_other_person(setup):
    # Testing deletion of message sent by another person
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello")
    with pytest.raises(AccessError):
        message_remove(token=setup["token_b"], message_id=message_id)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Hello")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_admin_deletes_other_person(setup):
    # Testing deletion of a message sent by another person by an admin
    message_id = message_send(token=setup["token_b"], channel_id=setup["channel_a"], message="Hello")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_not_in_channel(setup):
    # Testing editing a message in a channel without being in that channel
    channel_leave(token=setup["token_b"], channel_id=setup["channel_a"])
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Remove this")
    with pytest.raises(AccessError):
        message_remove(token=setup["token_b"], message_id=message_id)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Remove this")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_bad_token(setup):
    # Testing deletion of message with bad token
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello")
    with pytest.raises(AccessError):
        message_remove(token="", message_id=message_id)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Hello")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_already_deleted(setup):
    # Testing deletion of already deleted message
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    with pytest.raises(ValueError):
        message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_nonexistant(setup):
    # Testing removal of a nonexistant message
    with pytest.raises(ValueError):
        message_remove(token=setup["token_a"], channel_id=-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_sendlater(setup):
    # Testing removal of a message that hasn't been sent yet
    message_id = message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello", time_sent=time.time()+5)
    with pytest.raises(ValueError):
        message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(6)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Hello")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_remove_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_remove(token="", channel_id=-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                          TESTING message_edit                              ##
################################################################################

def test_message_edit_no_messages(setup):
    with pytest.raises(ValueError):
        message_edit(token=setup["token_a"], message_id=42, message="b"*1000) # A plausible but missing message_id
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_max_length(setup):
    # Testing message of max length
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="a")
    message_edit(token=setup["token_a"], message_id=message_id, message="b"*1000)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "b"*1000)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_too_big(setup):
    # Testing message of too long a length
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="a")
    with pytest.raises(ValueError):
        message_edit(token=setup["token_a"], message_id=message_id, message="b"*1001)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "a")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_empty_message(setup):
    # Testing editing an empty message
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="a")
    message_edit(token=setup["token_a"], message_id=message_id, message="")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_spaces(setup):
    # Testing editing an empty message
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="a")
    with pytest.raises(ValueError):
        message_edit(token=setup["token_a"], message_id=message_id, message="     ")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "a")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_other_person(setup):
    # Testing when editor did not post the message, and is not admin
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello")
    with pytest.raises(AccessError):
        message_edit(token=setup["token_b"], message_id=message_id, message="World")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Hello")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_admin_edits_other_person(setup):
    # Testing when editor did not post the message, but is an admin
    message_id = message_send(token=setup["token_b"], channel_id=setup["channel_a"], message="Edit this!")
    message_edit(token=setup["token_a"], message_id=message_id, message="Edited")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Edited")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_nonexistant(setup):
    # Testing editing a nonexistant message
    with pytest.raises(ValueError):
        message_edit(token=setup["token_a"], message_id=-1, message="Edited")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_not_in_channel(setup):
    # Testing editing a message in a channel without being in that channel
    channel_leave(token=setup["token_b"], channel_id=setup["channel_a"])
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Edit this")
    with pytest.raises(AccessError):
        message_edit(token=setup["token_b"], message_id=message_id, message="Edited")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Edit this")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_bad_token(setup):
    # Testing editing a message with bad token
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Edit this")
    with pytest.raises(AccessError):
        message_edit(token="", message_id=message_id, message="Edited")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "Edit this")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_sendlater(setup):
    # Testing editing of a message that hasn't been sent yet
    message_id = message_sendlater(token=setup["token_a"], channel_id=setup["channel_a"], message="Hello", time_sent=time.time()+5)
    with pytest.raises(ValueError):
        message_edit(token=setup["token_a"], message_id=message_id, message="There")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))
    time.sleep(6)
    message_edit(token=setup["token_a"], message_id=message_id, message="There")
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["message"] == "There")
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_edit_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_edit(token="", message_id=-1, message="")
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                          TESTING message_react                             ##
################################################################################

def test_message_react_normal(setup):
    # Testing normal scenario
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Who's down to clown?")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_to_another(setup):
    # Testing reacting to another person's message
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Who's down to clown?")
    message_react(token=setup["token_b"], message_id=message_id, react_id=1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["b_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_no_message(setup):
    # Testing reacting to no message
    with pytest.raises(ValueError):
        message_react(token=setup["token_a"], message_id=1, react_id=1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_not_in_channel(setup):
    # Testing reacting to a message in a channel without being in that channel
    channel_leave(token=setup["token_b"], channel_id=setup["channel_a"])
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="React to this")
    with pytest.raises(AccessError):
        message_react(token=setup["token_b"], message_id=message_id, react_id=1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"] == [])
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_bad_react(setup):
    # Testing trying to react to a nonexistant react_id
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Give me a -1!")
    with pytest.raises(ValueError):
        message_react(token=setup["token_a"], message_id=message_id, react_id=-1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"] == [])
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_same_twice(setup):
    # Testing someone reacting to the same message twice
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Bring in the reacts")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    with pytest.raises(ValueError):
        message_react(token=setup["token_a"], message_id=message_id, react_id= 1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_same_different_people(setup):
    # Testing two people using the same react on the same message
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Bring in the reacts")
    message_react(token=setup["token_a"], message_id=message_id, react_id= 1)
    message_react(token=setup["token_b"], message_id=message_id, react_id= 1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"], setup["b_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_two_different_reacts(setup):
    # Testing two different reacts on the same message
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Bring in the reacts")
    message_react(token=setup["token_a"], message_id=message_id, react_id= 1)
    message_react(token=setup["token_a"], message_id=message_id, react_id= 2)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 2)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][1]["react_id"] == 2)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_bad_token(setup):
    # Testing message_react with a bad token
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Helllo")
    with pytest.raises(AccessError):
        message_react(token="", message_id=message_id, react_id=1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"] == [])
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_react_disaster(setup):
    # Testing the worst case scenario
    with pytest.raises(Exception):
        message_react(token="", message_id=-1, react_id=-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                         TESTING message_unreact                            ##
################################################################################

def test_message_unreact_no_message(setup):
    # Testing unreacting to no messages
    with pytest.raises(ValueError):
        message_unreact(token=setup["token_a"], message_id=1, react_id=1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_no_react(setup):
    # Testing unreacting to a message that wasn't reacted.
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Darn tests")
    with pytest.raises(ValueError):
        message_unreact(token=setup["token_a"], message_id=message_id, react_id=1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"] == [])
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_normal(setup):
    # Testing normal scenario
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Who's down to clown?")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    message_unreact(token=setup["token_a"], message_id=message_id, react_id=1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"] == [])
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_to_another(setup):
    # Testing unreacting a message someone else (but not you) reacted to
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Who's down to clown?")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    with pytest.raises(ValueError):
        message_unreact(token=setup["token_b"], message_id=message_id, react_id=1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_wrong_react_id(setup):
    # Testing unreacting a reacted message with the wrong reaction
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Who's down to clown?")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    with pytest.raises(ValueError):
        message_unreact(token=setup["token_a"], message_id=message_id, react_id=2)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_bad_react_id(setup):
    # Testing unreacting to a bad react id
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Who's down to clown?")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    with pytest.raises(ValueError):
        message_unreact(token=setup["token_a"], message_id=message_id, react_id=-1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_twice(setup):
    # Testing unreacting twice on the same message
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Who's down to clown?")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    message_react(token=setup["token_b"], message_id=message_id, react_id=1)
    message_unreact(token=setup["token_a"], message_id=message_id, react_id=1)
    message_unreact(token=setup["token_b"], message_id=message_id, react_id=1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 0)
    with pytest.raises(ValueError):
        message_unreact(token=setup["token_a"], message_id=message_id, react_id=1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"] == [])
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_two_reacts_same_order(setup):
    # Testing unreacting twice, for two different reacts, in the order it was reacted to
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Who's down to clown?")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    message_react(token=setup["token_a"], message_id=message_id, react_id=2)
    message_unreact(token=setup["token_a"], message_id=message_id, react_id=1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 2)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_unreact(token=setup["token_a"], message_id=message_id, react_id=2)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"] == [])
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_two_reacts_different_order(setup):
    # Testing unreacting twice, for two different reacts, in the opposite order to what it was reacted to
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Who's down to clown?")
    message_react(token=setup["token_a"], message_id=message_id, react_id=2)
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    message_unreact(token=setup["token_a"], message_id=message_id, react_id=2)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_unreact(token=setup["token_a"], message_id=message_id, react_id=1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"] == [])
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_not_in_channel(setup):
    # Testing unreacting to a message in another channel
    channel_leave(token=setup["token_b"], channel_id=setup["channel_a"])
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="React to this")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    with pytest.raises(AccessError):
        message_unreact(token=setup["token_b"], message_id=message_id, react_id=1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_bad_token(setup):
    # Testing unreacting with a bad token
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Five clues, for five keys, for five locks")
    message_react(token=setup["token_a"], message_id=message_id, react_id=1)
    with pytest.raises(AccessError):
        message_unreact(token="", message_id=message_id, react_id=1)
    assert(len(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"]) == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["react_id"] == 1)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["u_ids"] == [setup["a_id"]])
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == True)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["reacts"][0]["is_this_user_reacted"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unreact_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_unreact(token="", message_id=-1, react_id=-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                           TESTING message_pin                              ##
################################################################################

def test_message_pin_no_message(setup):
    # Testing pinning with no messages
    with pytest.raises(ValueError):
        message_pin(token=setup["token_a"], message_id=1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_pin_normal(setup):
    # Testing pinning normally
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="HeLeELOO")
    message_pin(token=setup["token_a"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == True)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_pin_twice(setup):
    # Testing pinning a message twice
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="fml")
    message_pin(token=setup["token_a"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == True)
    with pytest.raises(ValueError):
        message_pin(token=setup["token_a"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == True)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_pin_not_admin(setup):
    # Testing pinnning a message when you aren't an admin
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Tam steals Chosen souls")
    with pytest.raises(AccessError):
        message_pin(token=setup["token_b"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_pin_not_in_channel(setup):
    # Testing pinning a message in another channel
    channel_leave(token=setup["token_a"], channel_id=setup["channel_a"])
    message_id = message_send(token=setup["token_b"], channel_id=setup["channel_a"], message="It's a sled")
    with pytest.raises(AccessError):
        message_pin(token=setup["token_a"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == False)
    message_remove(token=setup["token_b"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_pin_bad_token(setup):
    # Testing pinning a message with a bad token
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Dumbledore Dies")
    with pytest.raises(AccessError):
        message_pin(token="", message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_pin_disaster(setup):
    # Testing worst case scenario
    with pytest.raises(Exception):
        message_pin(token="", message_id=-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

################################################################################
##                          TESTING message_unpin                             ##
################################################################################

def test_message_unpin_no_message(setup):
    # Testing unpinning a message when there are no messages
    with pytest.raises(ValueError):
        message_unpin(token=setup["token_a"], message_id=1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unpin_not_pinned(setup):
    # Testing unpinning a message that wasn't pinned
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Tekeli-Li")
    with pytest.raises(ValueError):
        message_unpin(token=setup["token_a"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unpin_normal(setup):
    # Testing normal case
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Truth! Justice! Freedom! Reasonably Priced Love! And a Hard-Boiled Egg!")
    message_pin(token=setup["token_a"], message_id=message_id)
    message_unpin(token=setup["token_a"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unpin_twice(setup):
    # Testing unpinning the same message twice
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Twoo Wuv")
    message_pin(token=setup["token_a"], message_id=message_id)
    message_unpin(token=setup["token_a"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == False)
    with pytest.raises(ValueError):
        message_unpin(token=setup["token_a"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unpin_not_an_admin(setup):
    # Testing unpinning a message when you aren't an admin
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Someone gently rapping")
    message_pin(token=setup["token_a"], message_id=message_id)
    with pytest.raises(AccessError):
        message_unpin(token=setup["token_b"], message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == True)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unpin_not_in_channel(setup):
    # Testing unpinning a message when you don't have access to a channel
    channel_leave(token=setup["token_b"], channel_id=setup["channel_a"])
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="GOD Over Djinn")
    message_pin(token=setup["token_a"], message_id=message_id)
    with pytest.raises(AccessError):
        message_unpin(token=setup["token_b"], message_id=message_id)
    assert(channel_messages(token=setup["token_a"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == True)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unpin_bad_token(setup):
    # Testing unpinning a message with a bad token
    message_id = message_send(token=setup["token_a"], channel_id=setup["channel_a"], message="Wanna Orange?")
    with pytest.raises(AccessError):
        message_unpin(token="", message_id=message_id)
    assert(channel_messages(token=setup["token_b"], channel_id=setup["channel_a"], start=0)["messages"][0]["is_pinned"] == False)
    message_remove(token=setup["token_a"], message_id=message_id)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

def test_message_unpin_disaster(setup):
    # Testing the worst case scenario
    with pytest.raises(Exception):
        message_unpin(token="", message_id=-1)
    assert(channel_is_empty(setup["channel_a"]))
    assert(channel_is_empty(setup["channel_dead"]))

