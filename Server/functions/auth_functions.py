import re 
import smtplib
import ssl
from helper_functions import *
    
def auth_login(email, password):

    #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid Email")        
   
    #Checking if email provided is registered
    if email not in list_of_users:
        raise ValueError("Email Not Registered")           
    
    #Checking if password matches email
    if list_of_users[email]["password"] != password:
        raise ValueError("Incorrect Password Entered")
    
    #Check if user is already logged in:
    if list_of_users[email]["token"] not in list_of_valid_tokens:              
        #Generate new valid token for user
        list_of_users[email]["token"] = generate_token()
        print("User has logged in")
    else:
        print("User already logged in elsewhere")
        
    
    return {list_of_users[email]["u_id"], list_of_users[email]["token"]}
    
def auth_logout(token):
    
    if token in list_of_valid_tokens:
        list_of_valid_tokens.remove(token)
    else:
        print("Token already invalid")
    
def auth_register(email, password, name_first, name_last):

    #FIRST CHECK IF ALL THE PASSED IN PARAMETERS ARE VALID
           
    #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid Email")
            
    #Checking if valid password
    if not valid_password(password):
        raise ValueError("Invalid Password")
   
    #Check if for valid first and last names
    if (len(name_first) < 1):
        raise ValueError("Invalid First Name")
        
    if (len(name_last) < 1):
        raise ValueError("Invalid Last Name")
    
    print("VALIDDD")
    
    #Check if user is in list_of_users
    
    if email in list_of_users:
        raise ValueError("Email Provided Already in Use")
    
    #If not then add the user to list_of_users
    
    list_of_users[email] = {"password": password, "u_id": generate_u_id(), "token" : generate_token(),
                            "reset_code": None}
    print("USER ADDED")
 
    return {list_of_users[email]["u_id"], list_of_users[email]["token"]}
    
def auth_passwordreset_request(reset_email):

    reset_code = generate_reset_code()
    list_of_users[reset_email]['reset_code'] = reset_code
    
    message = "Reset Code " + str(reset_code)
    

    print("Starting to send")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("teamhdslackr@gmail.com", "V@lidPassword123")
        server.sendmail("teamhdslackr@gmail.com", reset_email, message)
        
    print("Email Sent")     
    
def auth_passwordreset_reset(reset_code, new_password):

    #Check if reset code belongs to any user. If not it is invalid
    
    for user in list_of_users: 
        if list_of_users[user]['reset_code'] == None:
            continue
    
        if list_of_users[user]['reset_code'] == reset_code:
            if valid_password(new_password):
                list_of_users[user]['reset_code'] = None
                list_of_users[user]['password'] = new_password
                return
            else:
                raise ValueError("Invalid Password")
            
    
    raise ValueError("Invalid Reset Code")
       
auth_register("shoandesai@gmail.com", "V@lidPassword123", "Shoan", "Desai")      
auth_register("santaIsRipped@gmail.com", "V@lidPassword123", "Santa", "Claus")    
auth_login("santaIsRipped@gmail.com", "V@lidPassword123")    
auth_logout(12345) 
auth_passwordreset_request("shoandesai@gmail.com")
