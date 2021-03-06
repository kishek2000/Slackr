""" user tests """
import sys
import pytest
sys.path.append('server/')
from functions.user_functions import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle, user_profiles_uploadphoto, users_all
from functions.auth_functions import auth_register
from functions.helper_functions import reset_data, get_user_details, list_of_users
from functions.Errors import AccessError, ValueError

@pytest.fixture
def register_account():
    """ register_account fixture """
    reset_data()
    auth_register(email='example2@gmail.com', password='P@ssword123', name_first='Epic', name_last='Style')
    return auth_register(email='example@gmail.com', password='Go0dPa>sword', name_first='dan', name_last='man')

#################################################################################
##                           TESTING user_profile                              ##
#################################################################################
# function inputs: token, u_id
# function returns: email, name_first, name_last, handle_str

#This test ensures that the function returns the correct values
def test_user_profile_correct_return(register_account):
    """ test_user_profile_correct_return """
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token=token, u_id=u_id)
    assert dictionary['email'] == 'example@gmail.com'
    assert dictionary['name_first'] == 'dan'
    assert dictionary['name_last'] == 'man'
    assert dictionary['handle_str'] == 'danman'

#This test ensures that the returned string is not incorrect
def test_user_profile_incorrect_return(register_account):
    """ test_user_profile_incorrect_return """
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token=token, u_id=u_id)
    assert dictionary['handle_str'] != 'dantheman'

def test_user_profile_token_nonexistent(register_account):
    """ test_user_profile_token_nonexistent """
    returning_dictionary = get_user_details(-1)
    assert returning_dictionary == {}

#This tests that that u_id is incorrect
def test_user_profile_invalid_id(register_account):
    """ test_user_profile_invalid_id """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile(token=token, u_id='wrong')

#This tests that that token is incorrect
def test_user_profile_invalid_token(register_account):
    """ test_user_profile_invalid_token """
    u_id = register_account['u_id']
    with pytest.raises(AccessError):
        user_profile(token='wrong token', u_id=u_id)

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
    """ test_user_profile_setname_no_return """
    token = register_account['token']
    assert user_profile_setname(token=token, name_first='danny', name_last='manny') is None

#This function ensures that the updated names are the same as the input
def test_user_profile_setname_updated_values(register_account):
    """ test_user_profile_setname_updated_values """
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token=token, u_id=u_id)
    assert dictionary['name_first'] == 'dan'
    assert dictionary['name_last'] == 'man'
    user_profile_setname(token=token, name_first='danny', name_last='manny')
    dictionary = user_profile(token=token, u_id=u_id)
    assert dictionary['name_first'] == 'danny'
    assert dictionary['name_last'] == 'manny'

#An invalid token should raise an error
def test_user_profile_setname_invalid_token():
    """ test_user_profile_setname_invalid_token """
    token = 'wrong token'
    with pytest.raises(AccessError):
        user_profile_setname(token=token, name_first='danny', name_last='manny')

#Name_first cannot be greater than 50 characters, so it should raise an error
def test_user_profile_setname_long_name_first(register_account):
    """ test_user_profile_setname_long_name_first """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setname(token=token, name_first='123456789012345678901234567890123456789012345678901', name_last='manny')

#Name_last cannot be greater than 50 characters, so it should raise an error
def test_user_profile_setname_long_name_last(register_account):
    """ test_user_profile_setname_long_name_last """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setname(token=token, name_first='danny', name_last='123456789012345678901234567890123456789012345678901')

#An empty string cannot be a name, so it should raise an error
def test_user_profile_setname_no_input(register_account):
    """ test_user_profile_setname_no_input """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setname(token=token, name_first='', name_last='')

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
    """ test_user_profile_setemail_no_return """
    token = register_account['token']
    assert user_profile_setemail(token=token, email='dantheman@gmail.com') is None

#This function ensures that the updated email is the same as the input
def test_user_profile_setemail_updated_values(register_account):
    """ test_user_profile_setemail_updated_values """
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token=token, u_id=u_id)
    assert dictionary['email'] == 'example@gmail.com'
    user_profile_setemail(token=token, email='dantheman@gmail.com')
    dictionary = user_profile(token=token, u_id=u_id)
    assert dictionary['email'] == 'dantheman@gmail.com'

#This should cause the function to raise an error as the token is invalid
def test_user_profile_setemail_invalid_token():
    """ test_user_profile_setemail_invalid_token """
    token = 'wrong token'
    with pytest.raises(AccessError):
        user_profile_setemail(token=token, email='dantheman@gmail.com')

#This should cause the function to raise an error as the email is invalid
def test_user_profile_setemail_not_valid(register_account):
    """ test_user_profile_setemail_not_valid """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setemail(token=token, email='dan@email')

#An empty string as an email should make the function raise an error
def test_user_profile_setemail_no_input(register_account):
    """ test_user_profile_setemail_no_input """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_setemail(token=token, email='')

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
    """ test_user_profile_sethandle_no_return """
    token = register_account['token']
    assert user_profile_sethandle(token=token, handle_str='dantheman') is None

