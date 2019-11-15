from functions.helper_functions import (valid_email, email_matches_password, valid_password,
                                        email_registered, password_hash, check_valid_channel_id,            
                                        check_token_in_channel, add_to_standup_queue, 
                                        all_channels_messages)

#===============================================================================#
#=============================== ACCESSERROR DEF ===============================#
#===============================================================================#
class AccessError(Exception):
    ## We raise this in general when things aren't accessed correctly!!
    pass
    
#===============================================================================#
#=============================== AUTH DECORATORS ===============================#
#===============================================================================#

def check_name_validity(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if (len(user_details['name_first']) < 1 or len(user_details['name_first']) > 50):
            raise ValueError("Invalid First Name")
        if (len(user_details['name_last']) < 1 or len(user_details['name_last']) > 50):
            raise ValueError("Invalid Last Name")
        return function(*args, **kwargs)
    return wrapper


def check_valid_password(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if valid_password(user_details['password']) is False:
            raise ValueError("Invalid Password Entered")
        return function(*args, **kwargs)
    return wrapper

def check_email_registered_false(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if email_registered(user_details['email']) == False:
            raise ValueError("Email Not Registered")
        return function(*args, **kwargs)
    return wrapper

def check_email_registered_true(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if email_registered(user_details['email']) == True:
            raise ValueError("Email Not Registered")
        return function(*args, **kwargs)
    return wrapper

def check_valid_email(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if valid_email(user_details['email']) == False:
            raise ValueError("Invalid Email")
        return function(*args, **kwargs)
    return wrapper

def check_password_email_match(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if email_matches_password(user_details['email'], password_hash(user_details['password'])) == False:
            raise ValueError("Incorrect Password Entered")
        return function(*args, **kwargs)
    return wrapper
    
#===============================================================================#
#============================= CHANNEL DECORATORS ==============================#
#===============================================================================#

def valid_channel_id(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if check_valid_channel_id(user_details['channel_id']) is False:
            raise ValueError("Invalid Channel")
        return function(*args, **kwargs)
    return wrapper
    
def token_in_channel(function):
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if check_token_in_channel(user_details['token'], user_details['channel_id']) is False:
            raise AccessError("User Not In Channel")
        return function(*args, **kwargs)
    return wrapper   


