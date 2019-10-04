import pytest

'''
Assume an accepted password has the following requirements (A function called 
is_valid_password() will check against these requirements and return either True or False) :-
    
    - Passoword length between 5 and 20 characters inclusive
    - At least 1 upper character
    - At least 1 lower case character
    - At least 1 number
    - At least 1 special character
    
'''

@pytest.fixture
def registered_user_1():
    return auth_register("PokemonMaster@gmail.com", "validp@ssword", "Ash", "Ketcham")

@pytest.fixture
def registered_user_2():
    return auth_register("TheRealPokemonMaster@gmail.com", "ValidP@sswordRocks", "Gary", "Oak")
    
######TESTS FOR auth_login#######

'''

Assume we have a function token_is_valid() which returns either True if token is active
and False inactive.

Similalry we have a funtion, u_id_is_valid() which returns either True or False

'''

def test_auth_login_correct_details(registered_user_1):

    email = "PokemonMaster@gmail.com"
    password = "validp@ssword"
    
    #Should produce no errors as the user is registered in the fixture
    auth_login(email, password)
    
    
def test_auth_login_invalid_email(registered_user_1):

    email = "PokemonMaster"
    password = "validp@ssword"
    
    #Should produce ValueError as an invalid email is provided
    with pytest.raises(ValueError):
        auth_login(email, password)
        
        
def test_auth_login_email_not_registered():

    email = "nonRegisterdEmail@gmail.com"
    password = "validp@ssword"
    
    #Should produce ValueError as an invalid email entered does not belong to a user
    with pytest.raises(ValueError):
        auth_login(email, password)
          
        
def test_auth_login_incorrect_password(registered_user):

    email = "PokemonMaster@gmail.com"
    password = "This_Is_Definetely_Not_The_Right_Password"
    
    #Should produce ValueError as an incorrect password is provided
    with pytest.raises(ValueError):
        auth_login(email, password)
        
        
def test_auth_login_email_and_password_mismatch(registered_user_1, registered_user_2):

    email = "TheRealPokemonMaster@gmail.com"
    password = "validp@ssword"
    
    #Should produce ValueError as the password does not match to the email provided, hence is incorrect
    with pytest.raises(ValueError):
        auth_login(email, password)
        
        
def test_auth_login_valid_token_generated(registered_user_1):
    
    email = "PokemonMaster@gmail.com"
    password = "validp@ssword"
    
    #Should produce no errors
    user_token = registered_user_1['token']
    
    assert(token_is_valid(returned_token) == True)    
 
def test_auth_login_valid_u_id_generated():
    
    email = "PokemonMaster@gmail.com"
    password = "validp@ssword"
    
    #Should produce no errors
    user_u_id = registered_user_1['u_id']
    
    assert(u_id_is_valid(returned_u_id) == True)  
        
######TESTS FOR auth_logout#######

'''

Assume we have a function token_is_valid() which returns either True if token is active
and False inactive.

'''

def test_auth_logout_active_token_provided(registered_user_1):

    user_token = registered_user_1['token']
    
    #Check if the token is valid
    assert(token_is_valid(user_token) == True)    
    
    #The function auth_logout should invalidate the token provided, logging the user out
    auth_logout(user_token)
    
    #Check if the token is now invalid
    assert(token_is_valid(user_token) == False)    
    
    
def test_auth_logout_inactive_token_provided(registered_user_1):

    user_token = registered_user_1['token']
    
    #Check if the token is valid
    assert(token_is_valid(user_token) == True)    
    
    #The function auth_logout should invalidate the token provided, logging the user out
    auth_logout(user_token)
    
    #Check if the token is now invalid
    assert(token_is_valid(user_token) == False)
    
    #The function auth_logout should do nothing, as the token provided is already invalid
    auth_logout(token_1)
    
    #Check if the token is still invalid
    assert(token_is_valid(token_1) == False)    
    

######TESTS FOR auth_register#######

