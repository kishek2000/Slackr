'''
user_functions written by Harry
-> user_profile
-> user_profile_setname
-> user_profile_setemail
-> user_profile_sethandle
-> user_profiles_uploadphoto
-> users_all
'''
import sys
import urllib.request
import requests
from PIL import Image

sys.path.append("/Server/functions/")
from functions.helper_functions import check_valid_u_id, get_user_details, check_valid_handle, list_of_users, update_channels_details
from functions.Errors import AccessError, ValueError, authorise_token, check_name_validity, check_valid_email

@authorise_token
def user_profile(token=None, u_id=None):
    """ user_profile function """

    #Checking for valid u_id
    if not check_valid_u_id(u_id):
        raise ValueError("Invalid u_id")
    returned_dict = get_user_details(u_id)

    user_dict = {'email': returned_dict['email'], 'name_first': returned_dict['name_first'], 'name_last': returned_dict['name_last'], 'handle_str': returned_dict['handle_str'], 'profile_img_url': returned_dict['profile_img_url']}
    return user_dict

@check_name_validity
@authorise_token
def user_profile_setname(token=None, name_first=None, name_last=None):
    """ user_profile_setname function """
    for user in list_of_users:
        if user['token'] == token:
            user['name_first'] = name_first
            user['name_last'] = name_last
    update_channels_details()

@check_valid_email
@authorise_token
def user_profile_setemail(token=None, email=None):
    """ user_profile_setemail function """
    for user in list_of_users:
        if user['token'] == token:
            user['email'] = email
    update_channels_details()

@authorise_token
def user_profile_sethandle(token=None, handle_str=None):
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
    update_channels_details()

@authorise_token
def user_profiles_uploadphoto(token=None, img_url=None, x_start=None, y_start=None, x_end=None, y_end=None, url_root=None):
    """ user_profiles_uploadphoto function """
    # https://auth0.com/blog/image-processing-in-python-with-pillow/

    x_start = int(x_start)
    y_start = int(y_start)
    x_end = int(x_end)
    y_end = int(y_end)

    if x_start > x_end or y_start > y_end:
        raise ValueError("Invalid dimensions")

    #need to handle if image doesnt exist
    try:
        returned_status = requests.head(str(img_url))
        if returned_status.status_code != 200:
            raise ValueError("Invalid img_url")
    except:
        raise ValueError("Invalid img_url")

    returned_dict = get_user_details(token)
    image_path = str(returned_dict['u_id']) + '.jpg'
    image_dir = '.' + '/static/' + image_path

    urllib.request.urlretrieve(str(img_url), image_dir)
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
    update_channels_details()

@authorise_token
def users_all(token=None):
    """ users_all function """
    user_list = []
    for user in list_of_users:
        new_dict = {'u_id': user['u_id'], 'email': user['email'], 'name_first': user['name_first'], 'name_last': user['name_last'], 'handle_str': user['handle_str'], 'profile_img_url': user['profile_img_url']}
        user_list.append(new_dict)
    return {'users': user_list}
