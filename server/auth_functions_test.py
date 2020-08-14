import pytest
from auth_functions import *
from storage import INFO, User, Channel, Message

def test_auth_login ():
#Given a registered users' email and password and generates a valid token for the user to remain authenticated
    fail_mail = "email"
    fail_pass = "pass"
    auth_register("email@email.com", "password", "jeff", "flintstones")
    auth_login("email@email.com", "password")
    auth_register("kath@notkath.com", "kathspassword","kath","notkath")
    auth_login("kath@notkath.com", "kathspassword")
    auth_register("hazza@gmail.com", "hazzaPass", "hazza", "mazza")
#not valid email
    with pytest.raises(ValueError):
        auth_login(fail_mail, fail_pass)
#email not found
    with pytest.raises(ValueError):
        auth_login("wrongemail@email.com", "password")
#wrong password
    with pytest.raises(ValueError):
        auth_login("email@email.com", "wrongpassword")
        
    assert INFO["Users"][0].getIsAuth() == True
    assert INFO["Users"][1].getIsAuth() == True
    assert INFO["Users"][2].getIsAuth() == False
    assert INFO["Users"][2].getToken() == None
    return

def test_auth_logout ():
#Given an active token, invalidates the token to log the user out. Given a non-valid token, does nothing
    global INFO
    INFO["Users"] = []
    auth_register("hazza@gmail.com", "hazzaPass", "hazza", "mazza")
    auth_login("hazza@gmail.com", "hazzaPass")
    hazza = INFO["Users"][0]
    auth_logout(hazza.getToken())
    assert INFO["Users"][0].getIsAuth() == False
    assert INFO["Users"][0].getToken() == None

    return

def test_auth_register ():
#Given a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their sessiong
    global INFO
    INFO["Users"] = []
    auth_register("kath@email.com", "kathhh123", "kath", "han")
    INFO["Users"][0].setToken(69)
    INFO["Users"][0].setID(420)
    fail_firstname = "jeffjeffjeffjeffjeffjeffjeffjeffjeffjeffjeffjeffjeff" 
    fail_lastname = "flintstonesflintstonesflintstonesflintstonesflintstones"
    assert INFO["Users"][0].getPassword() == "kathhh123"
    assert INFO["Users"][0].getFirstName() == "kath"
    assert INFO["Users"][0].getLastName() == "han"
    assert INFO["Users"][0].getEmail() == "kath@email.com"
    
#email address already being used
    with pytest.raises(ValueError):
        auth_register("kath@email.com", "password", "jeff", "flintstones")
#first name more than 50 chars
    with pytest.raises(ValueError):
        auth_register("fmail@email.com", "password", fail_firstname , "flintstones")
#last name more than 50 chars
    with pytest.raises(ValueError):
        auth_register("fmail@email.com", "password", "jeff" , fail_lastname)
    return

def test_auth_passwordreset_request ():
#Given an email address, if the user is a registered user, send's them a an email containing a specific secret code, that when entered in auth_passwordreset_reset, shows that the user trying to reset the password is the one who got sent this email
    global INFO
    INFO["Users"] = []
    auth_register("marvin@gmail.com", "marvinPass", "marvin", "yu")
    marvin = INFO["Users"][0]
    auth_register("kath@gmail.com", "kathPass", "kath", "han")
    kath = INFO["Users"][1]
    auth_register("hazzamazza@gmail.com", "hazzaPass", "hazza", "mazza")
    hazza = INFO["Users"][2]

    with pytest.raises(ValueError):
        auth_passwordreset_request("loser@loserland.com")

    return

def test_auth_passwordreset_reset ():
#Given a reset code for a user, set that user's new password to the password provided
    global INFO
    INFO["Users"] = []
    auth_register("loser96@gmail.com", "loserPass", "holy", "moly")
    loser = INFO["Users"][0]
    
#not valid password
    with pytest.raises(ValueError):
        auth_passwordreset_reset(loser.getSecret(), "short")
#invalid reset code
    with pytest.raises(ValueError):
        auth_passwordreset_reset("wrong secret", loser.getPassword())
#check function passed
    auth_passwordreset_reset(loser.getSecret(), "newLoserPass")
    assert loser.getSecret() == None
    assert loser.getPassword() == "newLoserPass"

    return
