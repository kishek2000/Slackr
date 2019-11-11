''' Tests for the search function '''
import sys
import pytest
sys.path.append('server/')
from functions.search_function import search
from functions.auth_functions import auth_register
from functions.helper_functions import reset_data
from functions.channel_functions import channels_create
from functions.message_functions import message_send, message_remove

@pytest.fixture
def register_account():
    ''' Used to set up temporary variables '''
    reset_data()
    returned_dict = auth_register('example@gmail.com', 'Go0dPa>sword', 'dan', 'man')
    channel_id = channels_create(returned_dict['token'], "Channel A", False)
    temp_second_dict = auth_register('exampl3@gmail.com', 'P@ssword123', 'Sharon', 'Mina')
    temp_channel = channels_create(temp_second_dict['token'], "Channel B", False)
    return [returned_dict, channel_id]

#################################################################################
##                           TESTING search                                    ##
#################################################################################
# function inputs: token, query_str
# function returns: messages

#The returned value from the function should be a dictionary
def test_search_correct_return_type(register_account):
    ''' Ensure that the return is of the correct format '''
    token = register_account[0]['token']
    assert isinstance(search(token, 'hello'), dict)

#The function should raise an error as there is no query_str
def test_search_no_input(register_account):
    ''' Test search with no input '''
    token = register_account[0]['token']
    with pytest.raises(ValueError):
        search(token, '')

#The function should return a dictionary with one message in it
def test_search_returned_value(register_account):
    ''' Check the returned values '''
    token = register_account[0]['token']
    message_send(token, register_account[1], "hello")
    returned_search = search(token, 'hello')
    assert len(returned_search['messages']) == 1
    assert returned_search['messages'][0] == 'hello'

#The function should return a dictionary with one message in it
def test_search_two_messages_in_channel(register_account):
    ''' With two messages in the channel check return message '''
    token = register_account[0]['token']
    message_send(token, register_account[1], "hello")
    message_send(token, register_account[1], "epic")
    returned_search = search(token, 'hello')
    assert len(returned_search['messages']) == 1
    assert returned_search['messages'][0] == 'hello'

#This tests the function after sending then removing a message
def test_search_returned_value_after_remove(register_account):
    ''' See if message is returned after removal '''
    token = register_account[0]['token']
    message_id = message_send(token, register_account[1], "hello")
    returned_search = search(token, 'hello')
    assert len(returned_search['messages']) == 1
    assert returned_search['messages'][0] == 'hello'
    message_remove(token, message_id)
    returned_search = search(token, 'hello')
    assert len(returned_search['messages']) == 0

reset_data()
