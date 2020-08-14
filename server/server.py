"""Flask server"""
#https://hackersandslackers.com/the-art-of-building-flask-routes/
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request, jsonify
from storage import INFO, User, Channel, Message
from auth_functions import *
from channel_functions import *
from users_functions import *
from message_functions import *
from flask_mail import Mail, Message

APP = Flask(__name__)
CORS(APP)

APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'zzteam.69zz@gmail.com',
    MAIL_PASSWORD = "fucking-die1"
)

@APP.route('/send-mail')
def send_mail():
    mail = Mail(APP)
    try:
        msg = Message("Send Mail Test!",
            sender="zzteam.69zz@gmail.com",
            recipients=["harrypark0513@gmail.com"])
        msg.body = "Hello! This is a test body"
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return (str(e))

def echo4():
    pass

@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : dumps(request.args.get('echo')),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : dumps(request.form.get('echo')),
    })

@APP.route('/auth/login', methods=['POST'])
def login():
    email = dumps(request.form.get("email"))
    password = dumps(request.form.get("password"))
    try:
        token = (auth_login(email,password))
        return jsonify(token)
    except Exception as e:
        print(str(e))
        return jsonify({})

#for now returns an empty dictionary on exception, might need to change based on what        #the frontend expects

@APP.route('/auth/logout', methods=['POST'])
def logout():
    token = dumps(request.form.get("token"))
    try:
        return jsonify({
            "is_success": auth_logout(token)
        })
    except Exception as e:
        print(str(e))
        return jsonify({})
    # try:
    #     return "is_success"
    # except Exception:
    #     return "is_fail"
        #for now just returns a string; not sure what the brackets are for in ("is_success)
    #

@APP.route('/auth/register', methods=['POST'])
def register(): 
    email = dumps(request.form.get("email"))
    password = dumps(request.form.get("password"))
    name_first = dumps(request.form.get("name_first"))
    name_last = dumps(request.form.get("name_last"))
    #call your function (pass in the args)
    #return dumps(auth_register(email, password, name_first, name_last))
    try:
        return jsonify(auth_register(email, password, name_first, name_last))
    except Exception as e:
        print(str(e))
        return jsonify({})

@APP.route('/auth/passwordreset/request', methods=['POST'])
def passwordreset_request():
    email = dumps(request.form.get('email'))
    try:
        auth_passwordreset_request(email)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def passwordreset_reset():
    reset_code = dumps(request.form.get('reset_code'))
    new_password = dumps(request.form.get('new_password'))
    try:
        auth_passwordreset_reset(reset_code, new_password)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/channel/invite', methods=['POST'])
def channel_inv():	
    token = dumps(request.form.get('token')).strip('"')
    channel_id = dumps(request.form.get('channel_id')).strip('"')
    u_id = dumps(request.form.get('u_id')).strip('"')
    try:
        channel_invite(token, int(channel_id), int(u_id))
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/channel/details', methods=['GET'])
def channel_dets():
    token = dumps(request.args.get('token')).strip('"')
    channel_id = dumps(request.args.get('channel_id')).strip('"')
    try:
        return jsonify(channel_details(int(channel_id), token))
    except Exception as e:
        print(str(e))
        raise e
        return jsonify({})
	
@APP.route('/channel/messages', methods=['GET'])
def channel_msg():
    token = dumps(request.args.get('token')).strip('"')
    channel_id = dumps(request.args.get('channel_id')).strip('"')
    start = dumps(request.args.get('start')).strip('"')
    try:
        return jsonify(channel_messages(token, int(channel_id), int(start)))
    except Exception as e:
        print(str(e))
        raise e
        return({})

@APP.route('/channel/leave', methods=['POST'])
def leave():	
    token = dumps(request.form.get('token')).strip('"')
    channel_id = dumps(request.form.get('channel_id')).strip('"')
    try:
        channel_leave(token, int(channel_id))
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/channel/join', methods=['POST'])
def join():
    token = dumps(request.form.get('token')).strip('"')
    channel_id = dumps(request.form.get('channel_id')).strip('"')
    try:
        return jsonify(channel_join(token, int(channel_id)))
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/channel/addowner', methods=['POST'])
def addowner():
    token = dumps(request.form.get('token')).strip('"')
    channel_id = dumps(request.form.get('channel_id')).strip('"')
    u_id = dumps(request.form.get('u_id')).strip('"')
    try:
        channel_addowner(token, int(channel_id), int(u_id))
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/channel/removeowner', methods=['POST'])
def removeowner():
    token = dumps(request.form.get('token')).strip('"')
    channel_id = dumps(request.form.get('channel_id')).strip('"')
    u_id = dumps(request.form.get('u_id')).strip('"')
    try:
        channel_removeowner(token, int(channel_id), int(u_id))
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/channels/list', methods=['GET'])
def channel_list():
    token = dumps(request.args.get('token')).strip('"')
    try:
        return jsonify({
            "channels":channels_list(token)
        })
    except Exception as e:
        print(str(e))
        raise e
        return jsonify([])

@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    token = dumps(request.args.get('token')).strip('"')
    try:
        return jsonify({
            "channels": channels_listall(token)
        })
    except Exception as e:
        print(str(e))
        raise e
        return jsonify([])

@APP.route('/channels/create', methods=['POST'])
def channel_create():
    token = dumps(request.form.get('token')).strip('"')
    name = dumps(request.form.get('name'))
    is_public = dumps(request.form.get('is_public'))
    try:
        return jsonify({
            "channel_id": channels_create(is_public, name, token)
        })
    except Exception as e:
        print(str(e))
        raise e
        return jsonify(-1)

