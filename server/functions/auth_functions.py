'''
File contains auth related functions
'''
import smtplib
import hashlib
from functions.helper_functions import (valid_email, email_matches_password, valid_password,
                                        email_registered, generate_reset_code, list_of_users,
                                        password_hash, generate_token, generate_u_id, 
                                        authorise_login, authorise_register, generate_handle,
                                        authorise_passwordreset_request)

@authorise_login
def auth_login(email=None, password=None, **kwargs):
    '''Funtion logs a registered user onto slackr'''

    #Assign token to user if they are not logged in:

    for user in list_of_users:
        if user["email"] == email:

            #Otherwise
            user["token"] = generate_token(email)
            return {'u_id': user["u_id"], 'token': user["token"]}
          

def auth_logout(token=None):
    '''Funtion logs out a registered user from slackr'''
    for user in list_of_users:
        if user["token"] == token:
            user["token"] = None
            return True

    return False

@authorise_register
def auth_register(email=None, password=None, name_first=None, name_last=None, **kwargs):
    '''Funtion registers a user onto slackr'''
    
    handle = generate_handle(name_first, name_last)
    
    if len(list_of_users) == 0:
    
        default_app_permission_id = 1
    else:
    
        default_app_permission_id = 3
    
    #Add user
    list_of_users.append({"handle_str": handle, "email" : email,
                          "password": password_hash(password), "u_id": generate_u_id(),
                          "token" : hashlib.sha256(email.encode()).hexdigest(),
                          "reset_code": None, "name_first": name_first,
                          "name_last": name_last,
                          'app_permission_id': default_app_permission_id, 'profile_img_url': None})


    return {'u_id' : list_of_users[-1]["u_id"], 'token': list_of_users[-1]["token"]}

@authorise_passwordreset_request
def auth_passwordreset_request(reset_email=None, **kwargs):
    '''Funtion requests a reset code for a password reset'''
    #Method for sending email obtained from https://www.youtube.com/watch?v=JRCJ6RtE3x
    reset_code = generate_reset_code()

    for user in list_of_users:
        if user["email"] == reset_email:

            user["reset_code"] = reset_code

            subject = "No Reply: Forgot Password Request"

            body = f"Hi {user['name_first']},\n\nYou recently requested that " \
            "you forgot your password. Here is your reset code!\n\n" + reset_code

            message = f'Subject: {subject}\n\n{body}'

            print("Starting to send Email...")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login("teamhdslackr@gmail.com", "V@lidPassword123")
                server.sendmail("teamhdslackr@gmail.com", reset_email, message)

            print("Email Sent")

            return

def auth_passwordreset_reset(reset_code=None, new_password=None):
    '''Funtion allows a user to reset their password provided the correct reset code'''
    #Check if reset code belongs to any user. If not it is invalid

    for user in list_of_users:

        if user['reset_code'] == reset_code and valid_password(new_password):
            user['reset_code'] = None
            user['password'] = password_hash(new_password)
            return

    raise ValueError("Invalid Reset Code")
