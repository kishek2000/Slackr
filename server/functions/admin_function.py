from functions.helper_functions import *
from functions.Errors import AccessError    

def admin_userpermission_change(token, u_id, permission_id):
    
    #Checking for valid u_id
    if not check_valid_u_id(u_id):
        raise ValueError("Invalid u_id")
        
    if not check_valid_token(token):
        raise ValueError("Invalid token")
        
    if permission_id == None:
        raise ValueError("Invalid permission_id")
    
    if permission_id > 3 or permission_id < 1:
        raise ValueError("Invalid permission_id")
    
    AdminreturnedDict = get_user_details(token)
    #userDict = {'app_permission_id': AdminreturnedDict['app_permission_id']}
    
    
    if AdminreturnedDict['app_permission_id'] == 3:
        raise AccessError("Unauthorised to change permission")
    
    for user in list_of_users:
        if user['u_id'] == u_id:
            user['app_permission_id'] = permission_id
    


