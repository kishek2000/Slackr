import re 
import random
import hashlib
import datetime

#Dictionary with key as email as the corresponding values e.g.
## Shoan version for Auth
#  list_of_users = [{'rajeshkumar@gmail.com':{'password': 'V@lidPassword123', 'u_id': 1, 'token' : 12345, 'reset_code': None}}]

## Adi new version for more general use:
list_of_users = [{'handle_str': '@Rajesh', 'email': 'rajeshkumar@gmail.com', 'password': 'V@lidPassword123', 'u_id': 1, 'token' : 12345, 'reset_code': None, 'name_first': 'Rajesh', 'name_last': 'Kumar', 'permission_id': 1}]

## Addition of a permissions list:
'''
    Note: for permission ids, we are saying that 1 is owner, 2 is admin and 3 is member.
    1 and 2 have same permissions but 2 cannot change the privileges that 1 has. 
    First member that is added to Slackr has owner permission. Only other owners could then
    change this. 
'''

#list_of_user_permissions = [{'u_id': 1, }] 

global number_of_users 
number_of_users = 1

#===============================================================================#
#=============================== GENERAL HELPERS ===============================#
#===============================================================================#
def get_user_details(token):
    for user in list_of_users:
        if user['token'] == token:
            return {'u_id': user['u_id'], 'token': token, 'name_first': user['name_first'], 'name_last': user['name_last'], 'handle_str': user['handle_str'], 'email': user['email']}
    return {}

def generate_token(email):   
    for user in list_of_users:
        if user['email'] == email:
            hashed_token = hashlib.sha256(email.encode()).hexdigest()
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
    if token == -1:
        return False
    for user in list_of_users:
        if token == user['token']:
            return True
    return False 

def check_token_matches_user(u_id, token):
    if token == -1:
        return False
    for user in list_of_users:
        if u_id == user['u_id']:
            if token == user['token']:
                return True
    return False

def get_user_from_token(token):
    for user in list_of_users:
        if token == user['token']:
            return user['u_id']

def get_token_from_user(u_id):
    for user in list_of_users:
        if u_id == user['u_id']:
            return user['token']

def get_user_permission(u_id):
    for user in list_of_users:
        if u_id == user['u_id']:
            return user['permission_id']

def email_registered(email):

    for user in list_of_users:
        if email == user['email']:
            return True
    
    return False

def email_matches_password(registered_email, password):

    for user in list_of_users:
        if registered_email == user['email'] and password == user['password']:
            return True 
    
    return False

def reset_data():
    global number_of_users 

    list_of_users.clear()
    number_of_users = 0

def get_name_from_token(token):
    for user in list_of_users:
        if token == user['token']:
            return {'name_first': user['name_first'], 'name_last': user['name_last']}

def check_valid_handle(handle_str):
    for user in list_of_users:
        if handle_str == user['handle_str']:
            return True
    return False 
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
    return reset_code
  
  
def get_reset_code_from_user(email):
    for user in list_of_users:
        if email == user['email']:
            return user['reset_code']    
    
#===============================================================================#
#=============================== CHANNEL HELPERS ===============================#
#===============================================================================#

#================= data storage for channels =================#
all_channels_details = [{'channel_id': 1, 'name': 'Channel A', 'owner_members':[{'u_id': 1, 'name_first': 'Rajesh', 'name_last': 'Kumar'}], 'all_members':[{'u_id': 1, 'name_first': 'Rajesh', 'name_last': 'Kumar'}], 'isPublic': True}]
all_channels_messages = [{'channel_id': 1, 'total_messages': 55, 'messages':[{'message_id': 1, 'u_id': 1, 'message': 'Hello', 'time_created': datetime.datetime(2019,10,15,19,30), 'reacts': [{'react_id': 1, 'u_ids': [1], 'is_this_user_reacted': False}], 'is_pinned': False}]}]

global number_of_channels
number_of_channels = 1

def reset_channel_data():
    global number_of_channels
    number_of_channels = 0
    number_of_messages = 0
    all_channels_details.clear()
    all_channels_messages.clear()

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
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if check_token_matches_user(users['u_id'], token) == True:
                    return True
            break
    return False

def check_user_in_channel(u_id, channel_id):
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
               #print("MORE DEBUG ====== checktokeninchannel HELPER ========")
               #print(users)
                if users['u_id'] == u_id:
                    return True
            break
    return False

def get_total_channel_messages(channel_id):
    for channels in all_channels_messages:
        if channel_id == channels['channel_id']:
            return channels['total_messages']

def get_channel_id_from_name(name):
    for channels in all_channels_details:
        if channels['name'] == name:
            return channels['channel_id']

#===============================================================================#
#=============================== MESSAGE HELPERS ===============================#
#===============================================================================#
# Helper Functions to write: find_message_info, has_user_reacted
global number_of_messages
number_of_messages = 1

# Return None if message does not exist
def find_message_info(message_id):
    if number_of_messages == 0:
        return None
    for channel in all_channel_messages:
        for message in channel["messages"]:
            if message["message_id"] == message_id:
                return {"channel_id": channel["channel_id"], "message": message}
    return None
    
def has_user_reacted(uid, react_id, message):
    for react in message["reacts"]:
        if react_id == react["react_id"]:
            if uid in react["u_ids"]:
                return True
            else:
                return False
            
def generate_message_id():
    global number_of_messages
    number_of_messages += 1
    return number_of_messages
#===============================================================================#
#============================= PERMISSIONS HELPERS =============================#
#===============================================================================#
def change_user_permission(u_id, permission_id):
    for user in list_of_users:
        if u_id == user['u_id']:
            user['permission_id'] = permission_id
            break
