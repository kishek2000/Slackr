from helper_functions import * 
    

def user_profile(token, u_id):
    
    #Checking for valid u_id
    if not check_valid_u_id(u_id):
        raise ValueError("Invalid u_id")
    returnedDict = get_user_details(token)
    userDict = {'email': returnedDict['email'], 'name_first': returnedDict['name_first'], 'name_last': returnedDict['name_last'], 'handle_str': returnedDict['handle_str']}
    return userDict


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
    
     #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid email")
    
    for user in list_of_users:
        if user['token'] == token:
            user['email'] = email
    
    
def user_profile_sethandle(token, handle_str):

    #Checking for valid handle_str
    if len(name_first) > 20 or len(name_first) < 3:
        raise ValueError("Invalid handle_str")
   
   #Checking for valid handle_str
    if not check_valid_handle(handle_str):
        raise ValueError("Invalid name_last")
    
    for user in list_of_users:
        if user['token'] == token:
            user['handle_str'] = handle_str

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):

    # https://auth0.com/blog/image-processing-in-python-with-pillow/


