"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request
from functions.auth_functions import *
from functions.channel_functions import *
from functions.user_functions import *

APP = Flask(__name__)
CORS(APP)

@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

#===============================================================================#
#=================================     AUTH     ================================#
#===============================================================================#

@APP.route('/auth/login', methods=['POST'])
def login_user():
        
    email = request.form.get('email')
    password = request.form.get('password')
        
    try:
        user_details = auth_login(email, password)
        return dumps({'u_id' : user_details['u_id'] ,'token' : user_details['token']})
    except ValueError as error:
        return {'error': error}
        

@APP.route('/auth/logout', methods=['POST'])
def logout_user():
    
    token = request.form.get('token')
    
    if auth_logout(token):
        return dumps({"Action": "Success"})
    else:
        return dumps({"Action": "Failure"})
        

@APP.route('/auth/register', methods=['POST'])
def create_user():
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        return dumps(auth_register(email, password, name_first, name_last))
    except ValueError as error:
        return {'error': error}

@APP.route('/auth/passwordreset/request', methods=['POST'])
def request_password_reset():

    email = request.form.get('email')

    try:
        auth_passwordreset_request(email)
        return dumps({"Action": "Success"})
        
    except ValueError as error:
        
        return {'error': error}


@APP.route('/auth/passwordreset/reset', methods=['POST'])
def reset_password():

    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')

    try:
    
        auth_passwordreset_reset(reset_code, new_password)
        return dumps({"Action": "Success"})
        
    except ValueError as error:
        
        return {'error': error}


#===============================================================================#
#===============================     CHANNELS     ==============================#
#===============================================================================#
@APP.route('/channel/invite', methods=['POST'])
def invite_to_channel():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    try:
        channel_invite(token, channel_id, u_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/details', methods=['GET'])
def get_channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    try:
        returning_dict = channel_details(token, channel_id)
        return dumps(returning_dict)
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/messages', methods=['GET'])
def get_channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    try: 
        returning_messages = channel_messages(token, channel_id, start)
        return dumps(returning_messages)
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/leave', methods=['POST'])
def leave_channel():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    
    try:
        channel_leave(token, channel_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/join', methods=['POST'])
def join_channel():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    try:
        channel_join(token, channel_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/addowner', methods=['POST'])
def add_owner_to_channel():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    try:
        channel_addowner(token, channel_id, u_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/removeowner', methods=['POST'])
def remover_owner_from_channel():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    try:
        channel_removeowner(token, channel_id, u_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/channels/list', methods=['GET'])
def get_channels_list():
    token = request.args.get('token')

    try: 
        returning_list_dictionary = channels_list(token)
        return dumps({'channels': returning_list_dictionary})
    except ValueError as error:
        return {'error': error}

@APP.route('/channels/listall', methods=['GET'])
def get_channels_listall():
    token = request.args.get('token')
    try: 
        returning_listall_dictionary = channels_listall(token)
        return dumps({'channels': returning_listall_dictionary})
    except ValueError as error:
        return {'error': error}

@APP.route('/channels/create', methods=['POST'])
def create_channel():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    try:
        new_channel_id = channels_create(token, name, is_public)
        return dumps({'channel_id': new_channel_id})
    except ValueError as error:
        return {'error': error}

#===============================================================================#
#=================================     USER     ================================#
#===============================================================================#

@APP.route('/user/profile', methods=['GET'])
def get_user_profile():
        
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id') )
    try:
        returning_dict = user_profile(token, channel_id)
        return dumps(returning_dict)
    except ValueError as error:
        return {'error': error}
        
@APP.route("/user/profile/setname", methods=['PUT'])
def put_user_setname():
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    try:
        user_profile_setname(token, name_first, name_last)
        return dumps({})
    except ValueError as error:
        return {'error': error} 
        
@APP.route("/user/profile/setemail", methods=['PUT'])
def put_user_setemail():
    token = request.form.get('token')
    email = request.form.get('email')
    try:
        user_profile_setemail(token, email)
        return dumps({})
    except ValueError as error:
        return {'error': error} 
        
@APP.route("/user/profile/sethandle", methods=['PUT'])
def put_user_sethandle():
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    try:
        user_profile_sethandle(token, handle_str)
        return dumps({})
    except ValueError as error:
        return {'error': error} 
        
@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def post_user_uploadphoto():
    token = request.form.get('token')
    img_url = request.form.get('img_url')
    x_start = request.form.get('x_start')
    y_start = request.form.get('y_start')
    x_end = request.form.get('x_end')
    y_end = request.form.get('y_end')
    try:
        user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
        return dumps({})
    except ValueError as error:
        return {'error': error}

#===============================================================================#
#=================================     MAIN     ================================#
#===============================================================================#

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 6000))
    
    
    
