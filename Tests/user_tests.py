import pytest
import sys
sys.path.append('Server/')
from functions.user_functions import *
from functions.auth_functions import auth_register
from functions.helper_functions import reset_data
from functions.Errors import *


@pytest.fixture
def register_account():
    reset_data()
    return auth_register('example@gmail.com', 'Go0dPa>sword', 'dan', 'man')
    
#################################################################################
##                           TESTING user_profile                              ##
#################################################################################
# function inputs: token, u_id
# function returns: email, name_first, name_last, handle_str

#This test ensures that the function returns the correct values
def test_user_profile_correct_return(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token, u_id)
    assert dictionary['email'] == 'example@gmail.com'
    assert dictionary['name_first'] == 'dan'
    assert dictionary['name_last'] == 'man'
    assert dictionary['handle_str'] == 'danman'
    
#This test ensures that the returned string is not incorrect
def test_user_profile_incorrect_return(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token, u_id)
    assert dictionary['handle_str'] != 'dantheman'

#This tests that that u_id is incorrect
def test_user_profile_invalid_id(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile(token, 'wrong')

#This tests that that token is incorrect
def test_user_profile_invalid_token(register_account):
    u_id = register_account['u_id']
    with pytest.raises(AccessError):
        user_profile('wrong token', u_id)

#################################################################################
##                      TESTING user_profile_setname                           ##
#################################################################################
# user_profile_setname tests
# function inputs: token, name_first, name_last
# function returns: 
'''
Assumptions
    - If given no name input, it should throw an error
'''
#Ensure the function does not return anything
def test_user_profile_setname_no_return(register_account):
    token = register_account['token']
    assert user_profile_setname(token, 'danny', 'manny') == None

#This function ensures that the updated names are the same as the input
def test_user_profile_setname_updated_values(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token, u_id)
    assert dictionary['name_first'] == 'dan'
    assert dictionary['name_last'] == 'man'
    user_profile_setname(token, 'danny', 'manny')
    dictionary = user_profile(token, u_id)
    assert dictionary['name_first'] == 'danny'
    assert dictionary['name_last'] == 'manny'

#An invalid token should raise an error
def test_user_profile_setname_invalid_token(register_account):
    token = 'wrong token'
    with pytest.raises(AccessError):
        user_profile_setname(token, 'danny', 'manny')

#Name_first cannot be greater than 50 characters, so it should raise an error
def test_user_profile_setname_long_name_first(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setname(token, '123456789012345678901234567890123456789012345678901', 'manny')

#Name_last cannot be greater than 50 characters, so it should raise an error
def test_user_profile_setname_long_name_last(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setname(token, 'danny', '123456789012345678901234567890123456789012345678901')

#An empty string cannot be a name, so it should raise an error
def test_user_profile_setname_no_input(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setname(token, '', '')

#################################################################################
##                        TESTING user_profile_setemail                        ##
#################################################################################
# function inputs: token, email
# function returns: 
'''
Assumptions
    - If given no email input, it should throw an error
'''
#Ensure the function does not return anything
def test_user_profile_setemail_no_return(register_account):
    token = register_account['token']
    assert user_profile_setemail(token, 'dantheman@gmail.com') == None

#This function ensures that the updated email is the same as the input
def test_user_profile_setemail_updated_values(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token, u_id)
    assert dictionary['email'] == 'example@gmail.com'
    user_profile_setemail(token, 'dantheman@gmail.com')
    dictionary = user_profile(token, u_id)
    assert dictionary['email'] == 'dantheman@gmail.com'

#This should cause the function to raise an error as the token is invalid
def test_user_profile_setemail_invalid_token(register_account):
    token = 'wrong token'
    with pytest.raises(AccessError):
        user_profile_setemail(token, 'dantheman@gmail.com')

#This should cause the function to raise an error as the email is invalid
def test_user_profile_setemail_not_valid(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setemail(token, 'dan@email')

#An empty string as an email should make the function raise an error
def test_user_profile_setemail_no_input(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setemail(token, '')

#################################################################################
##                        TESTING user_profile_sethandle                       ##
#################################################################################
# user_profile_sethandle tests
# function inputs: token, handle_str
# function returns: 
'''
Assumptions
- Handle should not be the same as one that already exists
'''
#Ensure the function does not return anything
def test_user_profile_sethandle_no_return(register_account):
    token = register_account['token']
    assert user_profile_sethandle(token, 'dantheman') == None

#This function ensures that the updated handle is the same as the input
def test_user_profile_sethandle_updated_values(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token, u_id)
    assert dictionary['handle_str'] == 'danman'
    user_profile_sethandle(token, 'dantheman')
    dictionary = user_profile(token, u_id)
    assert dictionary['handle_str'] == 'dantheman'
    
#Incorrect token should raise an error
def test_user_profile_set_handle_invalid_token(register_account):
    token = 'wrong token'
    with pytest.raises(AccessError):
        user_profile_sethandle(token, 'dantheman')

#Function should raise an error as the handle is > 20 characters
def test_user_profile_sethandle_too_long(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_sethandle(token, 'dantheman12345678901234567890')

#No handle input should raise an error
def test_user_profile_sethandle_no_input(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_sethandle(token, '')

#This tests to see if the user handle already exists
def test_user_profile_sethandle_already_exists(register_account):
    list_of_users.append({'handle_str': 'RajeshKumar', 'email': 'rajeshkumar@gmail.com', 'password': 'V@lidPassword123', 'u_id': 1, 'token' : 12345, 'reset_code': None, 'name_first': 'Rajesh', 'name_last': 'Kumar', 'app_permission_id': 2})
    token = register_account['token']
    #Should raise an error as we cannot have two of the same handles
    with pytest.raises(ValueError):
        user_profile_sethandle(token, 'RajeshKumar')

#################################################################################
##                  TESTING user_profiles_uploadphoto                          ##
#################################################################################
# function inputs: token, img_url, x_start, y_start, x_end, y_end
# function returns: 
'''
# This tests passes if the function works correctly, does not pass back any errors
def test_user_profiles_uploadphoto_no_return(register_account):
    token = register_account['token']
    assert user_profiles_uploadphoto(token, 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', 0, 0, 2864, 1861) == None
'''
def test_user_profiles_upload_photo_invalid_token(register_account):
    token = 'wrong token'
    with pytest.raises(AccessError):
        user_profiles_uploadphoto(token, 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', 0, 0, 2864, 1861)

# This tests the function with an invalid photo url, a HTTP status that is not 200
def test_user_profiles_uploadphoto_not_200(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token, 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Potates.jpg', 0, 0, 2864, 1861)
        
# This function passes x,y coordinates that are not possible (e.g x_end > x_start)
def test_user_profiles_uploadphoto_wrong_dimensions(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token, 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', 2864, 1861, 0, 0)
        
# This function passes x coordinates that are larger than the photo
def test_user_profiles_uploadphoto_larger_X_dimensions(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token, 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', 2865, 0, 2867, 1861)

# This function passes y coordinates that are larger than the photo
def test_user_profiles_uploadphoto_larger_Y_dimensions(register_account):
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token, 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', 0, 1862, 2864, 1865)
