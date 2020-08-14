import pytest
from message_functions import *
from auth_functions import *
from channel_functions import *
from storage import *
from datetime import *

auth_register("jeff@email.com", "password", "jeff", "flintstones")
auth_login("jeff@email.com", "password")
auth_register("kath@notkath.com", "kathspassword","kath","notkath")
auth_login("kath@notkath.com", "kathspassword")
auth_register("hazza@notkath.com", "hazzapassword","hazza","mazza")
auth_login("hazza@notkath.com", "hazzapassword")

jeff = INFO["Users"][0]
kath = INFO["Users"][1]
hazza = INFO["Users"][2]
INFO["Admins"].append(jeff)
jeffChannelID = channels_create(True, "jeff's channel", jeff.getToken())
channel_join(kath.getToken(), jeffChannelID)

def test_message_sendlater ():
    time  = datetime.now() + timedelta(days=3)
    message = "hi"
    channel_id = jeffChannelID
    token = jeff.getToken()
    message_sendlater("laters", token, channel_id, time)
    assert INFO["Channels"][0].messages[0].getMessageTime() == time
    with pytest.raises(ValueError):
        message_sendlater("", token, channel_id, time)
    with pytest.raises(ValueError):
        message_sendlater(message, "wrong token", channel_id, time)
    with pytest.raises(ValueError):
        message_sendlater(message, token, "wrong channel_id", time)
    with pytest.raises(ValueError):
        message_sendlater(message, token, channel_id, datetime(1999,1,1,5,30,11,10))
    INFO["Channels"][0].messages = []
    return

def test_message_send ():
    message = "send it"
    message_send(message, jeff.getToken(), jeffChannelID)
    assert INFO["Channels"][0].getMessages()[0].getMessage() == "send it"

    with pytest.raises(ValueError):
        message_send(message, hazza.getToken(), jeffChannelID)
    message = "deathhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
    with pytest.raises(ValueError):
        message_send(message, jeff.getToken(), jeffChannelID)
    INFO["Channels"][0].messages = []
    return

def test_message_remove ():
    message_id = message_send("clutch", jeff.getToken(), jeffChannelID)

    message_remove(message_id, jeff.getToken())
    assert INFO["Channels"][0].getMessages() == []

    message_send("chrissy", jeff.getToken(), jeffChannelID)
    with pytest.raises(ValueError):
        message_remove(message_id, kath.getToken())
    INFO["Channels"][0].messages = []
    return

def test_message_edit ():
    message_id = message_send("message", jeff.getToken(), jeffChannelID)
#    message does not exist
    message_edit(message_id, "new message", jeff.getToken())
    assert INFO["Channels"][0].getMessages()[0].getMessage() == "new message"
    with pytest.raises(ValueError):
        message_edit(message_id, "imposter message edit", kath.getToken())

    message_edit(message_id, "", jeff.getToken())
    assert INFO["Channels"][0].getMessages() == []
    INFO["Channels"][0].messages = []
    return

def test_message_react ():
    message_id = message_send("again", jeff.getToken(), jeffChannelID)
    message_react(message_id, jeff.getToken(), "haha")
    message_react(message_id, kath.getToken(), "lame")
    assert INFO["Channels"][0].getMessages()[0].getReact() == ["haha", "lame"]
    with pytest.raises(ValueError):
        message_react(message_id, hazza.getToken(), "same")
    INFO["Channels"][0].messages = []
    return

def test_message_unreact ():
    message_id = message_send("haha hello", jeff.getToken(), jeffChannelID)
    message_react(message_id, jeff.getToken(), "not funny")
    message_react(message_id, kath.getToken(), "love")
    message_unreact(message_id, kath.getToken(), "love")
    assert INFO["Channels"][0].getMessages()[0].getReact() == ["not funny"]
    with pytest.raises(ValueError):
        message_unreact(message_id, kath.getToken(), "love")
    INFO["Channels"][0].messages = []
    return

def test_message_pin ():
    message_id = message_send("haha hello", jeff.getToken(), jeffChannelID)
    message_pin(message_id, jeff.getToken())
    assert INFO["Channels"][0].getMessages()[0].getPinned() == True
    with pytest.raises(ValueError):
        message_pin(message_id, jeff.getToken())
    message_id = message_send("i want this pinned !", kath.getToken(), jeffChannelID)
    with pytest.raises(ValueError):
        message_pin(message_id, kath.getToken())
    INFO["Channels"][0].messages = []
    return

def test_message_unpin ():
    message_id = message_send("goodbye dummys", jeff.getToken(), jeffChannelID)
    message_pin(message_id, jeff.getToken())
    message_unpin(message_id, jeff.getToken())
    assert INFO["Channels"][0].getMessages()[0].getPinned() == False
    with pytest.raises(ValueError):
        message_unpin(message_id, jeff.getToken())
    INFO["Channels"][0].messages = []
    return
