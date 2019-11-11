'''
File contains auth related functions
'''
#import re
import smtplib
#import ssl
#import sys
#import hashlib
from functions.helper_functions import (valid_email, email_matches_password, valid_password,
                                        email_registered, generate_reset_code, list_of_users,
                                        password_hash, generate_token, generate_u_id)


def auth_login(email, password):
    '''Funtion logs a registered user onto slackr'''
    #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid Email")

    #Assign token to user if they are not logged in:

    for user in list_of_users:
        if user["email"] == email:

            #Checking if password matches email
            if not email_matches_password(email, password_hash(password)):
                raise ValueError("Incorrect Password Entered")

            #Otherwise
            user["token"] = generate_token(email)
            return {'u_id': user["u_id"], 'token': user["token"]}

    #If loop finishes then the email is not registered
    raise ValueError("Email Not Registered")

def auth_logout(token):
    '''Funtion logs out a registered user from slackr'''
    for user in list_of_users:
        if user["token"] == token:
            user["token"] = None
            return True

    return False

def auth_register(email, password, name_first, name_last):
    '''Funtion registers a user onto slackr'''
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
            handle = name_first[0] + name_last

        elif len(name_last) > 20 and len(name_first) < 20:
            handle = name_first + name_last[0]

        else:
            handle = name_first[0:2] + name_last[0:2]

    else:
        handle = name_first + name_last


    list_of_users.append({"handle_str": handle, "email" : email,
                          "password": password_hash(password), "u_id": None,
                          "token" : None, "reset_code": None, "name_first": name_first,
                          "name_last": name_last,
                          'app_permission_id': None, 'image_path': None})

    #Assign token and u_id

    list_of_users[-1]["token"] = generate_token(email)
    list_of_users[-1]["u_id"] = generate_u_id()

    if list_of_users[-1]['u_id'] == 1:
        list_of_users[-1]["app_permission_id"] = 1
    else:
        list_of_users[-1]["app_permission_id"] = 3


    return {'u_id' : list_of_users[-1]["u_id"], 'token': list_of_users[-1]["token"]}

def auth_passwordreset_request(reset_email):
    '''Funtion requests a reset code for a password reset'''
    #Method for sending email obtained from https://www.youtube.com/watch?v=JRCJ6RtE3xU

    #Checking for valid email
    if not valid_email(reset_email):
        raise ValueError("Invalid Email")


    reset_code = generate_reset_code()

    for user in list_of_users:
        if user["email"] == reset_email:

            user["reset_code"] = reset_code

            subject = "No Reply: Forgot Password Request"

            body = f"Hi {user['name_first']},\n\nYou recently requested that " \
            "you forgot your password. Here is your reset code!\n\n" + reset_code

            message = f'Subject: {subject}\n\n{body}'

            print("Starting to send Email")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login("teamhdslackr@gmail.com", "V@lidPassword123")
                server.sendmail("teamhdslackr@gmail.com", reset_email, message)

            print("Email Sent")

            return

    #If the loop completes then no valid emeail was found

    raise ValueError("Email Not Registered")

def auth_passwordreset_reset(reset_code, new_password):
    '''Funtion allows a user to reset their password provided the correct reset code'''
    #Check if reset code belongs to any user. If not it is invalid

    for user in list_of_users:

        if user['reset_code'] == reset_code and valid_password(new_password):
            user['reset_code'] = None
            user['password'] = password_hash(new_password)
            return

    raise ValueError("Invalid Reset Code")
