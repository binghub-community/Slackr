"""Flask server"""
#https://hackersandslackers.com/the-art-of-building-flask-routes/
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request, jsonify
from auth_functions import auth_register, auth_login, auth_logout, auth_password_request, auth_passwordreset


APP = Flask(__name__)
CORS(APP)

@APP.route('/auth/register', methods=['POST'])
def register(): 
#do I call this function the same as auth_functions halp idk
	email = request.form.get("email")
	password = request.form.get("password")
	name_first = request.form.get("name_first")
	name_last = request.form.get("name_last")
	
	#call your function (pass in the args)
	dumps = auth_register(email, password, name_first, name_last)
	return dumps

def echo4():
    pass

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

@APP.route('/auth/login', methods=['POST'])
def login():
	email = request.form.get("email")
	password = request.form.get("password")
	dumps = auth_login(email,password)
	return dumps()
	
@APP.route('/auth/logout', methods=['POST'])
def logout():
	token = request.form.get("token")
	dumps = auth_logout
	if dumps == 0:
		return jsonify({"is_success"})
	
	return jsonify({"is_failed"})

@APP.route('/auth/passwordreset/request', methods=['POST'])
def auth_password_request():
	email = request.form.get('email')
	dumps = auth_passwordreset(email)
	return {}

# @APP.route('/auth/passwordreset/reset', methods=['POST'])
# def auth_passwordreset():
# 	reset_code = request.form.get('reset_code')
# 	new_password = request.form.get('new_password')
# 	dumps = auth_passwordreset(reset_code, new_password)
# 	return {}

# @APP.route('/channel/invite', methods=['POST'])
# 	token = request.form.get('token')
# 	channel_id = request.form.get('channel_id')
# 	u_id = request.form.get('u_id')
# 	return {}

# @APP.route('/channel/details', methods=['GET'])
# 	token = request.args.get('token')
# 	channel_id = request.args.get('channel_id')
# 	return {}
	

# @APP.route('/channel/messages', methods=['GET'])
# 	token = request.args.get('token')
# 	channel_id = request.args.get('channel_id')
# 	start = request.start.get('start')

# @APP.route('/channel/leave', methods=['POST'])
# 	token = request.form.get('token')
# 	channel_id = request.form.get('channel_id')
# 	return;

# @APP.route('/channel/join', methods=['POST'])
# 	token = request.form.get('token')
# 	channel_id = request.form.get('channel_id')
# 	return;

# @APP.route('/channel/addowner', methods=['POST'])
# 	token = request.form.get('token')
# 	channel_id = request.form.get('channel_id')
# 	u_id = request.form.get('u_id')
# 	return;

# @APP.route('/channel/removeowner', methods=['POST'])
# 	token = request.form.get('token')
# 	channel_id = request.form.get('channel_id')
# 	u_id = request.form.get('u_id')
# 	return;

# @APP.route('/channel/list', methods=['GET'])
# 	token = request.args.get('token')
# 	return({channels:[]})

# @APP.route('/channel/listall', methods=['GET'])
# 	token = request.args.get('token')
# 	return({channels:[]})

# @APP.route('/channel/create', methods=['POST'])
# 	token = request.form.get('token')
# 	name = request.form.get('name')
# 	is_public = request.form.get('is_public')
# 	return({channel_id})

# @APP.route('/message/sendlater', methods=['POST'])

# @APP.route('/message/send', methods=['POST'])

# @APP.route('/message/remove', methods=['DELETE'])

# @APP.route('/message/edit', methods=['PUT'])

# @APP.route('/message/react', methods=['POST'])

# @APP.route('/message/unreact', methods=['POST'])

# @APP.route('/message/pin', methods=['POST'])

# @APP.route('/message/unpin', methods=['POST'])

# @APP.route('/user/profile', methods=['GET'])

# @APP.route('/user/profile/setname', methods=['PUT'])

# @APP.route('/user/profile/setemail', methods=['PUT'])

# @APP.route('/user/profile/sethandle', methods=['PUT'])

# @APP.route('/user/profiles/uploadphoto', methods=['POST'])
# 	pass

# @APP.route('/standup/start', methods=['POST'])

# @APP.route('/standup/send', methods=['POST'])

# @APP.route('/search', methods=['GET'])

# @APP.route('/admin/userpermission/change', methods=['POST'])
# def admin_userpermission:	
# 	token = request.form.get('token')
# 	u_id = request.form.get('uid')
# 	permission_id = request.form.get.('permission_id')
# 	#admin_
# 	return {}

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
