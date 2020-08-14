from storage import INFO, User, Channel, Message
import random
"""pulls global storage from storage.py"""
ID = 0

####################################################################
#                          Helper Functions                        #
####################################################################
def search_user_token_in_storage (token):
    global INFO
    for user_token in INFO["Users"]:
        if user_token.getToken() == token:
            return user_token
    raise ValueError("u_id does not refer to a valid user")

def search_user_in_storage (u_id):
    global INFO
    for user in INFO["Users"]:
        if user.getID() == u_id:
            return user
    raise ValueError("Invalid User ID")

def search_channel_in_storage (channel_id):
    global INFO
    for channel in INFO["Channels"]:
        if channel.getChannelID() == channel_id:
            return channel
    raise ValueError("Channel based on ID does not exist")

def generate_channelID ():
    global ID
    rand = random.sample(range(1000,9999), 8999)
    ID += 1
    return rand[ID]

# Invites a user (with user id u_id) to join a channel with ID channel_id.
# Once invited the user is added to the channel immediately
def channel_invite(token, channel_id, u_id):
    global INFO
    user_token = search_user_token_in_storage(token)
    user = search_user_in_storage(u_id)
    channel = search_channel_in_storage(channel_id)
    if user_token not in channel.getMembers():
        raise ValueError("Token user not in channel")
    if user in channel.getMembers():
        raise ValueError("User already in channel")
    channel.addMembers(user)
    return 

def channel_details(channel_id, token):
#Given a Channel with ID channel_id that the authorised user is part of,
# provide basic details about the channel
    global INFO
    channel_det = {}
    channel = search_channel_in_storage(channel_id)
    user_token = search_user_token_in_storage(token)
    #{ u_id, name_first, name_last, profile_img_url }
    channel_det["name"] = channel.getName()
    tempMembers = []
    tempDict = {}
    for member in channel.getMembers():
        tempDict["u_id"] = member.getID()
        tempDict["name_first"] = member.getFirstName()
        tempDict["name_last"] = member.getLastName()
        tempDict["profile_img_url"] = member.getImage()
        tempMembers.append(tempDict.copy())
    tempOwners = []
    for owner in channel.getOwners():
        tempDict["u_id"] = owner.getID()
        tempDict["name_first"] = owner.getFirstName()
        tempDict["name_last"] = owner.getLastName()
        tempDict["profile_img_url"] = owner.getImage()
        tempOwners.append(tempDict.copy())
    channel_det["owner_members"] = tempOwners
    channel_det["all_members"] = tempMembers
    return channel_det

def channel_messages(token, channel_id, start):
#Given a Channel with ID channel_id that the authorised
#user is part of, return up to 50 messages between index "start" and "start + 50".
#Message with index 0 is the most recent message in the channel.
# This function returns a new index "end" which is the value of "start + 50",
#or, if this function has returned the least recent messages in the channel,
# returns -1 in "end" to indicate there are no more messages to load after this return.
    global INFO
    return_msgs = {
        "messages": None,
        "start": None,
        "end": None
    }
    channel_msgs = []
    
    channel = search_channel_in_storage(channel_id)
    members = channel.getMembers()
    for user in members:
        if user.getToken() == token:
            messages = channel.getMessages()
            index = len(messages)
            if index < start:
                raise ValueError("start is greater than the total number of messages in the channel")
            if index - start > 50:
                index = start + 50
            channel_msgs = []
            temp_msg = {}
            for x in range(start, index):
                temp_msg["message_id"] = messages[x].getMessageID()
                temp_msg["u_id"] = messages[x].getUserID()
                temp_msg["message"] = messages[x].getMessage()
                temp_msg["time_created"] = messages[x].getMessageTime()
                temp_msg["reacts"] = messages[x].getReact()
                temp_msg["is_pinned"] = messages[x].getPinned()
                channel_msgs.append(temp_msg.copy())
            #{ message_id, u_id, message, time_created, reacts, is_pinned,  }
            return_msgs["messages"] = channel_msgs
            return_msgs["start"] = start
            return_msgs["end"] = index
            return return_msgs
    raise ValueError("Authorised user is not a member of channel with channel_id")

def channel_leave(token, channel_id):
#Given a channel ID, the user removed as a member of this channel
    channel = search_channel_in_storage(channel_id)
    members = channel.getMembers()
    for user in members:
        if user.getToken() == token:
            members.remove(user)
            return 
    raise ValueError("Invalid Token")

def channel_join(token, channel_id):
#Given a channel_id of a channel that the authorised user can join, adds them to that channel
    global INFO
    channel = search_channel_in_storage(channel_id)
    if channel.getPublic() == True:
        user_token = search_user_token_in_storage(token)
        if user_token in channel.getMembers():
            raise ValueError("User already in channel")
        channel.addMembers(user_token)
        return 

def channel_addowner(token, channel_id, u_id):
    global INFO
    user_token = search_user_token_in_storage(token)
    if user_token.getPermission == 3:
        raise ValueError("User with token does not have permission to make owners.")
    channel = search_channel_in_storage(channel_id)
    for user in channel.getMembers():
        if user.getID() == u_id:
            for owner in channel.getOwners():
                if user == owner:
                    raise ValueError("Member is already an owner")
            channel.addOwner(user)
            user.setPermission(1)
            return 
    raise ValueError ("User with u_id does not exist in this channel")

def channel_removeowner(token, channel_id, u_id):
#Remove user with user id u_id an owner of this channel
    global INFO
    channel = search_channel_in_storage(channel_id)
    for owner in channel.getOwners():
        if owner.u_id == u_id:
            channel.getOwners().remove(owner)
            return 
    raise ValueError("This user is not an owner of this channel")

def channels_list(token):
#Provide a list of all channels (and their associated details) that the authorised user is part of
    global INFO
    channelList = []
    channelTemp = {}
    for channel in INFO["Channels"]:
        for member in channel.getMembers():
            if member.getToken() == token:
                channelTemp["channel_id"] = channel.getChannelID()
                channelTemp["name"] = channel.getName()
                channelList.append(channelTemp.copy())
                break
    return channelList

def channels_listall(token):
#Provide a list of all channels (and their associated details)
    channelsList = []
    global INFO
    channelTemp = {}
    for channel in INFO["Channels"]:
        channelTemp["channel_id"] = channel.getChannelID()
        channelTemp["name"] = channel.getName()
        channelsList.append(channelTemp.copy())
    return channelsList

def channels_create(privacy_setting, name, token):
#Creates a new channel with that name that is either a public or private channel
    global INFO
    global ID
    user_token = search_user_token_in_storage(token)
    channelID = generate_channelID()
    channel = Channel(channelID, name, [], [], [], privacy_setting, False, [])
    channel.addOwner(user_token)
    channel.addMembers(user_token)
    INFO["Channels"].append(channel)
    return channelID


