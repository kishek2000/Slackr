import sys
import pytest
sys.path.append("Server/")
from functions.auth_functions import *
from functions.helper_functions import *

#################################################################################
##                              AUTH TESTS                                     ##
#################################################################################


@pytest.fixture
def registered_user_1():  
    
    reset_data() 
    
    user_details = auth_register("PokemonMaster@gmail.com", "validP@sswrd1", "Ash", "Ketcham")      
    
    user_u_id = user_details['u_id']
    user_token = user_details['token']
    
    return {'u_id': user_u_id, 'token' : user_token}

  
@pytest.fixture
def registered_user_2():
   
    reset_data() 
    
    user_details = user_u_id, user_token = auth_register("TheRealPokemonMaster@gmail.com", 
                                                         "ValidP@sswordRocks1",
                                                         "Gary", "Oak")    
        
    user_u_id = user_details['u_id']
    user_token = user_details['token']    
           
    return {'u_id': user_u_id, 'token' : user_token}
  

#################################################################################
##                           TESTING auth_login                                ##
#################################################################################    

def test_auth_login_correct_details(registered_user_1):

    email = "PokemonMaster@gmail.com"
    password = "validP@sswrd1"
    
    #Should produce no errors as the user is registered in the fixture
    auth_login(email, password)

 
def test_auth_login_invalid_email(registered_user_1):

    email = "PokemonMaster"
    password = "validp@ssword1"
    
    #Should produce ValueError as an invalid email is provided
    with pytest.raises(ValueError):
        auth_login(email, password)
    
 
def test_auth_login_email_not_registered():

    email = "nonRegisterdEmail@gmail.com"
    password = "validp@ssword1"
    
    #Should produce ValueError as an invalid email entered does not belong to a user
    with pytest.raises(ValueError):
        auth_login(email, password)
 
 
def test_auth_login_incorrect_password(registered_user_1):

    email = "PokemonMaster@gmail.com"
    password = "This_Is_Definetely_Not_The_Right_Password"
    
    #Should produce ValueError as an incorrect password is provided
    with pytest.raises(ValueError):
        auth_login(email, password)

                
def test_auth_login_email_and_password_mismatch(registered_user_1, registered_user_2):

    email = "TheRealPokemonMaster@gmail.com"
    password = "validp@ssword1"
    
    #Should produce ValueError as the password does not match to the email provided, hence is incorrect
    with pytest.raises(ValueError):
        auth_login(email, password)


def test_auth_login_valid_token_generated(registered_user_1):
    
    user_token = registered_user_1['token']
    
    #Should produce no errors
      
    assert(user_token == generate_token("PokemonMaster@gmail.com"))    
 
    

def test_auth_login_valid_u_id_generated(registered_user_1):
    
    user_u_id = registered_user_1['u_id']
    
    #Should produce no errors
    
    assert(check_valid_u_id(user_u_id) == True)  
    

    
#################################################################################
##                           TESTING auth_logout                               ##
#################################################################################        

def test_auth_logout_active_token_provided(registered_user_1):
    
    
    user_token = registered_user_1['token']
    
    #Check if the token is valid
    assert(check_valid_token(user_token) == True)    
    
    #The function auth_logout should invalidate the token provided, logging the user out
    auth_logout(user_token)
    
    #Check if the token is now invalid
    assert(check_valid_token(user_token) == False)    
    

    
def test_auth_logout_inactive_token_provided(registered_user_2):

    user_token = registered_user_2['token']
    
    #Check if the token is valid
    assert(check_valid_token(user_token) == True)    
    
    #The function auth_logout should invalidate the token provided, logging the user out
    auth_logout(user_token)
    
    #Check if the token is now invalid
    assert(check_valid_token(user_token) == False)
    
    #The function auth_logout should do nothing, as the token provided is already invalid
    auth_logout(user_token)
    
    #Check if the token is still invalid
    assert(check_valid_token(user_token) == False)    


    
#################################################################################
##                           TESTING auth_register                             ##
#################################################################################    

def test_auth_register_correct_details():
    
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
    user_details_1 = auth_register(email_1, password_1, name_first_1, name_last_1)
    user_details_2 = auth_register(email_2, password_2, name_first_2, name_last_2)
    
    assert(get_user_app_permission(user_details_1['u_id']) == 1)
    assert(get_user_app_permission(user_details_2['u_id']) == 3)
    
def test_auth_register_invalid_email():
    
    reset_data()
    
    email = "AshKetchum2@yaheecom"
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

    reset_data()
    
    email = "AshKetchum3@yahoo.com"
    password = "ILoveGary"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce ValueError as invalid password has been provided
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)  

