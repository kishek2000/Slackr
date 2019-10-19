from helper_functions import * 
from Errors import *
    

def search(token, u_id, permission_id):
    
    #Checking for valid u_id
    if not check_valid_u_id(u_id):
        raise ValueError("Invalid u_id")
        
    if permission_id > 3 or permission_id < 1:
        raise ValueError("Invalid permission_id")
    
    returnedDict = get_user_details(token)
    userDict = {'permission_id': returnedDict['permission_id']}
    
    if userDict['permission_id'] == 3:
        raise AccessError("Unauthorised to change permission")
    
    for user in list_of_users:
        if user['token'] == token:
            user['permission_id'] = permission_id
    


