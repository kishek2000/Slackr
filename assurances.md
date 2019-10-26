# Verification - understanding whether the system has been built right

To ensure that the system has been built right, each function has been extensively tested to ensure that it is acting the way it is intended to. Our method that allowed for extensive unit testing used was the coverage testing method; by running the command

_“python3-coverage run --branch --source=. -m pytest”_

This command checks how much of the code has been executed by the tests. The added tag of “--branch” also ensures that each decision point is executed at least once (eg True and False cases of If statements). Our aim was to make our core function tests have a coverage of 100%.
For our channel_functions, some of the partial branch errors which were pointed out, we deemed to be inefficient to solve ‘for the sake of coverage’, and thereby left it as is. 
The other form of testing that was used was a form of integration testing via the front-end. This black box testing method allowed us to analyse and ensure that the function flask implementation has been coded correctly; allowing for the front-end and the back-end functions to communicate. This front-end testing also allowed us to ensure our functions were properly working as intended. Not all functions were able to be tested using the front end, for example standup has yet to be implemented in the frontend, so we were limited to curl/postman testing and coverage testing.
Within our frontend testing process, we utilised the inspect element features to understand the responses and params given by each of the HTTP requests within the server, to then check whether they were working in a way that is given in the spec and also understood/desired by us. This further allowed to enhance our debugging process and be clear on what to change/fix when errors were arisen. 

# Validation - the right system has been built
We are able to check that the right system has been built via integration and systems testing. By using the front end, we can check that our creation and implementation of backend code properly works with the front-end. By manual testing and general use of the front end, we are able to prove that we have a valid system implementation. 
Our overall approach to this development process has a backbone of our user stories, which built our requirements and bridged the understanding that we have between spec requirements, and actual tasks/objectives to complete in order to reach our final product. Through our process of slowly iterating our delegated tasks within the backend functions, we each adhered to the requirements that we have setup in Iteration One, and continued with daily discussions on Messenger with screenshots and some Codeshare sessions to reflect any concerns or debatable points. These collaborations upon individually driven subtasks allowed us to a), meet a time frame and most importantly b), achieve a system with a high degree of validation which meets the ‘correct’ current requirements. 

Acceptance Criteria 
NOTE -> All the acceptance criteria use the perspective of the User, or App Slackr. 

*Epic 1: As a prospective/existing user of Slackr, I want the registration and login/logout processes to be quick, easy and secure so that I can regularly use the application for my messaging needs.* 
* US 1.1 [Register] : “As a Slackr user, I want to be able to create an account using a legitimate email address, strong password, first name and last name, so that I can register in the app with my identity.”
    * Clearly create account with different fields 
    * A weak password should be rejected
* US 1.2 [Login & Logout] : “As a Slackr user, I want to be able to quickly and securely login and logout, so that I can control the access to my personalised Slackr account.“
    *  A registered account should be able to log out, and then log in again
    *  The user setting should be the same after logging back in
    *  I want to be brought back to the login page after logging in
* US 1.3 [Reset Password] : “As a Slackr user, if I forget my password, I want password reset instructions to be sent to my registered email, so that I can securely reset my account password with clear steps and validation. 
    *  An email should be instantly sent after requesting a password reset
    *  A reset code can only be used once
    *  Cannot reset password without token

*Epic 2: As a Slackr user, I want to be able to easily create, join, view or leave channels, as well as invite others to a channel that I am a member of, so that I am able to communicate with specified others in the channels of my choice.*
* US 2.1 [Create] : “ As a Slackr user, I want to be able to create a channel where I can set the channel's name, purpose and whether the channel is public/private, so that I am able to create a channel to my own needs and specifications. “
    * Create a unique channel name
    * Private channels should be hidden from other users
    * A private channel should be indicated by an icon next to channel name
* US 2.2 [Join/Leave] : “As a Slackr user, I want to be able to join or leave a channel, so that I am only a member of channels that I want to be in.“
    * Leaving a channel should allow messages to continue to exist
    * After joining a channel, previous messages should be viewable
