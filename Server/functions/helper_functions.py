import re 
import random
import hashlib
import datetime

#Dictionary with key as email as the corresponding values e.g.
## Shoan version for Auth
#  list_of_users = [{'rajeshkumar@gmail.com':{'password': 'V@lidPassword123', 'u_id': 1, 'token' : 12345, 'reset_code': None}}]

## Adi new version for more general use:
list_of_users = [{'email': 'rajeshkumar@gmail.com', 'password': 'V@lidPassword123', 'u_id': 1, 'token' : 12345, 'reset_code': None, 'name_first': 'Rajesh', 'name_last': 'Kumar'}]

## Addition of a permissions list:
'''
    Note: for permission ids, we are saying that 1 is owner, 2 is admin and 3 is member.
    1 and 2 have same permissions but 2 cannot change the privileges that 1 has. 
    First member that is added to Slackr has owner permission. Only other owners could then
    change this. 
'''
list_of_user_permissions = [{'u_id': 1, 'permission_id': 1}] 


list_of_valid_tokens = [12345]

global number_of_users 
number_of_users = 1

#===============================================================================#
#=============================== GENERAL HELPERS ===============================#
#===============================================================================#
def get_user_details(u_id):
    for user in list_of_users:
        if user['u_id'] == u_id:
            return {'u_id': u_id, 'name_first': user['name_first'], 'name_last': user['name_last']}
        else:
            return {}

def generate_token(username):   
    for user in list_of_users:
        if user['username'] == username:
            hashed_token = hashlib.sha256(username.encode()).hexdigest()
            user['token'] = hashed_token
    return hashed_token                    

def generate_u_id():
    global number_of_users
    number_of_users += 1
    return number_of_users

def check_valid_u_id(u_id):
    for user in list_of_users:
        if u_id == user['u_id']:
            return True
    return False

def check_valid_token(token):
    for user in list_of_users:
        if token == user['token']:
            return True
    return False 

def check_token_matches_user(u_id, token):
    for user in list_of_users:
        if u_id == user['u_id']:
            if token == user['token']:
                return True
    return False

def get_user_from_token(token):
    for user in list_of_users:
        if token == user['token']:
            return user['u_id']

def get_user_permission(u_id):
    for user in list_of_user_permissions:
        if u_id == user['u_id']:
            return user['permission_id']

def email_registered(email):

    for user in list_of_users:
        if email == user['email']:
            return True
    
    return False

## def reset_data():

#===============================================================================#
#================================= AUTH HELPERS ================================#
#===============================================================================#

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
    
    
#===============================================================================#
#=============================== CHANNEL HELPERS ===============================#
#===============================================================================#

#================= data storage for channels =================#
all_channels_details = [{'channel_id': 1, 'name': 'Channel A', 'owner_members':[{'u_id': 1, 'name_first': 'Rajesh', 'name_last': 'Kumar'}], 'all_members':[{'u_id': 1, 'name_first': 'Rajesh', 'name_last': 'Kumar'}], 'isPublic': True}]
#all_channels_messages = [{'channel_id': 1, 'total_messages': 55, 'messages':[{'message_id': 1, 'u_id': 1, 'message': 'Hello', 'time_created': datetime(2019,10,15,19,30), 'is_unread': False, 'reacts': [{'react_id': 1, 'u_ids': [1], 'is_this_user_reacted': False}], 'is_pinned': False}]}]

global number_of_channels
number_of_channels = 1

def check_valid_channel_id(channel_id):
    for channel in all_channels_details:
        if channel_id == channel['channel_id']:
            return True
    return False

def generate_channel_id():
    global number_of_channels
    number_of_channels += 1
    return number_of_channels

def check_token_in_channel(token, channel_id):
    authorised_user_in_channel = False    
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if check_token_matches_user(users['u_id'], token) == True:
                    authorised_user_in_channel = True
    return authorised_user_in_channel
                

