import itertools

INFO = {
    "Users" : [],
    "Channels" : [],
    "Messages" : [],
    "Admins" : []
}

class User:
    def __init__(self, u_id, email, password, name_first, name_last, handle_str, token, auth, secret):
        self.u_id = u_id
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = handle_str
        self.token = token
        self.auth = False
        self.secret = None
        self.permission_id = None
        self.image_url = None
    def getID (self):
        return self.u_id
    def getEmail (self):
        return self.email
    def getPassword (self):
        return self.password
    def getFirstName (self):
        return self.name_first
    def getLastName (self):
        return self.name_last
    def getHandle (self):
        return self.handle_str
    def getToken (self):
        return self.token
    def getIsAuth (self):
        return self.auth
    def getSecret (self):
        return self.secret
    def getPermission (self):
        return self.permission_id
    def getImage (self):
        return self.image_url
    def setID (self, u_id):
        self.u_id = u_id
    def setEmail (self, email):
        self.email = email
    def setPassword (self, password):
        self.password = password
    def setFirstName (self, name_first):
        self.name_first = name_first
    def setLastName (self, name_last):
        self.name_last = name_last
    def setHandle (self, handle_str):
        self.handle_str = handle_str
    def setToken (self, token):
        self.token = token
    def setAuth (self, isAuth):
        self.auth = isAuth
    def setSecret (self, secret):
        self.secret = secret
    def setPermission (self, permission_id):
        self.permission_id = permission_id
    def setImage (self, image_url):
        self.image_url = image_url

class Channel:
    def __init__ (self, channel_id, name, owner_members, all_members, messages, is_public, standup, standupMessages):
        self.channel_id = channel_id
        self.name = name
        self.owner_members = owner_members
        self.all_members = all_members
        self.messages = messages
        self.is_public = is_public
        self.standup = False
        self.standupMessages = []
        self.standuptime = {
            "start": None,
            "end": None
        }
        self.standupMessages = []
    def getChannelID (self):
        return self.channel_id
    def getName (self):
        return self.name
    def getOwners (self):
        return self.owner_members
    def getMembers (self):
        return self.all_members
    def getMessages (self):
        return self.messages
    def getPublic (self):
        return self.is_public
    def getStandUp (self):
        return self.standup
    def getStandUpTime (self):
        return self.standuptime
    def getStandUpMsg(self):
        return self.standupMessages
    def setChannelID (self, channel_id):
        self.channel_id = channel_id
    def setName (self, name):
        self.name = name
    def addOwner (self, owner_member):
        self.owner_members.append(owner_member)
    def addMembers (self, member):
        self.all_members.append(member)
    def addMessages (self, message):
        self.messages.append(message)
    def setPublic (self, is_public):
        self.is_public = is_public
    def setStandUp (self, standup):
        self.standup = standup
    def setStandUpTime (self, time_start, time_end):
        self.standuptime = {
            "start": time_start,
            "end": time_end
        }
    def addStandup (self, message):
        self.standupMessages.append(message)


class Message:
    def __init__ (self, message_id, u_id, message, time_sent):
        self.message_id = message_id
        self.u_id = u_id
        self.message = message
        self.time_sent = time_sent
        self.is_unread = True
        self.react = []
        self.pinned = False
    def getMessageID (self):
        return self.message_id
    def getUserID (self):
        return self.u_id
    def getMessage (self):
        return self.message
    def getMessageTime (self):
        return self.time_sent
    def getRead (self):
        return self.is_unread
    def getReact (self):
        return self.react
    def getPinned (self):
        return self.pinned
    def setMessageID (self, message_id):
        self.message_id = message_id
    def setUserID (self, u_id):
        self.u_id = u_id
    def setMessage (self, message):
        self.message = message
    def setMessageTime (self, time_sent):
        self.time_sent = time_sent
    def setRead (self, is_unread):
        self.is_unread = is_unread
    def addReact (self, react):
        self.react.append(react)
    def setPinned (self, pinned):
        self.pinned = pinned

