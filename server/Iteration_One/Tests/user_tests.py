import pytest
@pytest.fixture
def register_account:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    return returned_dict
# user_profile tests
# function inputs: token, u_id
# function returns: email, name_first, name_last, handle_str
'''
Things to think about
    - No function inputs
'''

def user_profile_correct_return(register_account):
    upcr_token = returned_dict['token']
    upcr_u_id = returned_dict['u_id']
    upcr_dictionary = user_profile(upcr_token, upcr_u_id)
    assert upcr_dictionary[email] == 'example@gmail.com'
    assert upcr_dictionary[name_first] == 'dan'
    assert upcr_dictionary[name_last] == 'man'
    assert upcr_dictionary[handle_str] == 'danman'
    
def user_profile_incorrect_return(register_account):
    upir_token = returned_dict['token']
    upir_u_id = returned_dict['u_id']
    upir_dictionary = user_profile(upir_token, upir_u_id)
    assert upir_dictionary[handle_str] != 'dantheman'

def user_profile_invalid_id(register_account):
    upii_token = returned_dict['token']
    with pytest.raises(ValueError):
        user_profile(upii_token, 'wrong')

# user_profile_setname tests
# function inputs: token, name_first, name_last
# function returns: 
'''
Assumptions
    - If given no name input, it should throw an error
'''
def user_profile_setname_no_return(register_account):
    upsnr_token = returned_dict['token']
    upsnr_u_id = returned_dict['u_id']
    assert user_profile_setname(upsnr_token, 'danny', 'manny') == None

def user_profile_setname_updated_values(register_account):
    upsuv_token = returned_dict['token']
    upsuv_u_id = returned_dict['u_id']
    upsuv_dictionary = user_profile(upsuv_token, upsuv_u_id)
    assert upsuv_dictionary[name_first] == 'dan'
    assert upsuv_dictionary[name_last] == 'man'
    user_profile_setname(upsuv_token, 'danny', 'manny')
    upsuv_dictionary = user_profile(upsuv_token, upsuv_u_id)
    assert upsuv_dictionary[name_first] == 'danny'
    assert upsuv_dictionary[name_last] == 'manny'
    
def user_profile_setname_long_name_first(register_account):
    upslnf_token = returned_dict['token']
    upslnf_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        user_profile_setname(upslnf_token, '123456789012345678901234567890123456789012345678901', 'manny')

def user_profile_setname_long_name_last(register_account):
    uplnl_token = returned_dict['token']
    uplnl_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        user_profile_setname(uplnl_token, 'danny', '123456789012345678901234567890123456789012345678901')

def user_profile_setname_no_input(register_account):
    upni_token = returned_dict['token']
    upni_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        user_profile_setname(upni_token, '', '')

# user_profile_setemail tests
# function inputs: token, email
# function returns: 
'''
Assumptions
    - If given no email input, it should throw an error
'''
def user_profile_setemail_no_return(register_account):
    upsnr_token = returned_dict['token']
    upsnr_u_id = returned_dict['u_id']
    assert user_profile_setemail(upsnr_token, 'dantheman@gmail.com') == None

def user_profile_setemail_updated_values(register_account):
    upsuv_token = returned_dict['token']
    upsuv_u_id = returned_dict['u_id']
    upsuv_dictionary = user_profile(upsuv_token, upsuv_u_id)
    assert upsuv_dictionary[email] == 'example@gmail.com'
    user_profile_setemail(upsuv_token, 'dantheman@gmail.com')
    upsuv_dictionary = user_profile(upsuv_token, upsuv_u_id)
    assert upsuv_dictionary[email] == 'dantheman@gmail.com'
    
def user_profile_setemail_not_valid(register_account):
    upsnv_token = returned_dict['token']
    upsnv_u_id = returned_dict['u_id']
    #not valid email stuff can be copied from other areas
    with pytest.raises(ValueError):
        user_profile_setname(upsnv_token, '', '')

def user_profile_setname_no_input(register_account):
    upsni_token = returned_dict['token']
    upsni_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        user_profile_setname(upsni_token, '')

# user_profile_sethandle tests
# function inputs: token, handle_str
# function returns: 
'''
Assumptions
- Handle should not be that same as one that already exists
'''
def user_profile_sethandle_no_return(register_account):
    upsnr_token = returned_dict['token']
    upsnr_u_id = returned_dict['u_id']
    assert user_profile_sethandle(upsnr_token, 'dantheman') == None

def user_profile_sethandle_updated_values(register_account):
    upsuv_token = returned_dict['token']
    upsuv_u_id = returned_dict['u_id']
    upsuv_dictionary = user_profile(upsuv_token, upsuv_u_id)
    assert upsuv_dictionary[handle_str] == 'example@gmail.com'
    user_profile_sethandle(upsuv_token, 'dantheman')
    upsuv_dictionary = user_profile(upsuv_token, upsuv_u_id)
    assert upsuv_dictionary[handle_str] == 'dantheman'
    
def user_profile_sethandle_too_long(register_account):
    upsnv_token = returned_dict['token']
    upsnv_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        user_profile_sethandle(upsnv_token, 'dantheman12345678901234567890')

def user_profile_sethandle_no_input(register_account):
    upsni_token = returned_dict['token']
    upsni_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        user_profile_sethandle(upsni_token, '')

def user_profile_sethandle_already_exists(register_account):
    upsae_token = returned_dict['token']
    upsae_u_id = returned_dict['u_id']
    #need to think about how this is done
    with pytest.raises(ValueError):
        user_profile_sethandle(upsnv_token, 'something that already exists')

# user_profiles_uploadphoto tests
# function inputs: token, img_url, x_start, y_start, x_end, y_end
# function returns: 
def user_profiles_uploadphoto_no_return(register_account):
    upunr_token = returned_dict['token']
    upunr_u_id = returned_dict['u_id']
    assert user_profiles_uploadphoto(upunr_token, 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', 0, 0, 2864, 1861) == None

def user_profiles_uploadphoto_not_200(register_account):
    upun2_token = returned_dict['token']
    upun2_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        assert user_profiles_uploadphoto(upun2_token, 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Potates.jpg', 0, 0, 2864, 1861)
        
def user_profiles_uploadphoto_wrong_dimensions(register_account):
    upuwd_token = returned_dict['token']
    upuwd_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        assert user_profiles_sethandle(upuwd_token, 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Potates.jpg', 2864, 1861, 0, 0)
    
#need to think more about the tests for this one
