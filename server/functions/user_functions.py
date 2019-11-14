""" user_functions """
import sys
#import os
import urllib.request
import requests
from PIL import Image

sys.path.append("/Server/functions/")
from functions.helper_functions import check_valid_token, check_valid_u_id, get_user_details, valid_email, check_valid_handle, list_of_users
from functions.Errors import AccessError

def authorise_token(function):
    def wrapper(*args, **kwargs):
        argsList = list(args)
        if not check_valid_token(argsList[0]):
            raise AccessError("Token is Invalid")
        return function(*args, **kwargs)
    return wrapper

@authorise_token
def user_profile(token, u_id):
    """ user_profile function """

    #Checking for valid u_id
    if not check_valid_u_id(u_id):
        raise ValueError("Invalid u_id")
    returned_dict = get_user_details(token)

    user_dict = {'email': returned_dict['email'], 'name_first': returned_dict['name_first'], 'name_last': returned_dict['name_last'], 'handle_str': returned_dict['handle_str'], 'profile_img_url': returned_dict['profile_img_url']}
    return user_dict

@authorise_token
def user_profile_setname(token, name_first, name_last):
    """ user_profile_setname function """

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

@authorise_token
def user_profile_setemail(token, email):
    """ user_profile_setemail function """

    #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid email")

    for user in list_of_users:
        if user['token'] == token:
            user['email'] = email

@authorise_token
def user_profile_sethandle(token, handle_str):
    """ user_profile_sethandle function """

    #Checking for valid handle_str
    if len(handle_str) > 20 or len(handle_str) < 3:
        raise ValueError("Invalid handle_str")

    #Checking for valid handle_str
    if check_valid_handle(handle_str):
        raise ValueError("Invalid handle_str")

    for user in list_of_users:
        if user['token'] == token:
            user['handle_str'] = handle_str

@authorise_token
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, url_root=None):
    """ user_profiles_uploadphoto function """
    # https://auth0.com/blog/image-processing-in-python-with-pillow/

    x_start = int(x_start)
    y_start = int(y_start)
    x_end = int(x_end)
    y_end = int(y_end)

    if x_start > x_end or y_start > y_end:
        raise ValueError("Invalid dimensions")

    #need to handle if image doesnt exist
    returned_status = requests.head(str(img_url))
    if returned_status.status_code != 200:
        raise ValueError("Invalid img_url")

    image_path = token + '.jpg'
    image_dir = '.' + '/static/' + image_path    
    
    urllib.request.urlretrieve(str(img_url), image_dir)
    #image = Image.open(requests.get(str(img_url), stream=True).raw)
    image = Image.open(image_dir)
    img_x = image.size[0]
    img_y = image.size[1]

    if x_start > img_y or x_end > img_x:
        raise ValueError("Invalid x_dimension")

    if y_start > img_y or y_end > img_y:
        raise ValueError("Invalid y_dimension")

    box = (x_start, y_start, x_end, y_end)
    cropped_image = image.crop(box)
    cropped_image.save(image_dir)

    for user in list_of_users:
        if user['token'] == token:
            if url_root is None:
                user['profile_img_url'] = 'static/' + image_path
            else:
                user['profile_img_url'] = url_root + 'static/' + image_path

@authorise_token
def users_all(token):
    """ users_all function """

    return {'users': list_of_users}
