'''
File contains tests for the auth functions
'''
import sys
import pytest
sys.path.append("server/")
from functions.auth_functions import (auth_register, auth_login, auth_logout,
                                      auth_passwordreset_request, auth_passwordreset_reset)
from functions.helper_functions import (reset_data, generate_token, get_user_details,
                                        check_valid_u_id, check_valid_handle,
                                        get_user_app_permission, check_valid_token)

#################################################################################
##                              AUTH TESTS                                     ##
#################################################################################


@pytest.fixture
def _registered_user_1():
    '''Setting up registered user for tests'''
    reset_data()

    user_details = auth_register(email="PokemonMaster@gmail.com",
                                 password="validP@sswrd1",
                                 name_first="Ash",
                                 name_last="Ketcham")

    user_u_id = user_details['u_id']
    user_token = user_details['token']

    return {'u_id': user_u_id, 'token' : user_token}

@pytest.fixture
def _registered_user_2():
    '''Setting up second registered user for tests'''
    reset_data()

    user_details = user_u_id, user_token = auth_register(email="TheRealPokemonMaster@gmail.com",
                                                         password="ValidP@sswordRocks1",
                                                         name_first="Gary",
                                                         name_last="Oak")

    user_u_id = user_details['u_id']
    user_token = user_details['token']

    return {'u_id': user_u_id, 'token' : user_token}


#################################################################################
##                           TESTING auth_login                                ##
#################################################################################

def test_auth_login_correct_details(_registered_user_1):
    '''Tests login with valid details provided'''
    email = "PokemonMaster@gmail.com"
    password = "validP@sswrd1"

    #Should produce no errors as the user is registered in the fixture
    auth_login(email=email, password=password)


def test_auth_login_invalid_email(_registered_user_1):
    '''Tests login with invalid email'''
    email = "PokemonMaster"
    password = "validp@ssword1"

    #Should produce ValueError as an invalid email is provided
    with pytest.raises(ValueError):
        auth_login(email=email, password=password)


def test_auth_login_email_not_registered():
    '''Tests login with email which is not registered'''
    email = "nonRegisterdEmail@gmail.com"
    password = "validp@ssword1"

    #Should produce ValueError as an invalid email entered does not belong to a user
    with pytest.raises(ValueError):
        auth_login(email=email, password=password)


def test_auth_login_incorrect_password(_registered_user_1):
    '''Tests login with incorrect password'''
    email = "PokemonMaster@gmail.com"
    password = "This_Is_Definetely_Not_The_Right_Password"

    #Should produce ValueError as an incorrect password is provided
    with pytest.raises(ValueError):
        auth_login(email=email, password=password)


def test_auth_login_email_and_password_mismatch(_registered_user_1, _registered_user_2):
    '''Tests login with email not matching password'''
    email = "TheRealPokemonMaster@gmail.com"
    password = "validp@ssword1"

    #Should produce ValueError as the password does not match to the email provided
    with pytest.raises(ValueError):
        auth_login(email=email, password=password)


def test_auth_login_valid_token_generated(_registered_user_1):
    '''Testing login produces valid token'''
    user_token = _registered_user_1['token']

    #Should produce no errors

    assert user_token == generate_token("PokemonMaster@gmail.com")


def test_auth_login_valid_u_id_generated(_registered_user_1):
    '''Testing login produces valid u_id'''
    user_u_id = _registered_user_1['u_id']

    #Should produce no errors

    assert check_valid_u_id(user_u_id) is True


#################################################################################
##                           TESTING auth_logout                               ##
#################################################################################

def test_auth_logout_active_token_provided(_registered_user_1):
    '''Tests logout with valid details provided'''
    user_token = _registered_user_1['token']

    #Check if the token is valid
    assert check_valid_token(user_token) is True

    #The function auth_logout should invalidate the token provided, logging the user out
    auth_logout(token=user_token)

    #Check if the token is now invalid
    assert check_valid_token(user_token) is False


def test_auth_logout_inactive_token_provided(_registered_user_2):
    '''Tests logout with invalid token provided'''
    user_token = _registered_user_2['token']

    #Check if the token is valid
    assert check_valid_token(user_token) is True

    #The function auth_logout should invalidate the token provided, logging the user out
    auth_logout(token=user_token)

    #Check if the token is now invalid
    assert check_valid_token(user_token) is False

    #The function auth_logout should do nothing, as the token provided is already invalid
    auth_logout(token=user_token)

    #Check if the token is still invalid
    assert check_valid_token(user_token) is False

