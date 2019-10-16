import re 
import smtplib
import ssl
from helper_functions import *
    
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
            return {user["u_id"], user["token"]}
    
def auth_logout(token):
    
    for user in list_of_users:
        if user["token"] == token:
            user["token"] = None
    
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
    
    print("VALIDDD")
    
    #Check if user is in list_of_users
    
    if email_registered(email):
        raise ValueError("Email Provided Already in Use")
    
    #If not then add the user to list_of_users
    
    list_of_users.append({"email" : email, "password": password, "u_id": generate_u_id(),
                          "token" : None, "reset_code": None , 
                          "name_first": name_first, "name_last": name_last})
                          
    #Assign token
    list_of_users[-1]["token"] = generate_token(email)
                          
    print("USER ADDED")
 
    return {list_of_users[-1]["u_id"], list_of_users[-1]["token"]}
    
def auth_passwordreset_request(reset_email):

    reset_code = generate_reset_code()
    
    for user in list_of_users:
        if user["email"] == reset_email:
            user["reset_code"] = reset_code
    
    message = "Reset Code " + str(reset_code)
    

    print("Starting to send")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("teamhdslackr@gmail.com", "V@lidPassword123")
        server.sendmail("teamhdslackr@gmail.com", reset_email, message)
        
    print("Email Sent")     
    
def auth_passwordreset_reset(reset_code, new_password):

    #Check if reset code belongs to any user. If not it is invalid
    
    for user in list_of_users: 
        if user['reset_code'] == None:
            continue
    
        if user['reset_code'] == reset_code and valid_password(new_password):
            
            user['reset_code'] = None
            user['password'] = new_password
            return
        else:
            raise ValueError("Invalid Password")
            
    
    raise ValueError("Invalid Reset Code")
       
auth_login("rajeshkumar@gmail.com", "V@lidPassword123") 
auth_register("shoandesai@gmail.com", "V@lidPassword123", "Shoan", "Desai")      
auth_register("santaIsRipped@gmail.com", "V@lidPassword123", "Santa", "Claus")    
auth_login("santaIsRipped@gmail.com", "V@lidPassword123")   
auth_logout(generate_token("santaIsRipped@gmail.com")) 
auth_passwordreset_request("shoandesai@gmail.com")
