""" user_functions """
import sys
from PIL import Image
import requests
import urllib.request

sys.path.append("/Server/functions/")
from functions.helper_functions import check_valid_token, check_valid_u_id, get_user_details, valid_email, check_valid_handle, list_of_users, generate_reset_code
from functions.Errors import AccessError


def user_profile(token, u_id):
    """ user_profile function """

    if not check_valid_token(token):
        raise AccessError("Invalid token")

    #Checking for valid u_id
    if not check_valid_u_id(u_id):
        raise ValueError("Invalid u_id")
    returned_dict = get_user_details(token)

    user_dict = {'email': returned_dict['email'], 'name_first': returned_dict['name_first'], 'name_last': returned_dict['name_last'], 'handle_str': returned_dict['handle_str']}
    return user_dict


def user_profile_setname(token, name_first, name_last):
    """ user_profile_setname function """

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
    """ user_profile_setemail function """

    #Checking for valid email
    if not valid_email(email):
        raise ValueError("Invalid email")

    if not check_valid_token(token):
        raise AccessError("Invalid token")

    for user in list_of_users:
        if user['token'] == token:
            user['email'] = email


def user_profile_sethandle(token, handle_str):
    """ user_profile_sethandle function """

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
    """ user_profiles_uploadphoto function """
    # https://auth0.com/blog/image-processing-in-python-with-pillow/

    if not check_valid_token(token):
        raise AccessError("Invalid token")

    if x_start > x_end or y_start > y_end:
        raise ValueError("Invalid dimensions")

    #need to handle if image doesnt exist
    returned_status = requests.head(str(img_url))
    if returned_status.status_code != 200:
        raise ValueError("Invalid img_url")
    
    image_name = './server/functions/data/user_images/' + token + '.png'
    urllib.request.urlretrieve(str(img_url), image_name)
    #image = Image.open(requests.get(str(img_url), stream=True).raw)
    image = Image.open(image_name)
    img_x = image.size[0]
    img_y = image.size[1]
    
    if x_start > img_y or x_end > img_x:
        raise ValueError("Invalid x_dimension")

    if y_start > img_y or y_end > img_y:
        raise ValueError("Invalid y_dimension")

    box = (x_start, y_start, x_end, y_end)
    cropped_image = image.crop(box)
    cropped_image.save(image_name)

    cropped_image.save(image_name)

def users_all(token):
    """ users_all function """

    if not check_valid_token(token):
        raise AccessError("Invalid token")

    return {'users': list_of_users}