#################################################################################
##                           TESTING auth_register                             ##
#################################################################################

def test_auth_register_correct_details():
    '''Tests registering with correct details provided'''
    reset_data()

    email_1 = "AshKetchum1@yahoo.com"
    password_1 = "IWann@BeTheVeryBest123"
    name_first_1 = "Ash"
    name_last_1 = "Ketchum"

    email_2 = "GaryOak@yahoo.com"
    password_2 = "I@mTheVeryBest123"
    name_first_2 = "Gary"
    name_last_2 = "Oak"

    #Should produce no errors
    user_details_1 = auth_register(email=email_1, password=password_1,
                                   name_first=name_first_1, name_last=name_last_1)
    user_details_2 = auth_register(email=email_2, password=password_2,
                                   name_first=name_first_2, name_last=name_last_2)

    assert get_user_app_permission(user_details_1['u_id']) == 1
    assert get_user_app_permission(user_details_2['u_id']) == 3

def test_auth_register_invalid_email():
    '''Tests registering with invalid email provided'''
    reset_data()

    email = "AshKetchum2@yaheecom"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"

    #Should produce ValueError as an invalid email is provided
    with pytest.raises(ValueError):
        auth_register(email=email, password=password, name_first=name_first, name_last=name_last)


def test_auth_register_email_already_used(_registered_user_1):
    '''Tests registering with already registered email'''
    email = "PokemonMaster@gmail.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"

    #Should produce ValueError as the provided email is already being used by another user
    with pytest.raises(ValueError):
        auth_register(email=email, password=password, name_first=name_first, name_last=name_last)


def test_auth_register_invalid_password():
    '''Tests registering with invalid password provided'''
    reset_data()

    email = "AshKetchum3@yahoo.com"
    password = "ILoveGary"
    name_first = "Ash"
    name_last = "Ketchum"

    #Should produce ValueError as invalid password has been provided
    with pytest.raises(ValueError):
        auth_register(email=email, password=password, name_first=name_first, name_last=name_last)

def test_auth_register_first_name_too_long():
    '''Tests registering with too long first name'''
    reset_data()

    email = "AshKetchum4@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas Onyetenyevwe Ugwemubwem Ossas"
    name_last = "Ketchum"

    #Should produce ValueError as the first name is greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email=email, password=password, name_first=name_first, name_last=name_last)


def test_auth_register_last_name_too_long():
    '''Tests registering with too long last name'''
    reset_data()

    email = "AshKetchum5@gmail.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "supercalifragilisticexpialidocious supercalifragilisticexpialidocious"

    #Should produce ValueError as the last name is greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email=email, password=password, name_first=name_first, name_last=name_last)


def test_auth_register_first_and_last_name_too_long():
    '''Tests registering with too long first and last name provided'''
    reset_data()

    email = "AshKetchum6@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas Onyetenyevwe Ugwemubwem Ossas"
    name_last = "supercalifragilisticexpialidocious supercalifragilisticexpialidocious"

    #Should produce ValueError as the first and last name are greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email=email, password=password, name_first=name_first, name_last=name_last)

def test_auth_register_first_name_long_handler():
    '''Test which check handle with long first name'''
    reset_data()

    email = "AshKetchum6@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "UvuvwevwevweOsassz"
    name_last = "Super"

    user_details = auth_register(email=email, password=password, name_first=name_first,
                                 name_last=name_last)

    token = user_details['token']
    #obtain handle
    get_handle = get_user_details(token)
    handle_str = get_handle['handle_str']

    assert check_valid_handle(handle_str) is True


def test_auth_register_last_name_long_handler():
    '''Test which check handle with long last name'''
    reset_data()

    email = "AshKetchum6@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Super"
    name_last = "UvuvwevwevweOsasszkilo"

    user_details = auth_register(email=email, password=password, name_first=name_first,
                                 name_last=name_last)

    token = user_details['token']
    #obtain handle
    get_handle = get_user_details(token)
    handle_str = get_handle['handle_str']

    assert check_valid_handle(handle_str) is True

