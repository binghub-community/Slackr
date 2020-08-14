import pytest
from channel_functions import *
from auth_functions import *
from message_functions import *
from storage import INFO, User, Channel, Message

auth_register("harry@gmail.com", "harry123", "harry", "park")
auth_register("marvin@gmail.com", "marvin123", "marvin", "yu")
auth_register("kath@gmail.com", "kath123", "kath", "han")
harry = INFO["Users"][0]
marvin = INFO["Users"][1]
kath = INFO["Users"][2]

auth_login(harry.getEmail(), harry.getPassword())
auth_login(marvin.getEmail(), marvin.getPassword())
auth_login(kath.getEmail(), kath.getPassword())

#auth_register("james@gmail.com", "james123", "james", "jun")
#INFO["Users"][3].setToken(80)
#print(INFO["Users"][0].getID())
#print(INFO["Users"][1].getID())
#print(INFO["Users"][2].getID())
#print(INFO["Users"][3].getID())


def clear_INFO ():
    global INFO
    INFO = {
        "Users" : [],
        "Channels" : [],
        "Messages" : []
    }
    return


def test_database_build ():
    global INFO
    general = channels_create(True, "general channel", harry.getToken())
    cool = channels_create(True, "cool channel", harry.getToken())
    lame = channels_create(True, "lame channel", harry.getToken())
    empty = channels_create(True, "empty channel", harry.getToken())
    print("!!!!!", INFO)
    with pytest.raises(ValueError):
        channel_invite(harry.getToken(), general, "wronguid")
    channel_invite(harry.getToken(), general, kath.getID())
    return


def test_channel_invite():
#Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited the user is added to the channel immediately
    INFO["Channels"] = []
    channel = channels_create(True, "holy channel", marvin.getToken())
    channel_invite(marvin.getToken(), channel, harry.getID())
    members = INFO["Channels"][0].getMembers()
    print(INFO)
    print(marvin.getID())
    print(harry.getID())
    assert members[0].getID() == marvin.getID()
    assert members[1].getID() == harry.getID()
    with pytest.raises(ValueError):
        channel_invite(marvin.getToken(), "wrong channel_id", harry.getID())
    with pytest.raises(ValueError):
        channel_invite(-1, " ", -1)
    with pytest.raises(ValueError):
        channel_invite(marvin.getToken(), "holy channel", -1) 
    return

def test_channel_details():
#Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel
    global INFO
    INFO["Channels"] = []
    channelID = channels_create(True, "harry's channel", harry.getToken())
    assert channel_details(channelID, harry.getToken()) == {
        "name": "harry's channel",
        "owner_members": [{
            "u_id": harry.getID(),
            "name_first": harry.getFirstName(),
            "name_last": harry.getLastName(),
            "profile_img_url": harry.getImage()
        }],
        "all_members": [{
            "u_id": harry.getID(),
            "name_first": harry.getFirstName(),
            "name_last": harry.getLastName(),
            "profile_img_url": harry.getImage()
        }]
    }
    with pytest.raises(ValueError):
        channel_details(" ", -1)
    with pytest.raises(ValueError):
        channel_details("harry's channel", 0)
    with pytest.raises(ValueError):
        channel_details("not a channel", 0)
    return

def test_channel_messages():
#Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". 
#Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", 
# or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.
    INFO["Channels"] = []
    channels_create(True, "harry's channel", harry.getToken())
    INFO["Channels"][0].setChannelID(1000)
    message_send("peepee", harry.getToken(), 1000)
    print(channel_messages(harry.getToken(), 1000, 0))
#   start is greater than total no. msgs in chnnl error
    with pytest.raises(ValueError):
        channel_messages(harry.getToken(), 1000, 50)
#   authorised user not member of channnel
    with pytest.raises(ValueError):
        channel_messages("asda", 1, 0)
    with pytest.raises(ValueError):
        channel_messages(-1, 1, 0)
    with pytest.raises(ValueError):
        channel_messages(" ", 1, 0)
    with pytest.raises(ValueError):
        channel_messages(harry.getToken(), 1, -50)

def test_channel_leave():
#Given a channel ID, the user removed as a member of this channel
    #global INFO
    INFO["Channels"] = []
    channel = channels_create(True, "dumb channel", marvin.getToken())
    channel_join(harry.getToken(), channel)
    assert INFO["Channels"][0].getMembers() == [marvin, harry]
    channel_leave(harry.getToken(), channel)
    assert INFO["Channels"][0].getMembers() == [marvin]
    with pytest.raises(ValueError):
        channel_leave("wrong_token",channel)
    with pytest.raises(ValueError):
        channel_leave(harry.getToken(),-1)
    return

