# Refactoring 
We refactored to improve our engineering software design and to aim for these following attributes
  - Easier to test, design 
  - Extensible 
  - Reusable
  - Maintainable
  - Understandable
  - Testable

# Good Software Engineering Design
A summary of the principles we used to refactor our code for iteration 2 is listed below 
  
##### DRY - "Don't repeat yourself"
 In iteration 2 a lot of code was repeated in all functions to iterate through and confirm that the input values were within our global storage. Therefore we decided to include helper functions within each file (user, channel, message, authentication) so that helper functions could be reused for each feature and therefore we would avoid copying and pasting the same for loops, if statements and raised value Errors. 
  - Each Channel function - search for Value Errors 
  - Avoids space + avoid errors 

##### KISS - "Keep it Simple Stupid"
  - Used it the KISS methodology by removing complicated for-if-for-if statements
  - Used to avoid complex naming conventions and made variable names as coherent as possible
  - Removed 3 for loops with if statements 
  - Removed nested loops and nested if statements and combined if statements where possible

##### Encapsulation
- Encapsulation was used in our project to maintain type abstraction and restrict direct access to the classes
- We applied this software principle by creating get and set functions in each of our classes in storage.py 
- Encapsulation was already implemented in iteration 2 which meant this was not refactoring during this iteration.

##### Top down Thinking
- General high level was identified in Iteration 1
- Created epics and user stories within each category
- Started creating functions for each feature required in User Stories in iteration 2

### Changes Implemented 
Original Code
```py
def auth_passwordreset_reset(reset_code, new_password):
    global INFO
    for user in INFO["Users"]:
        if user.getSecret() == reset_code:
            if len(new_password) < 6:
                raise ValueError("Password entered is not a valid password")
            user.setPassword(new_password)
            return
    raise ValueError("reset_code is not a valid reset code")
```
Refactored code
> Removed nested if statement to make the code easier to test
```py
def auth_passwordreset_reset(reset_code, new_password):
    global INFO
    for user in INFO["Users"]:
        if len(new_password) < 6:
            raise ValueError("Password entered is not a valid password")
        if user.getSecret() == reset_code:
            user.setPassword(new_password)
            user.setSecret(None)
            return
    raise ValueError("reset_code is not a valid reset code")
```
Created helper functions in channel_functions.py user_functions.py and message_functions.py
- For example:
```py
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
```
> These helper functions were created to avoid repeating code (Each function needs to check for ValueErrors)
> Called within each function for each feature to create reusable code
> Created detailed function names to minimise commenting the purpose of each function
> Some for loop checks were not created into helper functions
    - If for loop was only used once in that file and only specific to that particular function. 
> As that specific feature function required a specific for loop, it would reduce readability if a helper function was created
> Modular and Maintainable if a newer feature is to be added

Some of the modified functions and their changes are mentioned below.

Original: 
```py
def channel_invite(token, channel_id, u_id):
    global INFO
    for user in INFO["Users"]:
        user_token = user.getToken()
        if user_token == token:
            for userChange in INFO["Users"]:
                if userChange.getID() == u_id:
                    for channel in INFO["Channels"]:
                        if channel.getChannelID() == channel_id:
                            channel.addMembers(user)
                            return
                    raise ValueError("channel_id does not refer to a valid channel that the authorised user is part of.")
            raise ValueError("Invalid Token")
```

Refactored:
> Changes made include:
> Called Helper functions to remove nested if and for statements, improve readability and understand
> Reduced time complexity and removed redundant variable names e.g. "user_token = user.getToken()"
> Both names are readable so might as well remove the unnecessary variable
```py
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
```
Original:
```py
def channel_removeowner(token, channel_id, u_id):
    global INFO
    for channel in INFO["Channels"]:
        if channel.getChannelID() == channel_id:
            owners = channel.getOwners()
            for owner in owners:
                if owner.u_id == u_id:
                    owners.remove(owner)
                    return
            raise ValueError("This user is not an owner of this channel")
    raise ValueError("Channel does not exist")
```
Refactored:
> included helper functions to reuse code, remove repeated for and if loops, allow modularity, can be reused if new features are to be added
> removed and renamed variable names to maintain consistency and understandable e.g. removed variable owners to avoid (for owner in owners)
> removed comments and raised errors. Ideally allow variable names to explain the code so that no commenting is needed
```py
def channel_removeowner(token, channel_id, u_id):
    global INFO
    channel = search_channel_in_storage(channel_id)
    for owner in channel.getOwners():
        if owner.u_id == u_id:
            channel.getOwners().remove(owner)
            return 
    raise ValueError("This user is not an owner of this channel")
```
Other channel functions were edited similarly in this way by including helper functions and removing unnecessary variable and renamed variable names to minimise comments
Original:
```py
def message_sendlater(message, token, channel_id, time):
#Send a message from authorised_user to the channel specified by channel_id automatically at a specified time in the future
    global INFO
    u = None
    for user in INFO["Users"]:
        if user.getToken() == token:
            u = user
            break
    c = None
    for channel in INFO["Channels"]:
        if channel.getChannelID() == channel_id:
            c = channel
            break
    message_id = generate_MID(token, channel_id)
    newMessage = Message(message_id, u.getID(), message, time)
    c.addMessages(newMessage)
    if isempty_message(message) == True:
        return False
    if isempty_message(token) == True:
        return False
    if channel_id < 1000:
        return False
    if time < 0:
        return False
    return True
```
Refactored:
> Included helper functions to allow modularity, can be reused if new features are to be added
> changed variable names to more meaningful variable names to maintain readability
```py
def message_sendlater(message, token, channel_id, time):
    global INFO
    user = find_user_token(token)
    channel = find_channel_ID(channel_id)
    message_id = generate_MID()
    newMessage = Message(message_id, user.getID(), message, time)
    channel.addMessages(newMessage)
    is_message_legit(message, token, channel_id, time)
    return message_id
```
In messages most functions were edited by including the helper functions to reduce reused code.