def test_auth_register_first_and_last_name_long_handler():
    '''Test which check handle with long first and last name'''
    reset_data()

    email = "AshKetchum6@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Supercalifragilisticexpialidocious"
    name_last = "UvuvwevwevweOsassz"

    user_details = auth_register(email=email, password=password, name_first=name_first,
                                 name_last=name_last)

    token = user_details['token']
    #obtain handle
    get_handle = get_user_details(token)
    handle_str = get_handle['handle_str']

    assert check_valid_handle(handle_str) is True


def test_auth_register_valid_token_generated():
    '''Tests valid token provided after registering'''
    reset_data()

    email = "AshKetchum7@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"

    #Should produce no errors
    user_details = auth_register(email=email, password=password, name_first=name_first,
                                 name_last=name_last)

    user_token = user_details['token']

    assert check_valid_token(user_token) is True

def test_auth_register_valid_u_id_generated():
    '''Tests valid u_id provided after registering'''
    reset_data()

    email = "AshKetchum8@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"

    #Should produce no errors
    user_details = auth_register(email=email, password=password, name_first=name_first,
                                 name_last=name_last)

    print(user_details)
    user_u_id = user_details['u_id']

    assert check_valid_u_id(user_u_id) is True

def test_auth_register_invalid_u_id_generated():
    '''Tests invalid u_id helper with invalid details'''
    #There are no negative
    assert check_valid_u_id(-1) is False


#################################################################################
##                    TESTING auth_passwordreset_request                       ##
#################################################################################

def test_auth_passwordreset_request_valid_email_provided(_registered_user_1):
    '''Tests requesting a reset code for password reset with valid email'''
    reset_email = "PokemonMaster@gmail.com"

    #Should produce no errors as the provided email for the password reset is valid
    auth_passwordreset_request(email=reset_email)


def test_auth_passwordreset_request_invalid_email_provided(_registered_user_1):
    '''Tests requesting a reset code for password reset with invalid email'''
    reset_email = "PokemonMaster"

    #Should produce a ValueError as an invalid email is provided
    with pytest.raises(ValueError):
        auth_passwordreset_request(email=reset_email)


def test_auth_passwordreset_request_non_registered_email_provided():
    '''Tests requesting a reset code for password reset with non registerd email provided'''
    reset_email = "non_registered_email@gmail.com"

    #Should produce a ValueError as the email provided is not regesitered
    with pytest.raises(ValueError):
        auth_passwordreset_request(email=reset_email)


#################################################################################
##                    TESTING auth_passwordreset_reset                         ##
#################################################################################

def test_auth_passwordreset_reset_correct_details(_registered_user_1):
    '''Tests resetting password with valid details provided'''
    #Registered user requests a reset code
    auth_passwordreset_request(email="PokemonMaster@gmail.com")

    reset_code = get_user_details(_registered_user_1['token'])['reset_code']

    new_password = "ThisIsAV@lidNewPassword123"

    #Should produce no errors
    auth_passwordreset_reset(reset_code, new_password)

    #Test logging in which should produce no errors
    auth_login(email="PokemonMaster@gmail.com", password="ThisIsAV@lidNewPassword123")

def test_auth_passwordreset_reset_incorrect_reset_code(_registered_user_1):
    '''Tests resetting password with incorrect reset code provided'''
    #Registered user requests a reset code
    auth_passwordreset_request(email="PokemonMaster@gmail.com")

    reset_code = -1

    new_password = "ThisIsAV@lidNewPassword123"

    #Should produce a ValueError as an incorrect reset_code is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)


def test_auth_passwordreset_reset_invalid_password(_registered_user_1):
    '''Tests resetting password with invalid new password provided'''
    #Registered user requests a reset code
    auth_passwordreset_request(email="PokemonMaster@gmail.com")

    reset_code = get_user_details(_registered_user_1['token'])['reset_code']

    new_password = "password"

    #Should produce a ValueError as an invalid password is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)


def test_auth_passwordreset_reset_invalid_password_and_reset_code(_registered_user_1):
    '''Tests resetting password with all incorrect details provided'''
    #Registered user requests a reset code
    auth_passwordreset_request(email="PokemonMaster@gmail.com")

    reset_code = -1

    new_password = "password"

    #Should produce a ValueError as an reset code and invalid password is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)