def test_channel_join():
#Given a channel_id of a channel that the authorised user can join, adds them to that channel
    global INFO
    INFO["Channels"] = []
    channel_id = channels_create(True, "notMarvin's channel", kath.getToken())
    channel_join(marvin.getToken(), channel_id)
    assert INFO["Channels"][0].getMembers() == [kath, marvin]
    channel_join(harry.getToken(), channel_id)
    assert INFO["Channels"][0].getMembers() == [kath, marvin, harry]
    with pytest.raises(ValueError):
        channel_join(kath.getToken(), "invalid channel_id")
    with pytest.raises(ValueError):
        channel_join(-1, "notMarvin's channel")
    return

def test_channel_addowner():
#Make user with user id u_id an owner of this channel
    #global INFO
    hazza = harry.getID()
    mervin = marvin.getID()
    channel_id = channels_create(True, "Disney's channel", kath.getToken())
    channel_join(harry.getToken(), channel_id)
    channel_join(marvin.getToken(), channel_id)
    channel_addowner(harry.getToken(), channel_id, hazza)
    channel_addowner(marvin.getToken(), channel_id, mervin)
    with pytest.raises(ValueError):
        channel_addowner(marvin.getToken(), channel_id, mervin)
    with pytest.raises(ValueError):
        channel_addowner(marvin.getToken(), "invalid channel_id", harry.getID())
    with pytest.raises(ValueError):
        channel_addowner(19000, channel_id, "bobs")

    return

def test_channel_removeowner():
#Remove user with user id u_id an owner of this channel
    INFO["Channels"] = []
    channel_id = channels_create(True, "cool channel", harry.getToken())
    channel_join(marvin.getToken(), channel_id)
    channel_addowner(harry.getToken(), channel_id, marvin.getID())
    channel_removeowner(harry.getToken(), channel_id, marvin.getID())
    with pytest.raises(ValueError):
        channel_removeowner(marvin.getToken(), channel_id, "kaaaath")
    with pytest.raises(ValueError):
        channel_removeowner(marvin.getToken(), "invalid channel_id", marvin.getID())
    with pytest.raises(ValueError):
        channel_removeowner(harry.getToken(), channel_id, marvin.getID())
    return

def test_channels_list():
#Provide a list of all channels (and their associated details) that the authorised user is part of
    INFO["Channels"] = []
    harryC = channels_create(True, "harry's channel", harry.getToken())
    marvinC = channels_create(True, "marvin's channel", harry.getToken())
    kathC = channels_create(True, "kath's channel", harry.getToken())
    jamesC = channels_create(True, "james's channel", harry.getToken())
    channel_join(marvin.getToken(), marvinC)
    channel_join(marvin.getToken(), jamesC)
    marvin_list = channels_list(marvin.getToken())
    print(marvin_list)
    assert marvin_list == [{
        "channel_id": marvinC,
        "name": "marvin's channel"
    },{
        "channel_id": jamesC,
        "name": "james's channel"
    }]
    return

def test_channels_listall():
#Provide a list of all channels (and their associated details)
    INFO["Channels"] = []
    assert channels_listall(harry.getToken()) == []
    marvinC = channels_create(True, "marvin's channel", harry.getToken())
    INFO["Channels"][0].setChannelID(2247)
    assert channels_listall(harry.getToken()) == [{'channel_id': 2247, 'name': "marvin's channel"}]
    kathC = channels_create(True, "kath's channel", harry.getToken())
    INFO["Channels"][1].setChannelID(2250)
    assert channels_listall(harry.getToken()) == [{'channel_id': 2247, 'name': "marvin's channel"}, {'channel_id': 2250, 'name': "kath's channel"}]
    assert channels_listall(harry.getToken()) != []
    channels_list(harry.getToken())
    return

def test_channels_create():
#Creates a new channel with that name that is either a public or private channel
    global INFO
    INFO["Channels"] = []
    print(INFO)
    print(harry.getToken())
    channelID = channels_create(True, "harry's channel", harry.getToken())
    with pytest.raises(ValueError):
        channels_create(True, "notaChannel", 1)
    with pytest.raises(ValueError):
        channels_create(False, "notaChannel", -1)

    assert INFO["Channels"][0].getChannelID() == channelID
    assert INFO["Channels"][0].getName() == "harry's channel"
    assert INFO["Channels"][0].getPublic() == True
    return
    
    
