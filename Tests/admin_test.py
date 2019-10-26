import pytest
import sys
sys.path.append('Server/')
from functions.admin_function import *
from functions.auth_functions import auth_register
from functions.helper_functions import reset_data
from functions.Errors import *

@pytest.fixture
def register_account():
    reset_data()
    returnedDict = auth_register('example@gmail.com', 'P@ssword123', 'dan', 'man')
    auth_register('example2@gmail.com', 'P@ssword123', 'Epic', 'Style')
    return returnedDict

#################################################################################
##                       TESTING admin_userpermission_change                   ##
#################################################################################
# admin_userpermission_change tests
# function inputs: token, u_id, permission_id
# function returns:
'''
Things to think about
    - What will permission_id be?
'''

#This test ensures that nothing is returned when calling the function
def test_admin_no_return(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    assert admin_userpermission_change(token, u_id, 3) == None
    
#This function should raise an error when the permission_id is empty
def test_admin_no_input(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change(token, u_id, None)

#This function should raise an error when the u_id is invalid        
def test_admin_u_id_invalid(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change(token, 'wrong u_id', 3)
        
#This function should raise an error when the token is invalid        
def test_admin_token_id_invalid(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change('wrong token', u_id, 3)
        
#This function should raise an error when the permission_id is invalid        
def test_admin_permission_id_invalid(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change(token, u_id, 10)

#Test a user who is unauthorised to change 
def test_admin_user_unauthorised(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    for user in list_of_users:
        if user['token'] == token:
            user['app_permission_id'] = 3 
    with pytest.raises(AccessError):
        admin_userpermission_change(token, u_id, 1)
