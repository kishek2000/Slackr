import pytest

# search tests
# function inputs: token, query_str
# function returns: messages
'''
Things to think about
    - Other cases
'''

def search_correct_return_type:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    scrt_token = returned_dict['token']
    assert type(search('')) = type({})
    
def search_no_input:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    sni_token = returned_dict['token']
    with pytest.raises(ValueError):
        search()
