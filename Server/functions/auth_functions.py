import re 
import smtplib
import ssl
from .helper_functions import *
import pytest
    
def auth_login(email, password):

    #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid Email")        
   
    #Checking if email provided is registered
    if not email_registered(email):
        raise ValueError("Email Not Registered")           
    
    #Checking if password matches email
    if not email_matches_password(email, password):
        raise ValueError("Incorrect Password Entered")
    
    #Assign token to user if they are not logged in:
    
    for user in list_of_users:
        if user["email"] == email:
            user["token"] = generate_token(email)
            return {'u_id': user["u_id"], 'token': user["token"]}
    
def auth_logout(token):
    
    for user in list_of_users:
        if user["token"] == token:
            user["token"] = None
            return True
    
    return False
            
def auth_register(email, password, name_first, name_last):

    #FIRST CHECK IF ALL THE PASSED IN PARAMETERS ARE VALID
           
    #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid Email")
            
    #Checking if valid password
    if not valid_password(password):
        raise ValueError("Invalid Password")
   
    #Check if for valid first and last names
    if (len(name_first) < 1 or len(name_first) > 50):
        raise ValueError("Invalid First Name")
        
    if (len(name_last) < 1 or len(name_last) > 50):
        raise ValueError("Invalid Last Name")
    
    #print("VALIDDD")
    
    #Check if user is in list_of_users
    
    if email_registered(email):
        raise ValueError("Email Provided Already in Use")
    
    #If not then add the user to list_of_users
    if len(name_first + name_last) > 20:
        if len(name_first) > 20 and len(name_last) < 20:
            handle  = name_first[0] + name_last
        elif len(name_last) > 20 and len(name_first) < 20:
            handle = name_first + name_last[0]
        else:
            handle = name_first[0:2] + name_last[0:2]
    else:
        handle = name_first + name_last
    
    
    list_of_users.append({"handle_str": handle, "email" : email, "password": password, "u_id": None,
                          "token" : None, "reset_code": None , 
                          "name_first": name_first, "name_last": name_last, 'permission_id': None})
    
    #Assign token and u_id
    for user in list_of_users:
        if user["email"] == email:
            user["token"] = generate_token(email)
            user["u_id"] = generate_u_id()
            
            #Assign default permission_id
            if user['u_id'] == 1:
                user["permission_id"] = 1
            else:
                user["permission_id"] = 3
            break        
    return {'u_id' : user["u_id"], 'token': user["token"]}
    
def auth_passwordreset_request(reset_email):

    #Checking for valid email
    if not valid_email(reset_email):
        raise ValueError("Invalid Email") 

    #Checking if email provided is registered
    if not email_registered(reset_email):
        raise ValueError("Email Not Registered") 

    reset_code = generate_reset_code()
    
    for user in list_of_users:
        if user["email"] == reset_email:
            user["reset_code"] = reset_code
    
    message = "Reset Code " + reset_code
    

    print("Starting to send")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("teamhdslackr@gmail.com", "V@lidPassword123")
        server.sendmail("teamhdslackr@gmail.com", reset_email, message)
        
    print("Email Sent")   
    # reset_code_timer(reset_email)  
    
def auth_passwordreset_reset(reset_code, new_password):

    #Check if reset code belongs to any user. If not it is invalid
    
    for user in list_of_users: 
        if user['reset_code'] == None:
            continue
    
        if user['reset_code'] == reset_code and valid_password(new_password):
            user['reset_code'] = None
            user['password'] = new_password
            return
        # else:
        #     raise ValueError("Invalid Password")
    raise ValueError("Invalid Reset Code")

      
#auth_login("rajeshkumar@gmail.com", "V@lidPassword123") 
#auth_register("shoandesai@gmail.com", "V@lidPassword123", "Shoan", "Desai")      
#auth_register("santaIsRipped@gmail.com", "V@lidPassword123", "Santa", "Claus")    
#auth_login("santaIsRipped@gmail.com", "V@lidPassword123")   
#auth_logout(generate_token("santaIsRipped@gmail.com")) 
#auth_passwordreset_request("shoandesai@gmail.com")
 
# def reset_code_timer(reset_email):
#     sleep(24*60*60)
#     for user in list_of_users:
#         if user['email'] == reset_email:
#             if user['reset_code'] != None:
#                 user['reset_code'] == None

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

    email = "AshKetchum1@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    auth_register(email, password, name_first, name_last)
    
    
def test_auth_register_invalid_email():

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

    email = "AshKetchum3@yahoo.com"
    password = "ILoveGary"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce ValueError as invalid password has been provided
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)  

def test_auth_register_first_name_too_long():

    email = "AshKetchum4@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas Onyetenyevwe Ugwemubwem Ossas"
    name_last = "Ketchum"
    
    #Should produce ValueError as the first name is greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)  


def test_auth_register_last_name_too_long():

    email = "AshKetchum5@yaheecom"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "supercalifragilisticexpialidocious supercalifragilisticexpialidocious"
    
    #Should produce ValueError as the last name is greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last)     


def test_auth_register_first_and_last_name_too_long():

    email = "AshKetchum6@yaheecom"
    password = "IWann@BeTheVeryBest123"
    name_first = "Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas Onyetenyevwe Ugwemubwem Ossas"
    name_last = "supercalifragilisticexpialidocious supercalifragilisticexpialidocious"
    
    #Should produce ValueError as the first and last name are greater than 50 characters
    with pytest.raises(ValueError):
        auth_register(email, password, name_first, name_last) 
        
             
def test_auth_register_valid_token_generated():
    
    email = "AshKetchum7@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    user_details = auth_register(email, password, name_first, name_last)
    
    user_token = user_details['token']
    
    assert(check_valid_token(user_token) == True)    
 
def test_auth_register_valid_u_id_generated():  
    
    email = "AshKetchum8@yahoo.com"
    password = "IWann@BeTheVeryBest123"
    name_first = "Ash"
    name_last = "Ketchum"
    
    #Should produce no errors
    user_details = auth_register(email, password, name_first, name_last)
    
    user_u_id = user_details['u_id']
    
    assert(check_valid_u_id(user_u_id) == True)       

    
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

    reset_code = get_reset_code_from_user("PokemonMaster@gmail.com")
    
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

    reset_code = get_reset_code_from_user("PokemonMaster@gmail.com")
    
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
    
    
