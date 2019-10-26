import re 
import random
import hashlib
import datetime
import sys
import atexit
import pickle

#Dictionary with key as email as the corresponding values e.g.
## Shoan version for Auth
#  list_of_users = [{'rajeshkumar@gmail.com':{'password': 'V@lidPassword123', 'u_id': 1, 'token' : 12345, 'reset_code': None}}]

## Adi new version for more general use:


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
#============================== PICKLING HELPERS ===============================#
#===============================================================================#
global number_of_channels
global number_of_messages
def pickle_data(all_channels_details, all_channels_messages, all_channels_permissions, list_of_users, number_of_channels, number_of_messages):
    pickle.dump(all_channels_details, open('Server/functions/data/all_channels_details.p', 'wb'))
    pickle.dump(all_channels_messages, open('Server/functions/data/all_channels_messages.p', 'wb'))
    pickle.dump(all_channels_permissions, open('Server/functions/data/all_channels_permissions.p', 'wb'))
    pickle.dump(list_of_users, open('Server/functions/data/list_of_users.p', 'wb'))
    pickle.dump(number_of_channels, open('Server/functions/data/number_of_channels.p', 'wb'))
    pickle.dump(number_of_messages, open('Server/functions/data/number_of_messages.p', 'wb'))


all_channels_details = pickle.load(open("Server/functions/data/all_channels_details.p", "rb"))
all_channels_messages = pickle.load(open("Server/functions/data/all_channels_messages.p", "rb"))
all_channels_permissions = pickle.load(open("Server/functions/data/all_channels_permissions.p", "rb"))
list_of_users = pickle.load(open("Server/functions/data/list_of_users.p", "rb"))
number_of_channels = pickle.load(open("Server/functions/data/number_of_channels.p", "rb"))
number_of_messages = pickle.load(open("Server/functions/data/number_of_messages.p", "rb"))
'''
#================= data storage for channels =================#
all_channels_details = [{'channel_id': 1, 'name': 'Channel A', 'owner_members':[{'u_id': 1, 'name_first': 'Rajesh', 'name_last': 'Kumar'}], 'all_members':[{'u_id': 1, 'name_first': 'Rajesh', 'name_last': 'Kumar'}], 'is_public': True}]
all_channels_messages = [{'channel_id': 1, 'total_messages': 55, 'standup_active': False, 'standup_buffer': '',
 'messages':[{'message_id': 1, 'u_id': 1, 'message': 'Hello', 'time_created': int(datetime.datetime.now().strftime('%s')), 'reacts': [{'react_id': 1, 'u_ids': [1]}], 'is_pinned': False}]}]
all_channels_permissions = [{'channel_id': 1, 'u_id': 1, 'channel_permission_id': 1}] ## 1 = owner, 2 = admin, 3 = just member
list_of_users = [{'handle_str': 'RajeshKumar', 'email': 'rajeshkumar@gmail.com', 'password': 'V@lidPassword123', 'u_id': 1, 'token' : 12345, 'reset_code': None, 'name_first': 'Rajesh', 'name_last': 'Kumar', 'app_permission_id': 1}]
number_of_messages = 0
number_of_channels = 1
'''
atexit.register(pickle_data, all_channels_details, all_channels_messages, all_channels_permissions, list_of_users, number_of_channels, number_of_messages)
#===============================================================================#
#=============================== GENERAL HELPERS ===============================#
#===============================================================================#

## GET FUNCTIONS
def get_user_details(token_or_u_id):
    for user in list_of_users:
        if user['token'] == token_or_u_id or user['u_id'] == token_or_u_id:
            return {'u_id': user['u_id'], 'token': user['token'], 'name_first': user['name_first'], 'name_last': user['name_last'], 'handle_str': user['handle_str'], 'email': user['email'], 'reset_code': user['reset_code'], 'app_permission_id': user['app_permission_id']}
    return {}

def get_user_from_token(token):
    return_dict = get_user_details(token)
    return return_dict['u_id']

def get_token_from_user(u_id):
    return_dict = get_user_details(u_id)
    return return_dict['token']

def get_user_app_permission(u_id):
    return_dict = get_user_details(u_id)
    return return_dict['app_permission_id']

## GENERATE FUNCTIONS   
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

## CHECK FUNCTIONS
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
        if u_id == user['u_id'] and token == user['token']:
                return True
    return False

def check_valid_handle(handle_str):
    for user in list_of_users:
        if handle_str == user['handle_str']:
            return True
    return False 
    

    
    
#===============================================================================#
#================================= AUTH HELPERS ================================#
#===============================================================================#
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

def valid_email(email):

    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' 
    
    if re.search(regex, email) is None:
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
    return str(reset_code)
  

    
#===============================================================================#
#=============================== CHANNEL HELPERS ===============================#
#===============================================================================#

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
                if users['u_id'] == u_id:
                    return True
            break
    return False

def get_total_channel_messages(channel_id):
    for channels in all_channels_messages:
        if channel_id == channels['channel_id']:
            return channels['total_messages']
    return {}

def get_channel_id_from_name(name):
    for channels in all_channels_details:
        if channels['name'] == name:
            return channels['channel_id']
    return {}

def get_user_channel_permission(channel_id, u_id):
    for users in all_channels_permissions:
        if users['channel_id'] == channel_id:
            if users['u_id'] == u_id:
                return users['channel_permission_id']

#===============================================================================#
#=============================== MESSAGE HELPERS ===============================#
#===============================================================================#
global valid_reacts
valid_reacts = [1,2,3]


# Return None if message does not exist
def find_message_info(message_id):
    for channel in all_channels_messages:
        for message in channel["messages"]:
            if message["message_id"] == message_id:
                return {"channel": channel, "message": message}
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
def change_user_app_permission(u_id, permission_id):
    for user in list_of_users:
        if u_id == user['u_id']:
            user['app_permission_id'] = permission_id
            break
    return {}

def change_user_channel_permission(u_id, permission_id, channel_id):
    added_person = False
    user_found = False
    print({"u_id": u_id, "permission_id": permission_id, "channel_id": channel_id})
    for user in all_channels_permissions:
        if u_id == user['u_id']:
            user_found = True
            if channel_id == user['channel_id']:
                user['channel_permission_id'] = permission_id
                added_person = True
                return {'added_id': u_id, 'changed_permission': permission_id}
    if added_person == False or user_found == False:
        all_channels_permissions.append({'channel_id': channel_id, 'u_id': u_id, 'channel_permission_id': 1})
    

def reset_data():
    global number_of_users 
    global number_of_channels
    all_channels_details.clear()
    all_channels_messages.clear()
    list_of_users.clear()
    all_channels_permissions.clear()
    number_of_users = 0
    number_of_channels = 0
    number_of_messages = 0
    
#===============================================================================#
#=============================== STANDUP HELPERS ===============================#
#===============================================================================#  

def check_standup_active(channel_id):

    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            if channel['standup_active'] == True:
                return True
                
    return False
    
    
def start_standup(channel_id):

    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            channel['standup_active'] = True
    return {}
                    
def end_standup(channel_id):

    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            channel['standup_active'] = False    
    return {}
                
                
def add_to_standup_queue(channel_id, message):

    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            channel['standup_buffer'] = channel['standup_buffer'] + ": " + message
    return {}
            
            
                           
