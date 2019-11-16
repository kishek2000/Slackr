''' Tests for the search function '''
import sys
import pytest
sys.path.append('server/')
from functions.search_function import search
from functions.auth_functions import auth_register
from functions.helper_functions import reset_data
from functions.channel_functions import channels_create
from functions.message_functions import message_send, message_remove
from functions.Errors import ValueError

@pytest.fixture
def register_account():
    ''' Used to set up temporary variables '''
    reset_data()
    returned_dict = auth_register(email='example@gmail.com', password='Go0dPa>sword', name_first='dan', name_last='man')
    channel_id = channels_create(token=returned_dict['token'], name="Channel A", is_public=False)
    temp_second_dict = auth_register(email='exampl3@gmail.com', password='P@ssword123', name_first='Sharon', name_last='Mina')
    temp_channel = channels_create(token=temp_second_dict['token'], name="Channel B", is_public=False)
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
    message_send(token=token, channel_id=register_account[1], message="hello")
    returned_search = search(token, 'hello')
    assert len(returned_search['messages']) == 1
    assert returned_search['messages'][0]['message'] == 'hello'

#The function should return a dictionary with one message in it
def test_search_two_messages_in_channel(register_account):
    ''' With two messages in the channel check return message '''
    token = register_account[0]['token']
    message_send(token=token, channel_id=register_account[1], message="hello")
    message_send(token=token, channel_id=register_account[1], message="epic")
    returned_search = search(token, 'hello')
    assert len(returned_search['messages']) == 1
    assert returned_search['messages'][0]['message'] == 'hello'

#This tests the function after sending then removing a message
def test_search_returned_value_after_remove(register_account):
    ''' See if message is returned after removal '''
    token = register_account[0]['token']
    message_id = message_send(token=token, channel_id=register_account[1], message="hello")
    returned_search = search(token, 'hello')
    assert len(returned_search['messages']) == 1
    assert returned_search['messages'][0]['message'] == 'hello'
    message_remove(token=token, message_id=message_id)
    returned_search = search(token, 'hello')
    assert len(returned_search['messages']) == 0

reset_data()
