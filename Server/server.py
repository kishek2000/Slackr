"""Flask server"""
import sys
from json import dumps
from flask import Flask, request
sys.path.insert(1, 'Server/functions/')
from auth_functions import *


APP = Flask(__name__)
#echo/get
@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })
#echo/post
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
        
    email = request.form.get('Email')
    password = request.form.get('Password')
        
    try:
    
        user_details = auth_login(email, password)
        return dumps({'u_id' : user_details['u_id'] ,'token' : user_details['token']})
        
    except ValueError as error:
        
        return {'error': error}
        

@APP.route('/auth/logout', methods=['POST'])
def logout_user():
    
    token = request.form.get('Token')
    
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
    
        user_details = auth_register(email, password, name_first, name_last)
        
    except ValueError as error:
        
        return {'error': error}

    
    return dumps({'u_id' : user_details['u_id'] ,'token' : user_details['token']})


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



if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
    
    
    
