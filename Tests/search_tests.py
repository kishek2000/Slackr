import pytest
@pytest.fixture
def register_account():
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    channel_id = channels_create(returned_dict['token'], "Channel A", False)
    return [returned_dict, channel_id]

#################################################################################
##                           TESTING search                                    ##
#################################################################################
# function inputs: token, query_str
# function returns: messages

#The returned value from the function should be a dictionary
def test_search_correct_return_type(register_account):
    token = register_account['token']
    assert type(search(token,'hello')) = type({})

#The function should raise an error as there is no query_str    
def test_search_no_input(register_account):
    token = register_account[0]['token']
    with pytest.raises(ValueError):
        search(token, '')
    
#The function should return a dictionary with one message in it    
def test_search_returned_value(register_account):
    token = register_account[0]['token']    
    message_send(token, register_account[1]["channel_a"], "Hello")
    returned_search = search(token, 'hello')
    assert len(returned_search) == 1
    assert returned_search['message_1'] == 'hello'
    
#This tests the function after sending then removing a message    
def test_search_returned_value(register_account):
    token = register_account[0]['token']    
    message_send(token, register_account[1]["channel_a"], "Hello")
    returned_search = search(token, 'hello')
    assert len(returned_search) == 1
    assert returned_search['message_1'] == 'hello' 
    message_remove(token, 0)
    returned_search = search(token, 'hello')
    assert len(returned_search) == 0
