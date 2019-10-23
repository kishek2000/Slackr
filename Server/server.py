"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request
from functions.auth_functions import *
from functions.channel_functions import *

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
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    try:
        channel_invite(token, channel_id, u_id)
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/details', methods=['GET'])
def get_channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    try:
        returning_dict = channel_details(token, channel_id)
        return dumps(returning_dict)
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/messages', methods=['GET'])
def get_channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')

    try: 
        returning_messages = channel_messages(token, channel_id, start)
        return dumps(returning_messages)
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/leave', methods=['POST'])
def leave_channel():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    
    try:
        channel_leave(token, channel_id)
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/join', methods=['POST'])
def join_channel():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')

    try:
        channel_join(token, channel_id)
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/addowner', methods=['POST'])
def add_owner_to_channel():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    try:
        channel_addowner(token, channel_id, u_id)
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/removeowner', methods=['POST'])
def remover_owner_from_channel():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    try:
        channel_removeowner(token, channel_id, u_id)
    except ValueError as error:
        return {'error': error}

@APP.route('/channels/list', methods=['GET'])
def get_channels_list():
    token = request.args.get('token')

    try: 
        returning_list_dictionary = channels_list(token)
        print("list:")
        print(returning_list_dictionary)
        return dumps(returning_list_dictionary)
    except ValueError as error:
        return {'error': error}

@APP.route('/channels/listall', methods=['GET'])
def get_channels_listall():
    token = request.args.get('token')
    try: 
        returning_listall_dictionary = channels_listall(token)
        print("list:")
        print(returning_listall_dictionary)
        return dumps(returning_listall_dictionary)
    except ValueError as error:
        return {'error': error}

@APP.route('/channels/create', methods=['POST'])
def create_channel():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    try:
        new_channel_id = channels_create(token, name, is_public)
        return dumps(new_channel_id)
    except ValueError as error:
        return {'error': error}

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 6000))
    
    
    
