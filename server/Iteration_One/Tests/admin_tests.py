import pytest

@pytest.fixture():
def register_account:
    return auth_register('example@gmail.com', '12345', 'dan', 'man')
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
    assert admin_userpermission_change(token, u_id, 'admin') == None
    
#This function should raise an error when the permission_id is empty
def test_admin_no_input(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change(token, u_id, '')

#This function should raise an error when the u_id is invalid        
def test_admin_u_id_invalid(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change(token, 'wrong u_id', 'admin')
        
#This function should raise an error when the token is invalid        
def test_admin_u_id_invalid(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change('wrong token', u_id, 'admin')
        
#This function should raise an error when the permission_id is invalid        
def test_admin_permission_id_invalid(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    with pytest.raises(ValueError):
        admin_userpermission_change(token, u_id, wrongpermission)

#Test a user who is unauthorised to change 
def test_admin_user_unauthorised(register_account):
    token = register_account['token']
    u_id = register_account['u_id']
    with pytest.raises(AccessError):
        admin_userpermission_change(token, u_id, 'admin')
