Briefly describe the strategies you followed and tools you used to achieve this in assurance.md.

Our backend implementation comprised of 3 sections. The storage space required to store the data globally for the various variables, the functions required to manipulate the data to achieve our goals and the connection to the frontend required to provide a bridge between the frontend and the backend. 

Our storage space was built upon a dictionary with 3 lists. "Users", "Channels", "Messages". Within each of these lists, elements will be stored as Classes. 

User classes have the following parameters:
u_id, email, password, name_first, name_last, handle_str, token, auth, secret
where auth is a boolean for authorised users and secret is a string for the code that will be used to verify a password reset. 

Chanenl classes have the following parameters:
channel_id, name, owner_members, all_members, messages, is_public, standup,standUpMessages
where standup is a boolean for whether a standup is active, and standUpMessages store the messages sent during the standup in the form of a list. 

Message classes have the following parameters:
message_id, u_id, message, time_sent, is_unread, react, pinned
where react is a list of "reacts" on the message, and pinned is a boolean for whether the message is pinned in the channel.

Verification and Validation

Verification and validation were handled through our token parameter within each user. When logged in, users will receive a token, with which they can gain permission to perform certain actions across the app. Examples include editing user information and profile, obtaining channel details and inviting people to channels, editing messages and more. These actions were approved or rejected depending on whether that token permitted such an action. This ties into our acceptance criteria, of which states that only active and valid users should be able to perform actions according to their permissions. We also implemented a parameter, user.auth, a boolean for whether a user is logged in or not, but didn't get used due to the way we handled tokens. When a user logs in, a token is generated. When a user logs out, the token is set to None. Through these methods, we were able to validate certain users for certain actions and also verify whether they have been validated for those actions or not. 


We made sure our code worked through various means. Our primary method of testing functions was through the Postman API. We would input many different variables through the mock server, and checked the outputs to show what was required. This was a very fun and rewarding method of testing as it was more than just staring at the terminal all the time. Futhermore, it was satisfying to see our functions get implemented onto an actual server. 
All of our group members installed pylint to test our style and to make sure our code was compiling at real time. It did a superb job and increased our productivity massively, reminding us of the syntax errors in a language we had just picked up this semester. This along with the communication throughout the group, allowed for quick and easy fixes. 
Finally, we utilised pytests to test our functions locally. Pytests were already built during our iteration 1, however these had to be edited for iteration 2 as we had changed the way we handled data. This was a more difficult way to test as we had to build new users and reset our global variable at the correct places and was very confusing to work with in the beginning. However it provided a way to test locally, especially helpful during certain periods of time where flask was not working on some of our devices (which we fixed eventually). Building our inputs and asserting our outputs, we were able to test our individual functions and fix any edge cases which we might have missed. 