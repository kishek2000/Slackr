''' admin_functions written by Harry '''
from functions.helper_functions import check_valid_u_id, check_valid_token, get_user_details, list_of_users
from functions.helper_functions import change_user_app_permission, change_user_channel_permission, all_channels_details
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

    change_user_app_permission(u_id, permission_id)
    if (permission_id <= 2):
        for channels in all_channels_details:
            for user in channels['all_members']:
                if user['u_id'] == u_id:
                    channels['owner_members'].append(get_user_details(u_id))
                    change_user_channel_permission(u_id, permission_id, channels['channel_id'])
