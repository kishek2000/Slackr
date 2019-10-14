import re 
from helper_functions import *
    
    
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
    
    list_of_users[email] = {"password": password, "u_id": generate_u_id(), "token" : generate_token()}
    print("USER ADDED")
 
    return {list_of_users[email]["u_id"], list_of_users[email]["token"]}
    
       
auth_register("shoandesai@gmail.com", "V@lidPassword123", "Shoan", "Desai")      
auth_register("santaIsRipped@gmail.com", "V@lidPassword123", "Santa", "Claus")    
  
       
