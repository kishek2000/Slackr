from functions.helper_functions import *
from PIL import Image
import requests
from functions.Errors import AccessError
    

def user_profile(token, u_id):
    
    if not check_valid_token(token):
        raise AccessError("Invalid token")

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
    
    if not check_valid_token(token):
        raise AccessError("Invalid token")
    
    for user in list_of_users:
        if user['token'] == token:
            user['name_first'] = name_first
            user['name_last'] = name_last
    
    
def user_profile_setemail(token, email):
    
    #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid email")
    
    if not check_valid_token(token):
        raise AccessError("Invalid token")
    
    for user in list_of_users:
        if user['token'] == token:
            user['email'] = email
    
    
def user_profile_sethandle(token, handle_str):

    if not check_valid_token(token):
        raise AccessError("Invalid token")

    #Checking for valid handle_str
    if len(handle_str) > 20 or len(handle_str) < 3:
        raise ValueError("Invalid handle_str")
   
    #Checking for valid handle_str
    if check_valid_handle(handle_str):
        raise ValueError("Invalid handle_str")
    
    for user in list_of_users:
        if user['token'] == token:
            user['handle_str'] = handle_str

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):

    if not check_valid_token(token):
        raise AccessError("Invalid token")
    
    if x_start > x_end or y_start > y_end:
        raise ValueError("Invalid dimensions")

    # https://auth0.com/blog/image-processing-in-python-with-pillow/
    #need to handle if image doesnt exist
    r = requests.head(str(img_url))
    if r.status_code != 200:
        raise ValueError("Invalid img_url")
    
    image = Image.open(requests.get(str(img_url), stream=True).raw)
    imgX = image.size[0]
    imgY = image.size[1]
    if x_start > imgX or x_end > imgX:
        raise ValueError("Invalid x_dimension")
    
    if y_start > imgY or y_end > imgY:
        raise ValueError("Invalid y_dimension")
    
    box = (x_start, y_start, x_end, y_end)
    cropped_image = image.crop(box)
    
    #return cropped_image

