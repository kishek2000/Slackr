import pytest

# admin_userpermission_change tests
# function inputs: token, u_id, permission_id
# function returns:
'''
Things to think about
    - What will permission_id be?
'''

def admin_no_return():
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    anr_token = returned_dict['token']
    anr_u_id = returned_dict['u_id']
    assert user_profile_setname(anr_token, anr_u_id, 'admin') == None
    
def admin_no_input:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    ani_token = returned_dict['token']
    anr_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        user_profile_setname(ani_token, ani_u_id, )
        
def admin_u_id_invalid:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    auii_token = returned_dict['token']
    anr_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        user_profile_setname(auii_token, wrongu_id, 'admin')
        
def admin_permission_id_invalid:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    apii_token = returned_dict['token']
    anr_u_id = returned_dict['u_id']
    with pytest.raises(ValueError):
        user_profile_setname(auii_token, ani_u_id, wrongpermission)

def admin_user_unauthorised:
    returned_dict = auth_register('example@gmail.com', '12345', 'dan', 'man')
    apii_token = returned_dict['token']
    anr_u_id = returned_dict['u_id']
    with pytest.raises(KeyError):
        user_profile_setname(auii_token, ani_u_id, 'admin')
