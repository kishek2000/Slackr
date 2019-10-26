import re 
import smtplib
import ssl
import sys
sys.path.append('/Server/functions')
from functions.helper_functions import *
import pytest
    
def auth_login(email, password):
    
    #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid Email")  
    
            
    #Assign token to user if they are not logged in:
    
    for user in list_of_users:
        if user["email"] == email:
            
            #Checking if password matches email
            if not email_matches_password(email, password):
                raise ValueError("Incorrect Password Entered")
            
            #Otherwise
            user["token"] = generate_token(email)
            return {'u_id': user["u_id"], 'token': user["token"]}
    
    #If loop finishes then the email is not registered
    raise ValueError("Email Not Registered") 
    
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
                          "name_first": name_first, "name_last": name_last, 'app_permission_id': None})
    
    #Assign token and u_id
    
    list_of_users[-1]["token"] = generate_token(email)
    list_of_users[-1]["u_id"] = generate_u_id()
    
    if list_of_users[-1]['u_id'] == 1:
        list_of_users[-1]["app_permission_id"] = 1
    else:
        list_of_users[-1]["app_permission_id"] = 3

    
    return {'u_id' : list_of_users[-1]["u_id"], 'token': list_of_users[-1]["token"]}
    
def auth_passwordreset_request(reset_email):

    #Checking for valid email
    if not valid_email(reset_email):
        raise ValueError("Invalid Email") 

    
    reset_code = generate_reset_code()
    
    for user in list_of_users:
        if user["email"] == reset_email:
            user["reset_code"] = reset_code
    
            message = "Reset Code " + reset_code
    
            print("Starting to send Email")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login("teamhdslackr@gmail.com", "V@lidPassword123")
                server.sendmail("teamhdslackr@gmail.com", reset_email, message)
                
            print("Email Sent")   
            
            return
            
    #If the loop completes then no valid emeail was found
    
    raise ValueError("Email Not Registered") 
    
def auth_passwordreset_reset(reset_code, new_password):

    #Check if reset code belongs to any user. If not it is invalid
    
    for user in list_of_users: 
       
        if user['reset_code'] == reset_code and valid_password(new_password):
            user['reset_code'] = None
            user['password'] = new_password
            return
        # else:
        #     raise ValueError("Invalid Password")
    raise ValueError("Invalid Reset Code")

      