@APP.route('/message/sendlater', methods=['POST'])
def msg_sendlater():
    token = dumps(request.form.get('token')).strip('"')
    channel_id = dumps(request.form.get('channel_id')).strip('"')
    message = dumps(request.form.get('message'))
    time_sent = dumps(request.form.get(datetime))
    try:
        return jsonify({
            "message_id": message_sendlater(message, token, int(channel_id), time)
        })
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/message/send', methods=['POST'])
def msg_send():
    token = dumps(request.form.get('token')).strip('"')
    channel_id = dumps(request.form.get('channel_id')).strip('"')
    message = dumps(request.form.get('message')).strip('"')
    try:
        return jsonify({
            "message_id": message_send(message, token, int(channel_id))
        })
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/message/remove', methods=['DELETE'])
def msg_rm():
    message_id = dumps(request.DELETE.get('message_id'))
    token = dumps(request.form.get('token')).strip('"')
    try:
        message_remove(message_id, token)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/message/edit', methods=['PUT'])
def msg_edit():
    token = dumps(request.form.get('token')).strip('"')
    message_id = dumps(request.form.get('message_id'))
    message = dumps(request.form.get('message'))
    try:
        message_edit(message_id, message, token)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/message/react', methods=['POST'])
def msg_react():
    token = dumps(request.form.get('token')).strip('"')
    message_id = dumps(request.form.get('message_id'))
    react_id = dumps(request.form.get('react_id'))
    try:
        message_react(message_id, token, react)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/message/unreact', methods=['POST'])
def msg_unreact():
    token = dumps(request.form.get('token')).strip('"')
    message_id = dumps(request.form.get('message_id'))
    react_id = dumps(request.form.get('react_id'))
    try:
        message_unreact(message_id, token, react)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/message/pin', methods=['POST'])
def msg_pin():
    token = dumps(request.form.get('token')).strip('"')
    message_id = dumps(request.form.get('message_id'))
    try:
        message_pin(message_id, token)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/message/unpin', methods=['POST'])
def msg_unpin():
    token = dumps(request.form.get('token')).strip('"')
    message_id = dumps(request.form.get('message_id'))
    try:
        message_unpin(message_id, token)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/user/profile', methods=['GET'])
def user_prof():
    token = dumps(request.args.get('token')).strip('"')
    u_id = dumps(request.args.get('u_id')).strip('"')
    try:
        return jsonify({
            "user": user_profile(token, int(u_id))
        })
    except Exception as e:
        print(str(e))
        raise e
        return dumps({})

@APP.route('/user/profile/setname', methods=['PUT'])
def user_prof_setname(): 
    token = dumps(request.form.get('token')).strip('"')
    name_first = dumps(request.form.get('name_first'))
    name_last = dumps(request.form.get('name_last'))
    try:
        user_profile_setname(token, name_first, name_last)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_prof_setemail():
    token = dumps(request.form.get('token')).strip('"')
    email = dumps(request.form.get('message_id'))
    try:    
        user_profile_setemail(token, email)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_prof_sethandle():
    token = dumps(request.form.get('token')).strip('"')
    handle_str = dumps(request.form.get('handle_str'))
    try:
        user_profile_sethandle(token, handle_str)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def upload():
    image_url = dumps(request.form.get('img_url'))
    x_start = dumps(request.form.get('x_start'))
    y_start = dumps(request.form.get('y_start'))
    x_end = dumps(request.form.get('x_end'))
    y_end = dumps(request.form.get('y_end'))
    user_profiles_uploadphoto(image_url, x_start, y_start, x_end, y_end)
    return jsonify({})

@APP.route('/standup/start', methods=['POST'])
def standup_start_time():
    token = dumps(request.form.get('token')).strip('"')
    channel_id = dumps(request.form.get('channel_id')).strip('"')
    length = dumps(request.form.get('length'))
    try:   
        return jsonify({
            "time_finish": standup_start(token, channel_id, length)
        })
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/standup/active', methods=['GET'])
def active_standup():
    token = dumps(request.args.get('token')).strip('"')
    channel_id = dumps(request.args.get('channel_id')).strip('"')
    try:
        return jsonify(standup_active(token, int(channel_id)))
    except Exception as e:
        print(str(e))
        raise e        

@APP.route('/standup/send', methods=['POST'])
def stand_send():
    token = dumps(request.form.get('token')).strip('"')
    channel_id = dumps(request.form.get('channel_id')).strip('"')
    message = dumps(request.form.get('message'))
    try:
        standup_send(token, int(channel_id), message)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/search', methods=['GET'])
def app_search():
    token = dumps(request.args.get('token')).strip('"')
    query = dumps(request.args.get('query'))
    try:
        return jsonify({
            "messages": search(token, query)
        })
    except Exception as e:
        print(str(e))
        raise e

@APP.route('/admin/userpermission/change', methods=['POST'])
def admin_userpermission():
    token = dumps(request.form.get('token')).strip('"')
    u_id =dumps(request.form.get('u_id')).strip('"')
    permission_id = dumps(request.form.get('permission_id'))
    try:
        admin_userpermission_change(token, int(u_id), permission_id)
        return jsonify({})
    except Exception as e:
        print(str(e))
        raise e


@APP.route('/users/all', methods=['GET'])
def user_list_get():
    token = dumps(request.args.get('token')).strip('"')
    try:
        return jsonify({
            "users": user_list(token)
        })
    except Exception as e:
        print(str(e))
        raise e
    
if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
