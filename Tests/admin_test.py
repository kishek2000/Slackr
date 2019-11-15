''' Test admin_userpermission_change '''
import sys
import pytest
sys.path.append('server/')
from functions.admin_function import admin_userpermission_change
from functions.auth_functions import auth_register
from functions.helper_functions import reset_data
from functions.Errors import AccessError

@pytest.fixture
def register_account():
    ''' Set up temporary data '''
    reset_data()
    return_list = []
    return_list.append(auth_register(email='example@gmail.com', password='P@ssword123', name_first='dan', name_last='man'))
    return_list.append(auth_register(email='example2@gmail.com', password='P@ssword123', name_first='Epic', name_last='Style'))
    return return_list

#################################################################################
##                       TESTING admin_userpermission_change                   ##
#################################################################################
# admin_userpermission_change tests
# function inputs: token, u_id, permission_id
# function returns:

#This test ensures that nothing is returned when calling the function
def test_admin_no_return(register_account):
    ''' Ensure that the function does not return anything '''
    token = register_account[0]['token']
    u_id = register_account[1]['u_id']
    assert admin_userpermission_change(token, u_id, 3) is None

#This function should raise an error when the permission_id is empty
def test_admin_no_input(register_account):
    ''' Test no input '''
    token = register_account[0]['token']
    u_id = register_account[1]['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change(token, u_id, None)

#This function should raise an error when the u_id is invalid
def test_admin_u_id_invalid(register_account):
    ''' Test invalid u_id '''
    token = register_account[0]['token']
    with pytest.raises(ValueError):
        admin_userpermission_change(token, 'wrong u_id', 3)

#This function should raise an error when the token is invalid
def test_admin_token_id_invalid(register_account):
    ''' Test invalid token '''
    u_id = register_account[1]['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change('wrong token', u_id, 3)

#This function should raise an error when the permission_id is invalid
def test_admin_permission_id_invalid(register_account):
    ''' Test invalid permission id '''
    token = register_account[1]['token']
    u_id = register_account[0]['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change(token, u_id, 10)

#Test a user who is unauthorised to change
def test_admin_user_unauthorised(register_account):
    ''' Test unauthorised user '''
    token = register_account[1]['token']
    u_id = register_account[0]['u_id']
    with pytest.raises(AccessError):
        admin_userpermission_change(token, u_id, 1)

reset_data()
