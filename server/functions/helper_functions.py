''' Common functions that are used in varying places '''
import re
import random
import hashlib
import atexit
import pickle
import os
import urllib.request
'''
    Note: for permission ids, we are saying that 1 is owner, 2 is admin and 3 is member.
    1 and 2 have same permissions but 2 cannot change the privileges that 1 has.
    First member that is added to Slackr has owner permission. Only other owners could then
    change this.
'''

#===============================================================================#
#============================== PICKLING HELPERS ===============================#
#===============================================================================#

def pickle_data(all_channels_details, all_channels_messages, all_channels_permissions,
                list_of_users, number_of_channels, number_of_messages, number_of_users):
    '''Pickles data at end of runtime'''
    pickle.dump(all_channels_details, open('server/functions/data/all_channels_details.p', 'wb'))
    pickle.dump(all_channels_messages, open('server/functions/data/all_channels_messages.p', 'wb'))
    pickle.dump(all_channels_permissions, open('server/functions/data/all_channels_permissions.p', 'wb'))
    pickle.dump(list_of_users, open('server/functions/data/list_of_users.p', 'wb'))
    pickle.dump(number_of_channels, open('server/functions/data/number_of_channels.p', 'wb'))
    pickle.dump(number_of_messages, open('server/functions/data/number_of_messages.p', 'wb'))
    pickle.dump(number_of_users, open('server/functions/data/number_of_messages.p', 'wb'))

global number_of_users
global number_of_messages
global number_of_channels
all_channels_details = pickle.load(open("server/functions/data/all_channels_details.p", "rb"))
all_channels_messages = pickle.load(open("server/functions/data/all_channels_messages.p", "rb"))
all_channels_permissions = pickle.load(open("server/functions/data/all_channels_permissions.p", "rb"))
list_of_users = pickle.load(open("server/functions/data/list_of_users.p", "rb"))
number_of_channels = pickle.load(open("server/functions/data/number_of_channels.p", "rb"))
number_of_messages = pickle.load(open("server/functions/data/number_of_messages.p", "rb"))
number_of_users = pickle.load(open("server/functions/data/number_of_users.p", "rb"))
atexit.register(pickle_data, all_channels_details, all_channels_messages, all_channels_permissions,
                list_of_users, number_of_channels, number_of_messages, number_of_users)

def reset_data():
    ''' Resets all existing stored data '''
    global number_of_users
    global number_of_channels
    global number_of_messages
    all_channels_details.clear()
    all_channels_messages.clear()
    list_of_users.clear()
    all_channels_permissions.clear()
    number_of_users = 0
    number_of_channels = 0
    number_of_messages = 0
    if not [f for f in os.listdir('./static/') if not f.startswith('.')] == []:
        images = [i for i in os.listdir('./static/') if i.endswith(".jpg")]
        for i in images:
            os.remove(os.path.join('./static/', i))
    make_default_photo()

#===============================================================================#
#=============================== GENERAL HELPERS ===============================#
#===============================================================================#

## GET FUNCTIONS
def get_user_details(token_or_u_id):
    ''' Used to retrieve user details based on a varying input '''
    for user in list_of_users:
        if user['token'] == token_or_u_id or user['u_id'] == token_or_u_id:
            return {'u_id': user['u_id'], 'token': user['token'], 'name_first': user['name_first'], 'name_last': user['name_last'], 'handle_str': user['handle_str'], 'email': user['email'], 'reset_code': user['reset_code'], 'app_permission_id': user['app_permission_id'], 'profile_img_url': user['profile_img_url']}
    return {}

def get_user_from_token(token):
    ''' function description '''
    return_dict = get_user_details(token)
    return return_dict['u_id']

def get_token_from_user(u_id):
    ''' function description '''
    return_dict = get_user_details(u_id)
    return return_dict['token']

def get_user_app_permission(u_id):
    ''' function description '''
    return_dict = get_user_details(u_id)
    return return_dict['app_permission_id']

## GENERATE FUNCTIONS
def generate_token(email):
    ''' Used to generate user token based on email '''
    for user in list_of_users:
        if user['email'] == email:
            hashed_token = hashlib.sha256(email.encode()).hexdigest()
            user['token'] = hashed_token
    return hashed_token

