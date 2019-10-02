import pytest

# user_profile tests
# function inputs: token, u_id
# function returns: email, name_first, name_last, handle_str
'''
Things to think about
    - No function inputs
'''

def user_profile_correct_return:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    upcr_token = returned_dict['token']
    upcr_u_id = returned_dict['u_id']
    upcr_dictionary = user_profile(upcr_token, upcr_u_id)
    assert upcr_dictionary[email] == 'example@gmail.com'
    assert upcr_dictionary[name_first] == 'dan'
    assert upcr_dictionary[name_last] == 'man'
    assert upcr_dictionary[handle_str] == 'danman'
    
def user_profile_incorrect_return:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    upir_token = returned_dict['token']
    upir_u_id = returned_dict['u_id']
    upir_dictionary = user_profile(upir_token, upir_u_id)
    assert upir_dictionary[handle_str] != 'dantheman'

def user_profile_invalid_id:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    upii_token = returned_dict['token']
    with pytest.raises(ValueError)
        user_profile(upii_token, 'wrong')

# user_profile_setname tests
# function inputs: token, name_first, name_last
# function returns: 
'''
Assumptions
    - If given no name input, it should throw an error
'''
def user_profile_setname_no_return():
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    upsnr_token = returned_dict['token']
    upsnr_u_id = returned_dict['u_id']
    assert user_profile_setname(upsnr_token, 'danny', 'manny') == None

def user_profile_setname_updated_values():
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    upsuv_token = returned_dict['token']
    upsuv_u_id = returned_dict['u_id']
    upsuv_dictionary = user_profile(upsuv_token, upsuv_u_id)
    assert upsuv_dictionary[name_first] == 'dan'
    assert upsuv_dictionary[name_last] == 'man'
    user_profile_setname(upcr_token, 'danny', 'manny')
    upsuv_dictionary = user_profile(upsuv_token, upsuv_u_id)
    assert upsuv_dictionary[name_first] == 'danny'
    assert upsuv_dictionary[name_last] == 'manny'
    
def user_profile_setname_long_name_first():
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    upslnf_token = returned_dict['token']
    upslnf_u_id = returned_dict['u_id']
    with pytest.raises(ValueError)
        user_profile_setname(upslnf_token, '123456789012345678901234567890123456789012345678901', 'manny')

def user_profile_setname_long_name_last():
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    uplnl_token = returned_dict['token']
    uplnl_u_id = returned_dict['u_id']
    with pytest.raises(ValueError)
        user_profile_setname(uplnl_token, 'danny', '123456789012345678901234567890123456789012345678901')

def user_profile_setname_no_input():
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    upni_token = returned_dict['token']
    upni_u_id = returned_dict['u_id']
    with pytest.raises(ValueError)
        user_profile_setname(upni_token, '', '')

# user_profile_setemail tests
# function inputs: token, email
# function returns: 

# user_profile_sethandle tests
# function inputs: token, handle_str
# function returns: 

# user_profiles_uploadphoto tests
# function inputs: token, img_url, x_start, y_start, x_end, y_end
# function returns: 
