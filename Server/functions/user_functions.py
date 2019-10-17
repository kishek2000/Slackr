from helper_functions import *

###Custom helpers###
def get_user_details(token):
    for user in list_of_users:
        if user['token'] == token:
            return {'email': user['email'], 'name_first': user['name_first'], 'name_last': user['name_last'], 'handle_str': user['handle_str']}
        else:
            return {}
####################    
    

def user_profile(token, u_id):
    
    #Checking for valid u_id
    if not check_valid_u_id(u_id):
        raise ValueError("Invalid u_id")
        
    return get_user_details(token)


def user_profile_setname(token, name_first, name_last):

    #Checking for valid name_first
    if len(name_first) > 50 or len(name_first) < 1:
        raise ValueError("Invalid name_first")
   
   #Checking for valid name_first
    if len(name_last) > 50 or len(name_last) < 1:
        raise ValueError("Invalid name_last")
    
    for user in list_of_users:
        if user['token'] == token:
            user['name_first'] = name_first
            user['name_last'] = name_last
    
    
def user_profile_setemail(token, email):
    
     #Checking for valid name_first
    if not valid_email(email):
        raise ValueError("Invalid email")
    
    for user in list_of_users:
        if user['token'] == token:
            user['email'] = email
    
    
def user_profile_sethandle(token, handle_str):