#This function ensures that the updated handle is the same as the input
def test_user_profile_sethandle_updated_values(register_account):
    """ test_user_profile_sethandle_updated_values """
    token = register_account['token']
    u_id = register_account['u_id']
    dictionary = user_profile(token=token, u_id=u_id)
    assert dictionary['handle_str'] == 'danman'
    user_profile_sethandle(token=token, handle_str='dantheman')
    dictionary = user_profile(token=token, u_id=u_id)
    assert dictionary['handle_str'] == 'dantheman'

#Incorrect token should raise an error
def test_user_profile_set_handle_invalid_token():
    """ test_user_profile_set_handle_invalid_token """
    token = 'wrong token'
    with pytest.raises(AccessError):
        user_profile_sethandle(token=token, handle_str='dantheman')

#Function should raise an error as the handle is > 20 characters
def test_user_profile_sethandle_too_long(register_account):
    """ test_user_profile_sethandle_too_long """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_sethandle(token=token, handle_str='dantheman12345678901234567890')

#No handle input should raise an error
def test_user_profile_sethandle_no_input(register_account):
    """ test_user_profile_sethandle_no_input """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profile_sethandle(token=token, handle_str='')

#This tests to see if the user handle already exists
def test_user_profile_sethandle_already_exists(register_account):
    """ test_user_profile_sethandle_already_exists """
    list_of_users.append({'handle_str': 'RajeshKumar', 'email': 'rajeshkumar@gmail.com', 'password': 'V@lidPassword123', 'u_id': 1, 'token' : 12345, 'reset_code': None, 'name_first': 'Rajesh', 'name_last': 'Kumar', 'app_permission_id': 2})
    token = register_account['token']
    #Should raise an error as we cannot have two of the same handles
    with pytest.raises(ValueError):
        user_profile_sethandle(token=token, handle_str='RajeshKumar')

#################################################################################
##                  TESTING user_profiles_uploadphoto                          ##
#################################################################################
# function inputs: token, profile_img_url, x_start, y_start, x_end, y_end
# function returns:

# This function tests that the code throws no errors
def test_user_profiles_uploadphoto_no_errors(register_account):
    """ test_user_profiles_uploadphoto_no_errors """
    token = register_account['token']
    user_profiles_uploadphoto(token=token, img_url='https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', x_start='0', y_start='0', x_end='2864', y_end='1861')

def test_user_profiles_upload_photo_invalid_token():
    """ test_user_profiles_upload_photo_invalid_token """
    token = 'wrong token'
    with pytest.raises(AccessError):
        user_profiles_uploadphoto(token=token, img_url='https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', x_start='0', y_start='0', x_end='2864', y_end='1861')

# This tests the function with an invalid photo url, a HTTP status that is not 200
def test_user_profiles_uploadphoto_not_200(register_account):
    """ test_user_profiles_uploadphoto_not_200 """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token=token, img_url='https://upload.wikimedia.org/wikipedia/commons/a/ab/Potates.jpg', x_start='0', y_start='0', x_end='2864', y_end='1861')

# This function passes x,y coordinates that are not possible (e.g x_end > x_start)
def test_user_profiles_uploadphoto_wrong_dimensions(register_account):
    """ test_user_profiles_uploadphoto_wrong_dimensions """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token=token, img_url='https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', x_start='2864', y_start='1861', x_end='0', y_end='0')

# This function passes x coordinates that are larger than the photo
def test_user_profiles_uploadphoto_larger_X_dimensions(register_account):
    """ test_user_profiles_uploadphoto_larger_X_dimensions """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token=token, img_url='https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', x_start='2865', y_start='0', x_end='2867', y_end='1861')

# This function passes y coordinates that are larger than the photo
def test_user_profiles_uploadphoto_larger_Y_dimensions(register_account):
    """ test_user_profiles_uploadphoto_larger_Y_dimensions """
    token = register_account['token']
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token=token, img_url='https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg', x_start='0', y_start='1862', x_end='2864', y_end='1865')

#################################################################################
##                            TESTING users_all                                ##
#################################################################################
# users_all tests
# function inputs: token
# function returns: dictionary containing list of users

#Ensure the function does not return anything
def test_users_all_correct_return(register_account):
    """ test_users_all_correct_return """
    token = register_account['token']
    assert users_all(token=token) == {'users': [{'handle_str': 'EpicStyle', 'email': 'example2@gmail.com', 'u_id': 1, 'name_first': 'Epic', 'name_last': 'Style', 'profile_img_url': None}, {'handle_str': 'danman', 'email': 'example@gmail.com', 'u_id': 2, 'name_first': 'dan', 'name_last': 'man', 'profile_img_url': None}]}

#This should cause the function to raise an error as the token is invalid
def test_users_all_invalid_token():
    """ test_users_all_invalid_token """
    token = 'wrong token'
    with pytest.raises(AccessError):
        users_all(token=token)

reset_data()
