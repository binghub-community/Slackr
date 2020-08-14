import re
from datetime import datetime
import random
from werkzeug.security import generate_password_hash
from flask_mail import Mail
from storage import INFO, User, Message
import jwt

#****************************************************************
#****                                                        ****
#****                   helper functions haha                ****
#****                                                        ****
#****************************************************************

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

COUNTER = 0

def check(email):
#   check if valid
    if re.search(regex, email):
        return True
    return False

def send_email(sender, recipient, message):
    msg = Message(sender= sender, recipient= recipient)
    msg.body = text_body
    mail.send(msg)

def generate_userID():
    global COUNTER
    rand = random.sample(range(1000, 9999), 8999)
    COUNTER += 1
    return rand[COUNTER]

#****************************************************************

def auth_login(email, password):
    global INFO
#   value error check for valid email
    # if check(email) != True:
    #     raise ValueError("Email entered is not a valid email") 
#   value error check for existing user
#   latest user loggedIn , stores values     
    loggedIn = {}
    for user in INFO["Users"]:
        if user.getEmail() != email:
            continue
        if user.getEmail() == email and user.getPassword() == password:
            user.setAuth(True)
            loggedIn["u_id"] = user.getID()
            # loggedIn["token"] = generate_password_hash(email)
            secret = "team96"
            loggedIn["token"] = jwt.encode({"some": email}, secret, algorithm='HS256')
            user.setToken(loggedIn["token"])
            return loggedIn
        else:
            raise ValueError("Password is not correct")
    raise ValueError("Email entered does not belong to a user")

def auth_logout(token):
    for user in INFO["Users"]: 
        if user.getToken() == token:
            user.setAuth(False)
            user.setToken(None)
            return True
    return False


def auth_register(email, password, name_first, name_last):
    global INFO
#  # check for valid email
    # if check(str(email)) != True:
    #     raise ValueError("Email entered is not a valid email")
 # check for available email
    for user in INFO["Users"]:
        if email == user.getEmail():
            raise ValueError("Email address is already being used by another user")
 # check for valid password
    if len(password) < 6:
        raise ValueError("Password entered is not a valid password")
 # check for valid first and last name
    if len(name_first) > 50:
        raise ValueError("name_first is more than 50 characters")
    if len(name_last) > 50:
        raise ValueError("name_last is more than 50 characters")
#adding a new user
    userID = generate_userID()
    newHandle = name_first.lower() + name_last.lower() + str((len(INFO["Users"]) + 1))
    newUser = User(userID, email, password, name_first, name_last, newHandle, None, False, None)
# unique handle
    INFO["Users"].append(newUser)
    returnInfo = {
        "u_id": userID,
        "token": None
    }
    return returnInfo
    

def auth_passwordreset_request(email):
    global INFO
    new_Message = Message(1234, 8888, "secret code", datetime.now())
    for user in INFO["Users"]:
        if user.getEmail() == email:
            send_email("BACKENDBOYS@slackr.com", email, new_Message)
            return {}
    raise ValueError("Email does not belong to any user")

def auth_passwordreset_reset(reset_code, new_password):
    global INFO
    for user in INFO["Users"]:
        if len(new_password) < 6:
            raise ValueError("Password entered is not a valid password")
        if user.getSecret() == reset_code:
            user.setPassword(new_password)
            user.setSecret(None)
            return {}
    raise ValueError("reset_code is not a valid reset code")
