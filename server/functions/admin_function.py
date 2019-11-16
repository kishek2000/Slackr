''' admin_functions written by Harry '''
from functions.helper_functions import check_valid_u_id, check_valid_token, get_user_details, list_of_users
from functions.Errors import AccessError, ValueError, authorise_token

@authorise_token
def admin_userpermission_change(token=None, u_id=None, permission_id=None):
    """ admin_userpermission_change function """

    #Checking for valid u_id
    if not check_valid_u_id(u_id):
        raise ValueError("Invalid u_id")

    if permission_id is None:
        raise ValueError("Invalid permission_id")

    if permission_id > 3 or permission_id < 1:
        raise ValueError("Invalid permission_id")

    admin_returned_dict = get_user_details(token)

    if admin_returned_dict['app_permission_id'] == 3:
        raise AccessError("Unauthorised to change permission")

    for user in list_of_users:
        if user['u_id'] == u_id:
            user['app_permission_id'] = permission_id
