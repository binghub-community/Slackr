from storage import *
import random
from datetime import datetime

count = 0

#################################################################
#                      Helper function                          #
#################################################################

def isempty_message (message):
#    if empty message return true
    if(not (message and message.strip())):
        return True
    return False

def generate_MID ():
    global count
    message_id = random.sample(range(0,10000),10000)
    count += 1
    return message_id[count]

def validate(date_text):
    count = 0
    if (2000 <= date_text.year <= 3000) == True:
#        print("success1")
        count += 1
    if (1 <= date_text.month <= 12) == True:
#        print("success2")
        count += 1
    if (1 <= date_text.day <= 31) == True:
#        print("success3")
        count += 1
    if (0 <= date_text.hour <= 24) == True:
#        print("success4")
        count += 1
    if (0 <= date_text.minute <= 60) == True:
#        print("success5")
        count += 1
    if (0 <= date_text.second <= 60) == True:
#        print("success6")
        count += 1
    if count == 6:
#        print("functon works")
        return True
    else:
        raise ValueError("Time is invalid")
    
def is_message_legit (message,token,channel_id,time):

    if isempty_message (message) == True:
        raise ValueError("Empty message")
    if isempty_message (token) == True:
        raise ValueError("Invalid Token")
    if len(message) > 1000:
        raise ValueError("Message length exceeds 1000 characters")
    find_channel_ID(channel_id)
    validate(time)
    return 

def find_user_token(token):
    for user in INFO["Users"]:
        if user.getToken() == token:
            return user
    raise ValueError("Invalid token")

def find_user_ID(user_id):
    for user in INFO["Users"]:
        if user.getID() == user_id:
            return user
    raise ValueError("User with ID does not exist")

def find_channel_ID(channel_id):
    for channel in INFO["Channels"]:
        if channel.getChannelID() == channel_id:
            return channel
    raise ValueError("Invalid channel_id")
    
    
########################################################

def message_sendlater(message, token, channel_id, time):
#Send a message from authorised_user to the channel specified by channel_id automatically at a specified time in the future
    global INFO

    user = find_user_token(token)
    channel = find_channel_ID(channel_id)

    message_id = generate_MID()
    newMessage = Message(message_id, user.getID(), message, time)
    channel.addMessages(newMessage)

    is_message_legit(message, token, channel_id, time)
    return message_id
    
def message_send(message, token, channel_id):
#Send a message from authorised_user to the channel specified by channel_id
    global INFO

    user = find_user_token(token)
    message_id = generate_MID()
    time = datetime.now()

    is_message_legit(message, token, channel_id, time)
    newMessage = Message(message_id, user.getID(), message, time)
      
    channel = find_channel_ID(channel_id)
    if user not in channel.getMembers():
        raise ValueError("User is not in channel")

    channel.addMessages(newMessage)
    return message_id

def message_remove(message_id, token):
#Given a message_id for a message, this message is removed from the channel
    global INFO
   
    user = find_user_token(token)

    for channel in INFO["Channels"]:
        for message in channel.getMessages():
            if message.getMessageID() == message_id:
                channel.getMessages().remove(message)
                return 
    raise ValueError("Invalid message_id")

def message_edit(message_id, message, token):
#Given a message, update it's text with new text
    global INFO
    user = find_user_token(token)
    if isempty_message(message) == False:
        empty = True
    for channel in INFO["Channels"]:
        for msg in channel.getMessages():
            if msg.getMessageID() == message_id:
                if user.getID() == msg.getUserID() or user in channel.getOwners() or user in INFO["Admins"]:
                    if isempty_message(message) == True:
                        channel.getMessages().remove(msg)
                    else:
                        msg.setMessage(message)
                    return 
    raise ValueError("Message does not exist")

def message_react(message_id, token, react_id):
#Given a message within a channel the authorised user is part of, add a "react" to that particular message
    global INFO
    user = find_user_token(token)
    for channel in INFO["Channels"]:
        if user in channel.getMembers():            
            for message in channel.getMessages():
                if message.getMessageID() == message_id:
                    for react in message.getReact():
                        if react == react_id:
                            raise ValueError("Message with ID message_id already contains an active React with ID react_id")
                    message.addReact(react_id)
                    return 
    raise ValueError("Message does not exist")

def message_unreact(message_id, token, react_id):
#Given a message within a channel the authorised user is part of, remove a "react" to that particular message
    global INFO
    user = find_user_token(token)
    for channel in INFO["Channels"]:
        if user in channel.getMembers():
            for message in channel.getMessages():
                if message.getMessageID() == message_id:
                    for react in message.getReact():
                        if react == react_id:
                            message.react.remove(react_id)
                            return 
                    raise ValueError("Message with ID message_id does not contain an active React with ID react_id")               
    raise ValueError("Message does not exist")
    
def message_pin(message_id, token):
#Given a message within a channel, mark it as "pinned" to be given special display treatment by the frontend
    global INFO

    user = find_user_token(token)
    if user not in INFO["Admins"]:
        raise ValueError("Authorised user is not an admin")
    for channel in INFO["Channels"]:
        for message in channel.getMessages():
            if message.getMessageID() == message_id:
                if user not in channel.getMembers():
                    raise ValueError("AccessError")
                if message.getPinned() == True:
                    raise ValueError("Message is already pinned")
                message.setPinned(True)
                return 
    raise ValueError("Message does not exist")
    
def message_unpin(message_id, token):
#Given a message within a channel, remove it's mark as unpinned
    global INFO
    user = find_user_token(token)
    if user not in INFO["Admins"]:
        raise ValueError("Authorised user is not an admin")
    for channel in INFO["Channels"]:
        for message in channel.getMessages():
            if message.getMessageID() == message_id:
                if user not in channel.getMembers():
                    raise ValueError("AccessError")
                if message.getPinned() == False:
                    raise ValueError("Message is already unpinned")
                message.setPinned(False)
                return 
    raise ValueError("Message does not exist")