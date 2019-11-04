"""Flask server"""
import sys
from json import dumps
from datetime import timezone
from flask_cors import CORS
from flask import Flask, request
sys.path.append('server/')
from functions.auth_functions import *
from functions.channel_functions import *
from functions.user_functions import *
from functions.standup_functions import *
from functions.search_function import *
from functions.admin_function import *
from functions.Errors import *
from functions.message_functions import *

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
    """ Description of function """

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user_details = auth_login(email, password)
        return dumps({'u_id' : user_details['u_id'], 'token' : user_details['token']})
    except ValueError as error:
        return {'error': error}


@APP.route('/auth/logout', methods=['POST'])
def logout_user():
    """ Description of function """

    token = request.form.get('token')

    if auth_logout(token):
        return dumps({"Action": "Success"})

    return dumps({"Action": "Failure"})


@APP.route('/auth/register', methods=['POST'])
def create_user():
    """ Description of function """
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
    """ Description of function """
    email = request.form.get('email')

    try:
        auth_passwordreset_request(email)
        return dumps({"Action": "Success"})

    except ValueError as error:

        return {'error': error}


@APP.route('/auth/passwordreset/reset', methods=['POST'])
def reset_password():
    """ Description of function """

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
    """ Description of function """
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
    """ Description of function """
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    try:
        returning_dict = channel_details(token, channel_id)
        return dumps(returning_dict)
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/messages', methods=['GET'])
def get_channel_messages():
    """ Description of function """
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
    """ Description of function """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))

    try:
        channel_leave(token, channel_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/join', methods=['POST'])
def join_channel():
    """ Description of function """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    try:
        channel_join(token, channel_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/channel/addowner', methods=['POST'])
def add_owner_to_channel():
    """ Description of function """
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
    """ Description of function """
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
    """ Description of function """
    token = request.args.get('token')

    try:
        returning_list_dictionary = channels_list(token)
        return dumps({'channels': returning_list_dictionary})
    except ValueError as error:
        return {'error': error}

@APP.route('/channels/listall', methods=['GET'])
def get_channels_listall():
    """ Description of function """
    token = request.args.get('token')
    try:
        returning_listall_dictionary = channels_listall(token)
        return dumps({'channels': returning_listall_dictionary})
    except ValueError as error:
        return {'error': error}

@APP.route('/channels/create', methods=['POST'])
def create_channel():
    """ Description of function """
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    try:
        new_channel_id = channels_create(token, name, is_public)
        return dumps({'channel_id': new_channel_id})
    except ValueError as error:
        return {'error': error}

#===============================================================================#
#===============================     MESSAGES     ==============================#
#===============================================================================#
@APP.route('/message/send', methods=['POST'])
def post_message_send():
    """ Description of function """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')
    try:
        message_id = message_send(token, channel_id, message)
        return dumps({'message_id': message_id})
    except ValueError as error:
        return {'error': error}

@APP.route('/message/sendlater', methods=['POST'])
def post_message_sendlater():
    """ Description of function """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')
    #time_sent = datetime.datetime.strptime(request.form.get('time_sent'), "%Y-%m-%dT%H:%M:%S.%f%z")
    time_sent = int(request.form.get('time_sent'))/1000.0
    try:
        message_id = message_sendlater(token, channel_id, message, time_sent)
        return dumps({'message_id': message_id})
    except ValueError as error:
        print(error)
        return {'error': error}

@APP.route('/message/remove', methods=['DELETE'])
def post_message_remove():
    """ Description of function """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    try:
        message_remove(token, message_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/message/edit', methods=['PUT'])
def put_message_edit():
    """ Description of function """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    message = request.form.get('message')
    try:
        message_edit(token, message_id, message)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/message/react', methods=['POST'])
def post_message_react():
    """ Description of function """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    try:
        message_react(token, message_id, react_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/message/unreact', methods=['POST'])
def post_message_unreact():
    """ Description of function """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    try:
        message_unreact(token, message_id, react_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/message/pin', methods=['POST'])
def post_message_pin():
    """ Description of function """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    try:
        message_pin(token, message_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/message/unpin', methods=['POST'])
def post_message_unpin():
    """ Description of function """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    try:
        message_unpin(token, message_id)
        return dumps({})
    except ValueError as error:
        return {'error': error}

#===============================================================================#
#=================================     USER     ================================#
#===============================================================================#

@APP.route('/user/profile', methods=['GET'])
def get_user_profile():
    """ Description of function """
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    try:
        returning_dict = user_profile(token, u_id)
        return dumps(returning_dict)
    except ValueError as error:
        print(error)
        return {'error': error}

@APP.route("/user/profile/setname", methods=['PUT'])
def put_user_setname():
    """ Description of function """
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
    """ Description of function """
    token = request.form.get('token')
    email = request.form.get('email')
    try:
        user_profile_setemail(token, email)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route("/user/profile/sethandle", methods=['PUT'])
def put_user_sethandle():
    """ Description of function """
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    try:
        user_profile_sethandle(token, handle_str)
        return dumps({})
    except ValueError as error:
        return {'error': error}

@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def post_user_uploadphoto():
    """ Description of function """
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

@APP.route('/users/all', methods=['GET'])
def get_users_all():
    """ Description of function """
    token = request.args.get('token')
    try:
        returning_dict = users_all(token)
        return dumps(returning_dict)
    except ValueError as error:
        print(error)
        return {'error': error}

#===============================================================================#
#=================================   STANDUP    ================================#
#===============================================================================#

@APP.route('/standup/start', methods=['POST'])
def start_standup():
    """ Description of function """

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    length = request.form.get('length')

    try:
        standup_end_time = standup_start(token, channel_id, length)

#To represet 'standup_end_time' numerically as 'timestamp' the following method from https://www.tutorialspoint.com/How-to-convert-Python-date-to-Unix-timestamp was used

        timestamp = standup_end_time.replace(tzinfo=timezone.utc).timestamp()
        return dumps({'time_finish' : timestamp})

    except ValueError as error:
        return {'error': error}

    except AccessError as error:
        return {'error': error}

@APP.route('/standup/active', methods=['GET'])
def standup_active_check():
    """ Description of function """

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    
    try:
        standup_details = standup_active(token, channel_id)
        return dumps({'standup_active' : standup_details['standup_active'], 
                      'time_finish': standup_details['time_finish']})

    except ValueError as error:
        return {'error': error}

    except AccessError as error:
        return {'error': error}

@APP.route('/standup/send', methods=['POST'])
def start_send():
    """ Description of function """

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')

    try:
        standup_send(token, channel_id, message)
        return dumps({})

    except ValueError as error:
        return {'error': error}

    except AccessError as error:
        return {'error': error}

#===============================================================================#
#=================================    SEARCH    ================================#
#===============================================================================#

@APP.route('/search', methods=['GET'])
def get_search():
    """ Description of function """

    token = request.args.get('token')
    query_str = request.args.get('query_str')
    try:
        returning_dict = search(token, query_str)
        return dumps(returning_dict)
    except ValueError as error:
        print(error)
        return {'error': error}

#===============================================================================#
#=================================    ADMIN     ================================#
#===============================================================================#

@APP.route('/admin/userpermission/change', methods=['POST'])
def post_admin_userpermission_change():
    """ Description of function """


    token = request.form.get('token')
    u_id = int(request.form.get('u_id'))
    permission_id = int(request.form.get('permission_id'))

    try:
        admin_userpermission_change(token, u_id, permission_id)
        return dumps({})

    except ValueError as error:
        return {'error': error}

#===============================================================================#
#=================================     MAIN     ================================#
#===============================================================================#

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 6000))

    # End of server.py
