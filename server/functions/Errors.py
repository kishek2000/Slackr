from functions.helper_functions import valid_email, email_matches_password, valid_password
from functions.helper_functions import email_registered, password_hash, check_valid_channel_id
from functions.helper_functions import check_token_in_channel, add_to_standup_queue
from functions.helper_functions import all_channels_messages, check_valid_u_id, check_valid_token
from werkzeug.exceptions import HTTPException


#===============================================================================#
#=============================== ERRORS DEF ====================================#
#===============================================================================#
## For actual messages to print in the frontend, we define our classes here
## and then import these everywhere.
class AccessError(HTTPException):
    code = 400
    message = "no message specified"

class ValueError(HTTPException):
    code = 400
    message = "no message specified"

#===============================================================================#
#=============================== COMMON DECORATORS =============================#
#===============================================================================#
def authorise_token(function):
    ''' Decorator for authorising just token '''
    def wrapper(**kwargs):
        if kwargs['token'] and not check_valid_token(kwargs['token']):
            raise AccessError("Given token is invalid")
        return function(**kwargs)
    return wrapper


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
            raise ValueError("Email Is Already Registered")
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

def authorise_channel_id(function):
    ''' Decorator for authorising channel id '''
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if check_valid_channel_id(user_details['channel_id']) is False:
            raise ValueError("Invalid Channel")
        return function(*args, **kwargs)
    return wrapper

def token_in_channel(function):
    ''' Decorator for authorising token is in channel '''
    def wrapper(*args, **kwargs):
        user_details = kwargs
        if check_token_in_channel(user_details['token'], user_details['channel_id']) is False:
            raise AccessError("Accessing user is not in this channel")
        return function(*args, **kwargs)
    return wrapper

def authorise_u_id(function):
    ''' Decorator for authorising uid '''
    def wrapper(**kwargs):
        if kwargs['u_id'] and not check_valid_u_id(kwargs['u_id']):
            raise ValueError("Given user id does not exist.")
        return function(**kwargs)
    return wrapper





