import re 
import random

#Dictionary with key as email as the corrosponding values e.g.
list_of_users = {"rajeshkumar@gmail.com" : {"password": "V@lidPassword123", "u_id": 1, "token" : 12345, 
                 "reset_code": None}} 
                 
list_of_valid_tokens = [12345]


global number_of_users 
number_of_users = 1

#===============================================================================#
#=============================== GENERAL HELPERS ===============================#
#===============================================================================#

def generate_token():
     
    token = random.randint(1,10000000)   
    list_of_valid_tokens.append(token)
    
    return token                    

def generate_u_id():
    global number_of_users
    number_of_users += 1
    return number_of_users


######## AUTH FUNCTION HELPERS ##########

def valid_email(email):

    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' 
    
    if re.search(regex,email) is None:
        return False
    else:
        return True
        
def valid_password(password):
    
    no_of_characters = 0
    no_of_numbers = 0
    no_of_upper_case = 0
    no_of_lower_case = 0
    no_of_special_characters = 0
    
    for character in password:
    
        no_of_characters += 1
    
        if character.isupper():
            no_of_upper_case += 1
            
        if character.islower():
            no_of_lower_case += 1   
    
        if character.isdigit():
            no_of_numbers += 1
        
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
       
        if regex.search(character) is not None: 
            no_of_special_characters += 1
            
            
    if (no_of_characters >= 1 and no_of_numbers >= 1 and
        no_of_upper_case >= 1 and no_of_lower_case >= 1 and
        no_of_special_characters >= 1 and len(password) >= 6):
        
        return True
        
    else:
        return False  
    
def generate_reset_code():
    reset_code = random.randint(1,10000000)   
    list_of_active_reset_codes.append(reset_code)
    return reset_code
    
    
