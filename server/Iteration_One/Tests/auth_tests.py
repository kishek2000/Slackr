import pytest

######TESTS FOR auth_login#######

'''

Assume these are the usernames and passwords for existing slackr users

1) Username: sorakumar@gmail.com
   Password: Sora@IsGreat413
   
2) Username: Pik@chuEatsSquirtle@hotmail.com
   Password: 123PokemonDontEatPokemon123

Assume we have a function token_is_valid() which returns either True if token is active
and False inactive.

Similalry we have a funtion, u_id_is_valid() which returns either True or False

'''

def test_auth_login_correct_details():

    email = "sorakumar@gmail.com"
    password = "Sor@IsGreat413"
    
    #Should produce no errors
    auth_login(email, password)
    
    
def test_auth_login_invalid_email():

    email = "sorakumarm"
    password = "Sor@IsGreat413"
    
    #Should produce ValueError as an invalid email is provided
    with pytest.raises(ValueError):
        auth_login(email, password)
        
        
def test_auth_login_email_not_registered():

    email = "soraDesai@gmail.com"
    password = "Sor@IsGreat413"
    
    #Should produce ValueError as an invalid email entered does not belong to a user
    with pytest.raises(ValueError):
        auth_login(email, password)
          
        
def test_auth_login_incorrect_password():

    email = "Pik@chuEatsSquirtle@hotmail.com"
    password = "This_Is_Definetely_Not_The_Right_Password"
    
    #Should produce ValueError as an incorrect password is provided
    with pytest.raises(ValueError):
        auth_login(email, password)
        
        
def test_auth_login_email_and_password_mismatch():

    email = "sorakumar@gmail.com"
    password = "123PokemonDontEatPokemon!123"
    
    #Should produce ValueError as the password does not match to the email provided, hence is incorrect
    with pytest.raises(ValueError):
        auth_login(email, password)
        
        
def test_auth_login_valid_token_generated():
    
    email = "sorakumar@gmail.com"
    password = "Sor@IsGreat413"
    
    #Should produce no errors
    returned_u_id, returned_token = auth_login(email, password)
    
    assert(token_is_valid(returned_token) == True)    
 
def test_auth_login_valid_u_id_generated():
    
    email = "sorakumar@gmail.com"
    password = "Sor@IsGreat413"
    
    #Should produce no errors
    returned_u_id, returned_token = auth_login(email, password)
    
    assert(u_id_is_valid(returned_u_id) == True)  
        
######TESTS FOR auth_logout#######

'''
Assume there is an active token_1 = "x" which is generated at login, which is passed into
the other function

Assume there is an inactive token_2 = "y" which is generated at login, which is passed into
the other function

Assume we have a function token_is_valid() which returns either True if token is active
and False inactive.

'''

def test_auth_logout_active_token_provided():

    token_1 = "x"
    
    #Check if the token is valid
    assert(token_is_valid(token_1) == True)    
    
    #The function auth_logout should invalidate the token provided, logging the user out
    auth_logout(token_1)
    
    #Check if the token is infact valid
    assert(token_is_valid(token_1) == False)    
    
def test_auth_logout_inactive_token_provided():

    token_2 = "y"
    
    #Check if the token is invalid
    assert(token_is_valid(token_1) == False)    
    
    #The function auth_logout should do nothing, as the token provided is already invalid
    auth_logout(token_1)
    
    #Check if the token is infact valid
    assert(token_is_valid(token_1) == False)    
    

######TESTS FOR auth_register#######

'''

Assume these are valid details provided at registration for new slackr users

1) Email: AshKetchum@yahoo.com
   Password: IWann@BeTheVeryBest123
   First Name: Ash
   Last Name: Ketchum   
   
2) Email: GaryOak@hotmail.com
   Password: IAmAlre@dyTheVeryBest123
   First Name: Gary
   Last Name: Oak
   
Note: Assuming an accepted password has the following requirements (A function called 
is_valid_password() will check against these requirements and return either True or False) :-
    
    - Passoword length between 5 and 20 characters inclusive
    - At least 1 upper character
    - At least 1 lower case character
    - At least 1 number
    - At least 1 special character   
   
Assume these are the emails for existing slackr users

1) Email: sorakumar@gmail.com
   
2) Email: PikachuEatsSquirtle@hotmail.com
   
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
        
def test_auth_register_email_already_used():

    email = "sorakumar@gmail.com"
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

    email = "AshKetchum@yaheecom"
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
    
    email = "sorakumar@gmail.com"
    password = "Sor@IsGreat413"
    
    #Should produce no errors
    returned_u_id, returned_token = auth_login(email, password)
    
    assert(token_is_valid(returned_token) == True)    


def test_auth_register_token_generated():
    
    email = "AshKetchum@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    returned_u_id, returned_token = auth_register(email, password, name_first, name_last) 
    
    assert(token_is_valid(returned_token) == True)  
 
 
def test_auth_register_valid_u_id_generated():
    
    email = "AshKetchum@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    returned_u_id, returned_token = auth_register(email, password, name_first, name_last) 
    
    assert(u_id_is_valid(returned_u_id) == True)       
    
    
######TESTS FOR auth_passwordreset_request#######  
        
'''

Assume these are the emails for existing slackr users

1) Email: sorakumar@gmail.com

'''        

def test_auth_passwordreset_request_valid_email_provided():

    email = "sorakumar@gmail.com"      
    
    #Should produce no errors as the provided email for the password reset is valid
    auth_passwordreset_request(email)    

 
def test_auth_passwordreset_request_invalid_email_provided():

    email = "sorakumar"      
    
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

Assume reset_code = 123 is a valid reset code and reset_code = 111 is invalid

Note: Assuming an accepted new password for reset has the following requirements (A function called 
is_valid_password() will check against these requirements and return either True or False) :-
    
    - Passoword length between 5 and 20 characters inclusive
    - At least 1 upper character
    - At least 1 lower case character
    - At least 1 number
    - At least 1 special character 

'''          
        
def test_auth_passwordreset_reset_correct_details():

    reset_code = 123
    new_password = "ThisIsAV@lidNewPassword123"
    
    #Should produce no errors
    auth_passwordreset_reset(reset_code, new_password)    
    
    
def test_auth_passwordreset_reset_incorrect_reset_code():

    reset_code = 111
    new_password = "ThisIsAV@lidNewPassword123"
    
    #Should produce a ValueError as an incorrect reset_code is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)  


def test_auth_passwordreset_reset_invalid_password():

    reset_code = 123
    new_password = "password"
    
    #Should produce a ValueError as an invalid password is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)  


def test_auth_passwordreset_reset_invalid_password_and_reset_code():

    reset_code = 111
    new_password = "password"
    
    #Should produce a ValueError as an reset code and invalid password is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)  

 