def generate_u_id():
    ''' Assigns a unique u_id to a user '''
    global number_of_users
    number_of_users += 1
    return number_of_users

## CHECK FUNCTIONS
def check_valid_u_id(u_id):
    ''' Checks if u_id exists '''
    for user in list_of_users:
        if u_id == user['u_id']:
            return True
    return False

def check_valid_token(token):
    ''' Checks if token exists '''
    for user in list_of_users:
        if token == user['token']:
            return True
    return False

def check_token_matches_user(u_id, token):
    ''' Checks if token and u_id is from same user '''
    for user in list_of_users:
        if u_id == user['u_id'] and token == user['token']:
            return True
    return False

def check_valid_handle(handle_str):
    ''' Checks if handle exists '''
    for user in list_of_users:
        if handle_str == user['handle_str']:
            return True
    return False


#===============================================================================#
#================================= AUTH HELPERS ================================#
#===============================================================================#

def email_registered(email):
    ''' Does email already exist '''
    for user in list_of_users:
        if email == user['email']:
            return True

    return False

def email_matches_password(registered_email, password):
    ''' Checks if email and password come from same user '''
    for user in list_of_users:
        if registered_email == user['email'] and password == user['password']:
            return True

    return False

def valid_email(email):
    ''' To check whether an email is valid the method from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/ was used '''

    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if re.search(regex, email) is None:
        return False
    return True

def valid_password(password):
    ''' Checks if password meets is strong enough '''
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

#To check for special characters in a string the method from https://www.geeksforgeeks.org/python-program-check-string-contains-special-character/ was used

        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        if regex.search(character) is not None:
            no_of_special_characters += 1


    if (no_of_characters >= 1 and no_of_numbers >= 1 and
            no_of_upper_case >= 1 and no_of_lower_case >= 1 and
            no_of_special_characters >= 1 and len(password) >= 6):

        return True

    return False

def generate_handle(name_first, name_last):
    '''Generates handle based on first and last names'''
    if len(name_first + name_last) > 20:
        if len(name_first) > 20 and len(name_last) < 20:
            handle = name_first[0] + name_last

        elif len(name_last) > 20 and len(name_first) < 20:
            handle = name_first + name_last[0]

        else:
            handle = name_first[0:2] + name_last[0:2]

    else:
        handle = name_first + name_last

    return handle

#Following method of hashing password obtained from the COMP1531 lecture on 14th October 2019
def password_hash(password):
    ''' Hashes Password '''
    return hashlib.sha256(password.encode()).hexdigest()

def generate_reset_code():
    ''' Create reset code to send to user '''
    reset_code = random.randint(1, 10000000)
    return str(reset_code)


#===============================================================================#
#=============================== CHANNEL HELPERS ===============================#
#===============================================================================#

def check_valid_channel_id(channel_id):
    ''' Checks if channel id exists '''
    for channel in all_channels_details:
        if channel_id == channel['channel_id']:
            return True
    return False

def generate_channel_id():
    ''' Creat new and unique channel_id '''
    global number_of_channels
    number_of_channels += 1
    return number_of_channels

def check_token_in_channel(token, channel_id):
    ''' Check if user token exists in channel '''
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if check_token_matches_user(users['u_id'], token):
                    return True
            break
    return False

def check_user_in_channel(u_id, channel_id):
    ''' Checks if user u_id exists in channel '''
    for channels in all_channels_details:
        if channel_id == channels['channel_id']:
            for users in channels['all_members']:
                if users['u_id'] == u_id:
                    return True
            break
    return False

def get_total_channel_messages(channel_id):
    ''' Returns the amount of messages in a given channel '''
    for channels in all_channels_messages:
        if channel_id == channels['channel_id']:
            return channels['total_messages']
    return {}

def get_channel_id_from_name(name):
    ''' Get channel_id from channel name '''
    for channels in all_channels_details:
        if channels['name'] == name:
            return channels['channel_id']
    return {}