* US 2.3 [View] : “As a Slackr user, I want a clear view of all my groups and connections that I am a member of, so that I can quickly/easily access them.“
    * Messages in each channel should be independent for the channel
    * It should be clear what channel is currently open
* US 2.4 [Invite] : “As a Slackr user, I want to be able to send invites to other Slackr users to my channel, so that I can communicate with them on the channel.“
    * Be able to invite other members to channels a user is in

*Epic 3: As a Slackr user, I want to be able to view all messages and channel details, so that I can clearly identify the channels I am a member of.*
* US 3.1 [View Messages] : “As a Slackr user, I want to be able to see all messages in a channel, so that I can keep track of all conversations and be able to refer to them at any point in time if required.“
    * All messages should stay in a channel unless deleted
    * Each messages in a channel should be independent of the channel
* US 3.2 [View Details - Members] : “As a Slackr user, I want to be able to see the list of people in the channel, so I know who will be able to see my messages in the channel.“
    * All members should be visible regardless of the channel status
    * Channel member user profiles should be viewable directly from the channel
* US 3.3 [View Details - Other] : “As a user, I want to have access to the details of the channel such as its name, so that I can better identify my channels.“
    * Channel names should be static, and should not change
    * Channel names should appear in the channel page and on the sidebar
    * The channel name should be the same as the created name

*Epic 4: As a Slackr user I want to be able to send messages at varying times to a channel, so that it can be read by other users.*
* US 4.1 [Send] : “As a Slackr user, I want my messages to be sent in real time, so others in the channel can communicate with me immediately.”
    * Messages should appear live without needing to reload the page
    * This should occur to myself and other users
    * There is no noticeable delay when sending a message
*US 4.2 [Send Later] : “As a Slackr user, I want the option of sending these messages at a set time so that I can plan announcements.”*
    * Sending messages later should appear at the instant of the set time
    * A set time should be any time in the future
* US 4.3 [Search] : “As a Slackr user, I want to be able to search for strings in the full set of messages in a channel, so I can easily find earlier messages if required for reference at any point of time.”
    * A search should return a list of messages
    * The returned messages should come from various channels

*Epic 5: As a user of Slackr, I want to be able to interact with sent messages, so that I can enhance my communication experience."*
* US 5.1 [Edit] : “As a Slackr user, I want to be able to edit a message, so that I can correct myself or add more detail without sending a new message.”
    * A user can edit a message without its place is lost in the message list
    * An admin or owner can delete anyones message
* US 5.2 [Remove] : “As a Slackr user, I want to remove the messages I send if I do not want the message to remain in the channel any more.”
    * A user should be able to, at any time, remove a message he sent in a channel they’re in
    * An admin or owner should be able to delete anyone’s message
* US 5.3 [Pin/Unpin] : “As a Slackr user, I want to be able to pin or unpin any messages so that I can easily reference important messages or links that the group can use for particular information.”
    * An admin or owner can pin and unpin messages
    * These messages are easily viewable from anyone in the channel
* US 5.4 [React/Unreact] : “As a Slackr user, I want to be able to react and unreact to messages so that I can quickly convey my feelings.”
    * A user can react and unreact to anyone’s messages, including their own.
    * They should be able to see if they have reacted to a message or not
    * They should be able to see how many people have reacted to a message.

*Epic 6: As a Slackr user, I want to view the user profiles of others, and update my own, so that we can find current information about one another.*
* US 6.1 [View] : “As a Slackr user, I want to be able to view other people's user profiles, so that I can identify the people I am interacting with.”
    * A user can see other people’s profiles
    * They can see name, handle and picture of other people by viewing their profiles
* US 6.2 [Modify] : “As a Slackr user, I want to be able to construct my own profile with a picture, name, email and handle, and also be able to choose how much personal information I want to provide the app.”
    * A user can add this information to their own profiles
    * A user can pick how much they want to share

*Epic 7: “As a Slackr admin, I want to be able to modify admin privileges so that I and other members can moderate a channel to our specifications.”*
* US 7.1 [Admin]: “As a Slackr admin, I want to give other members admin and owner privileges, so that they can assist with the running of the channel.”
    * A user with admin and owner permission can give others admin and owner permission.