'''
Assume an accepted password has the following requirements (A function called 
is_valid_password() will check against these requirements and return either True or False) :-
    
    - Passoword length between 5 and 20 characters inclusive
    - At least 1 upper character
    - At least 1 lower case character
    - At least 1 number
    - At least 1 special character
   
Assume we have a function token_is_valid() which returns either True if token is active
and False inactive.

Similalry we have a funtion, u_id_is_valid() which returns either True or False

'''
def test_auth_register_correct_details():

    email = "AshKetchum@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    auth_register(email, password, name_first, name_last)
    
def test_auth_register_invalid_email():

    email = "AshKetchum@yaheecom"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce ValueError as an invalid email is provided
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)
        
def test_auth_register_email_already_used(registered_user_1):

    email = "PokemonMaster@gmail.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce ValueError as the provided email is already being used by another user
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)    


def test_auth_register_invalid_password():

    email = "AshKetchum@yahoo.com"
    password = "ILoveGary"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce ValueError as invalid password has been provided
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)  


def test_auth_register_first_name_too_long():

    email = "AshKetchum@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas Onyetenyevwe Ugwemubwem Ossas"
    name_last = "Ketchum"
    
    #Should produce ValueError as the first name is greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)  
     
        
def test_auth_register_last_name_too_long():

    email = "AshKetchum@yaheecom"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "supercalifragilisticexpialidocious supercalifragilisticexpialidocious"
    
    #Should produce ValueError as the last name is greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)     
        
def test_auth_register_first_and_last_name_too_long():

    email = "AshKetchum@yaheecom"
    password = "IWann@BeTheVeryBest123"
    name_first = "Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas Onyetenyevwe Ugwemubwem Ossas"
    name_last = "supercalifragilisticexpialidocious supercalifragilisticexpialidocious"
    
    #Should produce ValueError as the first and last name are greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last) 
        
     
def test_auth_register_valid_token_generated():
    
    email = "AshKetchum@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    user_token = auth_register(email, password, name_first, name_last)['token']
    
    assert(token_is_valid(user_token) == True)    
 
 
 
def test_auth_register_valid_u_id_generated():
    
    email = "AshKetchum@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    user_u_id = auth_register(email, password, name_first, name_last)['u_id']
    
    assert(u_id_is_valid(user_u_id) == True)       
    
    
######TESTS FOR auth_passwordreset_request#######  
        
    

def test_auth_passwordreset_request_valid_email_provided(registered_user_1):

    email = "PokemonMaster@gmail.com"      
    
    #Should produce no errors as the provided email for the password reset is valid
    auth_passwordreset_request(email)    

 
def test_auth_passwordreset_request_invalid_email_provided(registered_user_1):

    email = "PokemonMaster"      
    
    #Should produce a ValueError as an invalid email is provided
    with pytest.raises(ValueError):
        auth_passwordreset_request(email)   
    
    
def test_auth_passwordreset_request_non_registered_email_provided():

    email = "non_registered_email@gmail.com"      
    
    #Should produce a ValueError as the email provided is not regesitered 
    with pytest.raises(ValueError):
        auth_passwordreset_request(email)    
        
        
######TESTS FOR auth_passwordreset_reset#######          
        
'''
Assume that get_reset_code() provides a valid reset code

Note: Assuming an accepted new password for reset has the following requirements (A function called 
is_valid_password() will check against these requirements and return either True or False) :-
    
    - Passoword length between 5 and 20 characters inclusive
    - At least 1 upper character
    - At least 1 lower case character
    - At least 1 number
    - At least 1 special character 

'''          
        
def test_auth_passwordreset_reset_correct_details():

    reset_code = get_reset_code()
    new_password = "ThisIsAV@lidNewPassword123"
    
    #Should produce no errors
    auth_passwordreset_reset(reset_code, new_password)    
    
    
def test_auth_passwordreset_reset_incorrect_reset_code():

    reset_code = "invalid_reset_code"
    new_password = "ThisIsAV@lidNewPassword123"
    
    #Should produce a ValueError as an incorrect reset_code is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)  


def test_auth_passwordreset_reset_invalid_password():

    reset_code = get_reset_code()
    new_password = "password"
    
    #Should produce a ValueError as an invalid password is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)  


def test_auth_passwordreset_reset_invalid_password_and_reset_code():

    reset_code = "invalid_reset_code"
    new_password = "password"
    
    #Should produce a ValueError as an reset code and invalid password is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)  

 