def get_user_channel_permission(channel_id, u_id):
    ''' Get user permission in a given channel '''
    for users in all_channels_permissions:
        if users['channel_id'] == channel_id:
            if users['u_id'] == u_id:
                return users['channel_permission_id']
    return None

def message_reacts_helper(message_list, uid):
    ''' This helper handles the reactions code in channel/messages '''
    for message in message_list:
        for react in message['reacts']:
            if uid in react["u_ids"]:
                react["is_this_user_reacted"] = True
            else:
                react["is_this_user_reacted"] = False

def update_channels_details():
    ''' Update user information in channels '''
    for channels in all_channels_details:
        for users in channels['owner_members']:
            returned_dict = get_user_details(users['u_id'])
            #print(returned_dict['profile_img_url'])
            users['name_first'] = returned_dict['name_first']
            users['name_last'] = returned_dict['name_last']
            users['profile_img_url'] = returned_dict['profile_img_url']
        for users in channels['all_members']:
            returned_dict = get_user_details(users['u_id'])
            users['name_first'] = returned_dict['name_first']
            users['name_last'] = returned_dict['name_last']
            users['profile_img_url'] = returned_dict['profile_img_url']

#===============================================================================#
#=============================== MESSAGE HELPERS ===============================#
#===============================================================================#
VALID_REACTS = [1, 2, 3]

def find_message_info(message_id):
    '''Returns pointer to message item in all_channels_messages, or none if not found'''
    for channel in all_channels_messages:
        for message in channel["messages"]:
            if message["message_id"] == message_id:
                return {"channel": channel, "message": message}
    return None

def has_user_reacted(uid, react_id, message):
    '''Returns true if user has reacted, false otherwise'''
    for react in message["reacts"]:
        if react_id == react["react_id"]:
            if uid in react["u_ids"]:
                return True
            return False
    return False

def generate_message_id():
    '''Creates a new message id by starting at 1 and adding one for each message'''
    global number_of_messages
    number_of_messages += 1
    return number_of_messages

#===============================================================================#
#================================ USER HELPERS =================================#
#===============================================================================#

def fix_img_url(url_root):
    ''' Update to most recent host in user dict ''' 
    for user in list_of_users:
        if user['profile_img_url'] is not None:
            data = user['profile_img_url'].split('static/')
            identifier = data[1].split('.')
            img_type = str(identifier[0])
            if img_type == 'default':
                new_url = url_root + 'static/default.jpg'
                user['profile_img_url'] = new_url
            else:
                new_url = url_root + 'static/' + str(user['u_id']) + '.jpg'
                user['profile_img_url'] = new_url

def default_photo(url_root):
    ''' Set the default photo '''
    for user in list_of_users:
        if user['profile_img_url'] is None:
            new_url = url_root + 'static/default.jpg'
            user['profile_img_url'] = new_url

def make_default_photo():
    ''' Make a default photo '''
    image_dir = './static/default.jpg'    
    urllib.request.urlretrieve('https://images-na.ssl-images-amazon.com/images/I/41mUvRO4kXL.jpg', image_dir)

#===============================================================================#
#============================= PERMISSIONS HELPERS =============================#
#===============================================================================#
def change_user_app_permission(u_id, permission_id):
    ''' Change permission_id of a given user '''
    for user in list_of_users:
        if u_id == user['u_id']:
            user['app_permission_id'] = permission_id
            break
    return {}

def change_user_channel_permission(u_id, permission_id, channel_id):
    ''' Change channel_permission_id of a given user '''
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
    if not added_person or not user_found:
        all_channels_permissions.append({'channel_id': channel_id, 'u_id': u_id, 'channel_permission_id': 1})


#===============================================================================#
#=============================== STANDUP HELPERS ===============================#
#===============================================================================#

def add_to_standup_queue(channel_id, message, token):
    ''' Adds a message to the queue of messages from a standup '''
    user_details = get_user_details(token)
    handle = user_details["handle_str"]
    for channel in all_channels_messages:
        if channel_id == channel['channel_id']:
            channel['standup_buffer'] = channel['standup_buffer'] + handle + ": " + message + '\n'
    return {}