def test_auth_register_first_name_too_long():

    reset_data()
    
    email = "AshKetchum4@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas Onyetenyevwe Ugwemubwem Ossas"
    name_last = "Ketchum"
    
    #Should produce ValueError as the first name is greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)  


def test_auth_register_last_name_too_long():

    reset_data()
    
    email = "AshKetchum5@gmail.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "supercalifragilisticexpialidocious supercalifragilisticexpialidocious"
    
    #Should produce ValueError as the last name is greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)     


def test_auth_register_first_and_last_name_too_long():

    reset_data()
    
    email = "AshKetchum6@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas Onyetenyevwe Ugwemubwem Ossas"
    name_last = "supercalifragilisticexpialidocious supercalifragilisticexpialidocious"
    
    #Should produce ValueError as the first and last name are greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last) 

def test_auth_register_first_name_long_handler():

    reset_data()
    
    email = "AshKetchum6@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "UvuvwevwevweOsassz"
    name_last = "Super"
      
    user_details = auth_register(email, password, name_first, name_last)         
    
    token = user_details['token']
    #obtain handle             
    get_handle = get_user_details(token)
    handle_str = get_handle['handle_str']
            
    assert(check_valid_handle(handle_str) == True)  


def test_auth_register_last_name_long_handler():

    reset_data()
    
    email = "AshKetchum6@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Super"
    name_last = "UvuvwevwevweOsasszkilo"
      
    user_details = auth_register(email, password, name_first, name_last)         
               
    token = user_details['token']
    #obtain handle             
    get_handle = get_user_details(token)
    handle_str = get_handle['handle_str']
            
    assert(check_valid_handle(handle_str) == True)
    
def test_auth_register_first_and_last_name_long_handler():

    reset_data()
    
    email = "AshKetchum6@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Supercalifragilisticexpialidocious"
    name_last = "UvuvwevwevweOsassz"
      
    user_details = auth_register(email, password, name_first, name_last)         
    
    token = user_details['token']
    #obtain handle             
    get_handle = get_user_details(token)
    handle_str = get_handle['handle_str']
            
    assert(check_valid_handle(handle_str) == True)    

             
def test_auth_register_valid_token_generated():
   
    reset_data()
     
    email = "AshKetchum7@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    user_details = auth_register(email, password, name_first, name_last)
    
    user_token = user_details['token']
    
    assert(check_valid_token(user_token) == True)    
 
def test_auth_register_valid_u_id_generated():  
    
    reset_data()
    
    email = "AshKetchum8@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    user_details = auth_register(email, password, name_first, name_last)
    
    user_u_id = user_details['u_id']
    
    assert(check_valid_u_id(user_u_id) == True)       

def test_auth_register_invalid_u_id_generated():  
       
    #There are no negative   
    assert(check_valid_u_id(-1) == False)  
 
    
#################################################################################
##                    TESTING auth_passwordreset_request                       ##
#################################################################################        
      
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
 
        
#################################################################################
##                    TESTING auth_passwordreset_reset                         ##
#################################################################################                       
        
def test_auth_passwordreset_reset_correct_details(registered_user_1):

    #Registered user requests a reset code
    auth_passwordreset_request("PokemonMaster@gmail.com")

    reset_code = get_user_details(registered_user_1['token'])['reset_code']
    
    new_password = "ThisIsAV@lidNewPassword123"
    
    #Should produce no errors
    auth_passwordreset_reset(reset_code, new_password)    
    
        
def test_auth_passwordreset_reset_incorrect_reset_code(registered_user_1):

    #Registered user requests a reset code
    auth_passwordreset_request("PokemonMaster@gmail.com")
    
    reset_code = -1
    
    new_password = "ThisIsAV@lidNewPassword123"
    
    #Should produce a ValueError as an incorrect reset_code is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)  


def test_auth_passwordreset_reset_invalid_password(registered_user_1):

    #Registered user requests a reset code
    auth_passwordreset_request("PokemonMaster@gmail.com")

    reset_code = get_user_details(registered_user_1['token'])['reset_code']
    
    new_password = "password"
    
    #Should produce a ValueError as an invalid password is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)  


def test_auth_passwordreset_reset_invalid_password_and_reset_code(registered_user_1):
    
    #Registered user requests a reset code
    auth_passwordreset_request("PokemonMaster@gmail.com")
    
    reset_code = -1
    
    new_password = "password"
    
    #Should produce a ValueError as an reset code and invalid password is provided
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code, new_password)  
    
    
