import pytest
import sys
sys.path.append('server/')
from functions.channel_functions import channel_addowner, channel_details, channel_invite, channel_join, channel_leave, channel_messages, channel_removeowner, channels_create, channels_list, channels_listall
from functions.helper_functions import reset_data, all_channels_details, list_of_users, change_user_app_permission, get_user_from_token, get_total_channel_messages, get_channel_id_from_name, all_channels_permissions, check_token_in_channel, check_user_in_channel, change_user_channel_permission, get_user_details
from functions.auth_functions import auth_register
from functions.message_functions import message_send
from functions.Errors import AccessError
import datetime

@pytest.fixture()
def setup():
	reset_data()
	a_user_details = auth_register(email="userA@userA.com", password="Go0dPa>sword", name_first = "User", name_last="A")
	a_user_id = a_user_details['u_id']
	a_token = a_user_details['token']
	b_user_details = auth_register(email = "userB@userB.com", password = "G00DPa>$word", name_first = "First", name_last = "B")
	b_user_id = b_user_details['u_id']
	b_token = b_user_details['token']
	channel_a_id = channels_create(token = a_token, name = "Channel A", is_public = False) # Private Channel created by user A
	channel_b_id = channels_create(token = a_token, name = "Channel B", is_public = True)  # Public Channel created by user A
	return [a_user_id, b_user_id, a_token, b_token, channel_a_id, channel_b_id]
	#       setup[0], setup[1], setup[2], setup[3], setup[4], setup[5]

#################################################################################
##                           TESTING channel_invite                            ##
#################################################################################
def tests_channel_invite_valid(setup):
	u_id = setup[1] ## u_id that is being invited to channel
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## These are valid values, and hence should not produce errors:
	channel_invite(token = token, channel_id = channel_id_private, u_id = u_id)
	channel_invite(token = token, channel_id = channel_id_public, u_id = u_id)

def tests_check_token_or_user_in_channel_fails(setup):
	assert check_token_in_channel(setup[2], -1) == False
	assert check_user_in_channel(setup[2], -1) == False

def tests_channel_invite_channel_nonexisting(setup):
	u_id = setup[1] ## u_id that is being invited to channel
	channel_id = -1 ## some invalid channel_id
	token = setup[2]

	## The channel id is a non-existing and thereby invaild id, and hence should produce a ValueError:
	with pytest.raises(ValueError):
		channel_invite(token = token, channel_id = channel_id, u_id = u_id)

def tests_channel_invite_user_not_member(setup):
	u_id = setup[0] ## u_id that is being invited to channel
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	token = setup[3] ## token of accessing user who is not an owner or member of channel setup[4] or setup[5]

	## The accessing user is not a member of either channel, and hence should produce a AccessError:
	with pytest.raises(AccessError):
		channel_invite(token = token, channel_id = channel_id_private, u_id = u_id)
	with pytest.raises(AccessError):
		channel_invite(token = token, channel_id = channel_id_public, u_id = u_id)

def tests_channel_invite_user_already_member(setup):
	u_id = setup[0] ## u_id that is being invited to channel
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## The invited user is already a member of either channel, and hence should produce a ValueError:
	with pytest.raises(ValueError):
		channel_invite(token = token, channel_id = channel_id_private, u_id = u_id)
	with pytest.raises(ValueError):
		channel_invite(token = token, channel_id = channel_id_public, u_id = u_id)

def tests_channel_invite_user_invalid(setup):
	u_id = -1 ## u_id that is being invited to channel
	channel_id = setup[4]
	token = setup[2]

	## The user id does not exist, and hence a ValueError should occur:
	with pytest.raises(ValueError):
		channel_invite(token = token, channel_id = channel_id, u_id = u_id)

def tests_channel_invite_token_invalid(setup):
	u_id = setup[0] ## u_id that is being invited to channel
	channel_id = setup[4]
	token = -1

	## The token passed into the function does not correspond to any accessing user,
	## hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_invite(token = token, channel_id = channel_id, u_id = u_id)

#################################################################################
##                           TESTING channel_details                           ##
#################################################################################
'''
	Within channel_details, we are assuming and interpreting that it returns a
	dictionary that provides the channel name as a string, then a list of the owners,
	then a list of all members.

'''

def tests_channel_details_valid(setup):
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## These are valid values, and hence should not produce errors:
	assert channel_details(token = token, channel_id = channel_id_private) == {'name': 'Channel A', 'owner_members': [{'u_id': 1, 'name_first': 'User', 'name_last': 'A', 'profile_img_url': None}], 'all_members': [{'u_id': 1, 'name_first': 'User', 'name_last': 'A', 'profile_img_url': None}]}
	assert channel_details(token = token, channel_id = channel_id_public) == {'name': 'Channel B', 'owner_members': [{'u_id': 1, 'name_first': 'User', 'name_last': 'A', 'profile_img_url': None}], 'all_members': [{'u_id': 1, 'name_first': 'User', 'name_last': 'A', 'profile_img_url': None}]}

def tests_channel_details_channel_nonexisting(setup):
	channel_id = -1
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## There should be a ValueError produced since the given channel_id does not exist.
	with pytest.raises(ValueError):
		channel_details(token = token, channel_id = channel_id)

def tests_channel_details_user_not_member(setup):
	channel_id = setup[4]
	token = setup[3] ## token of accessing user who is not an owner or member of channel setup[4] or setup[5]

	## There should be an AccessError produced since the accessing user is not a
	## member of the channel.
	with pytest.raises(AccessError):
		channel_details(token = token, channel_id = channel_id)

def tests_channel_details_token_invalid(setup):
	channel_id = setup[4]
	token = 'InvalidTokenString'

	## The token passed into the function does not correspond to any accessing user,
	## hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_details(token = token, channel_id = channel_id)

#################################################################################
##                           TESTING channel_messages                          ##
#################################################################################

'''
	For channel_messages, assume there is some function/functionality within channel_messages()
	that prompts users for an input of some start value, called message_start_index().

	Assume there is also some function/functionality within channel_messages() that provides us
	the number of messages in the channel, as long as the token given pertains to a user that is
	a member of the channel, called total_channel_messages().

'''

@pytest.fixture()
def add_messages_to_channel(setup):
	## Assuming that message_send has full functionality, (tested in message_tests.py):
	token_user_A = setup[2] ## Token of user who is owner of channels setup[4] and setup[5]
	channel_id_public = setup[5] ## Channel id of the public channel from main setup fixture
	message_one_id = message_send(token_user_A, channel_id_public, "Hello here is a message.")
	message_two_id = message_send(token_user_A, channel_id_public, "Hello here is a second message.")
	return [message_one_id, message_two_id]

def tests_channel_messages_valid(setup, add_messages_to_channel):
	channel_id_public = setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	start = 0 ## assume that message_start_index() is given an input of 0

	## This should produce no errors as all valid values:
	return_messages = channel_messages(token = token, channel_id = channel_id_public, start = start)
	assert return_messages['messages'][1]['message'] == "Hello here is a message."
	assert return_messages['messages'][0]['message'] == "Hello here is a second message."

def tests_channel_messages_above_fifty(setup):
	channel_id_public = setup[5]
	token = setup[2]
	start = 0

	for i in range(0, 53):
		message_send(token, channel_id_public, "Hi this is spam")

	## This should produce no errors:
	channel_messages(token = token, channel_id = channel_id_public, start = start)


def tests_channel_messages_total_invalid(setup):
	assert get_total_channel_messages(-1) == {}

def tests_channel_messages_empty(setup):
	channel_id_public = setup[5] ## valid channel id
	token = setup[2] ## valid token
	start = 0 ## only valid start index for an empty channel

	## This should produce no errors:
	return_messages = channel_messages(token = token, channel_id = channel_id_public, start = start)
	assert return_messages == {'end': -1, 'messages': [], 'start': 0}

def tests_channel_messages_single_message(setup):
	channel_id_public = setup[5] ## valid channel id
	token = setup[2] ## valid token of member in channel
	start = 0 ## only valid start index for a single message channel

	message_send(token, channel_id_public, "Hello here is a message.")
	## This should produce no errors:
	return_messages = channel_messages(token = token, channel_id = channel_id_public, start = start)
	assert return_messages['messages'][0]['message'] == "Hello here is a message."

def tests_channel_messages_channel_nonexisting(setup):
	channel_id = -1
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	start = 0 ## doesnt matter

	## This should produce a ValueError as the channel_id does not exist:
	with pytest.raises(ValueError):
		channel_messages(token = token, channel_id = channel_id, start = start)

def tests_channel_messages_start_invalid(setup):
	channel_id = setup[4]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	start = get_total_channel_messages(channel_id) + 1
	## This should produce a ValueError as start > total messages in channel:
	with pytest.raises(ValueError):
		channel_messages(token = token, channel_id = channel_id, start = start)

def tests_channel_messages_user_not_member(setup):
	channel_id = setup[4]
	token = setup[3] ## token of accessing user who is not an owner or member of
					## channel setup[4] or setup[5]
	start = 4 ## doesnt matter

	## This should produce an AccessError as the authorised user is not a member
	## of the channel:
	with pytest.raises(AccessError):
		channel_messages(token = token, channel_id = channel_id, start = start)

def tests_channel_messages_token_invalid(setup):
	channel_id = setup[4]
	token = -1
	start = 0 ## doesnt matter

	## The token passed into the function does not correspond to any accessing
	## user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_messages(token = token, channel_id = channel_id, start = start)

################################################################################
##                           TESTING channel_leave                            ##
################################################################################
## Potentially could add in check with channel_details after execution of a member
## leave, to ensure amount of members has changed in channel (Add assumption that
## details works)

def tests_channel_leave_valid(setup):
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4]
					## and setup[5]

	## This should produce no errors as all values are valid:
	channel_leave(token = token, channel_id = channel_id_private)
	channel_leave(token = token, channel_id = channel_id_public)

def tests_channel_leave_channel_nonexisting(setup):
	channel_id = -1
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## This should produce a ValueError as the channel does not exist:
	with pytest.raises(ValueError):
		channel_leave(token = token, channel_id = channel_id)

def tests_channel_leave_user_not_member(setup):
	channel_id = setup[4]
	token = setup[3] ## token of accessing user who is not an owner or member of
					## channel setup[4] or setup[5]

	## This should produce a AccessError as the authorised user is not a member
	## of the channel:
	with pytest.raises(AccessError):
		channel_leave(token = token, channel_id = channel_id)

def tests_channel_leave_token_invalid(setup):
	channel_id = setup[4]
	token = 'InvalidTokenString' ## token of accessing user

	## The token passed into the function does not correspond to any accessing
	## user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_leave(token = token, channel_id = channel_id)

################################################################################
##                           TESTING channel_join                             ##
################################################################################

def tests_channel_join_valid(setup):
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	token = setup[3] ## token of accessing user who is not owner of channel setup[4] and setup[5]
	## Let us give this user a permission id of admin meaning they can join both channels:
	change_user_app_permission(get_user_from_token(token), 1)

	## This should produce no errors as all values are valid:
	channel_join(token = token, channel_id = channel_id_public)
	channel_join(token = token, channel_id = channel_id_private)

def tests_channel_join_channel_nonexisting(setup):
	channel_id = -1
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## This should produce a ValueError as the channel does not exist:
	with pytest.raises(ValueError):
		channel_join(token = token, channel_id = channel_id)

def tests_channel_join_user_not_admin(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	## channel_id of the public channel created by the user of token setup[2]
	channel_id_public = setup[5]
	u_id = setup[1] ## token of user who is not owner of channel setup[4] or setup[5]
	channel_addowner(token = token, channel_id = channel_id_public, u_id = u_id)
	## now user setup[3] is member of public channel [5]
	channel_id_private = setup[4] ## reassign to private channel
	token = setup[3] ## token of accessing user who is an owner of public
					## channel [5] but not private channel [4]
	## This should produce a AccessError as the authorised user is not an admin
	## of the private channel [4]:
	with pytest.raises(AccessError):
		channel_join(token = token, channel_id = channel_id_private)

def tests_channel_join_user_already_member(setup):
	channel_id = setup[4]
	token = setup[2] ## token of accessing user who is already an owner or member of
					## channel setup[4] or setup[5]

	## This should produce a ValueError as the authorised user is already a member of the channel:
	with pytest.raises(ValueError):
		channel_join(token = token, channel_id = channel_id)

def tests_channel_join_token_invalid(setup):
	channel_id = setup[4]
	token = 'InvalidTokenString' ## token of accessing user

	## The token passed into the function does not correspond to any accessing
	## user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_join(token = token, channel_id = channel_id)

#################################################################################
##                           TESTING channel_addowner                          ##
#################################################################################

def tests_channel_addowner_valid(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	u_id = setup[1] ## token of user who is not an owner or member of channel setup[4] or setup[5]

	## With all valid values, this should produce no errors:
	channel_addowner(token = token, channel_id = channel_id_public, u_id = u_id)
	channel_addowner(token = token, channel_id = channel_id_private, u_id = u_id)

def tests_channel_addowner_provided_user_already_owner(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id = setup[4]
	u_id = setup[0] ## token of same user

	## Given a user id that is already an owner, there should be a ValueError:
	with pytest.raises(ValueError):
		channel_addowner(token = token, channel_id = channel_id, u_id = u_id)

def tests_channel_addowner_access_user_not_owner(setup):
	token = setup[3] ## token of accessing user who is not an owner of
					## channel setup[4] and setup[5], but is a member
	channel_id = setup[5] ## channel_id of the public channel created by the user of token setup[2]
	u_id = setup[0] ## token of user who is an owner of channel setup[4] or setup[5]
	## With the accessing authorised user not being an owner of the channel, there should be an AccessError:
	with pytest.raises(AccessError):
		channel_addowner(token = token, channel_id = channel_id, u_id = u_id)

def tests_channel_addowner_channel_nonexisting(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id = -1
	u_id = setup[1] ## token of user who is not owner of channel setup[4] or setup[5]

	## Given a channel id that does not exist, there should be a ValueError:
	with pytest.raises(ValueError):
		channel_addowner(token = token, channel_id = channel_id, u_id = u_id)

def tests_channel_addowner_u_id_invalid(setup):
	channel_id = setup[4] ## doesnt matter
	token = setup[2] ## doesnt matter
	u_id = -1

	## Due to an invalid u_id being provided, there should be a ValueError.
	with pytest.raises(ValueError):
		channel_addowner(token = token, channel_id = channel_id, u_id = u_id)

def tests_channel_addowner_token_invalid(setup):
	channel_id = setup[4]
	token = -1 ## invalid token
	u_id = setup[1] ## token of user who is not owner of channel setup[4] or setup[5]

	## The token passed into the function does not correspond to any accessing
	## user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_addowner(token = token, channel_id = channel_id, u_id = u_id)

#################################################################################
##                           TESTING channel_removeowner                       ##
#################################################################################
'''
	In channel_removeowner, we are assuming that channel_addowner adds a user into
	a channel as a member AND owner.
'''

def tests_channel_removeowner_valid(setup):
	## Adding extra owner:
	token = setup[2] ## token of user who is owner of channel setup[4] and setup[5]
	c_user_details = auth_register(email = "userC@userC.com", password = "gO0dPa$$3orD", name_first = "User", name_last = "C")
	c_user_id = c_user_details['u_id']
	c_token = c_user_details['token']
	## These will now add user C as a member and owner of channels setup[4] and setup[5]:

	channel_addowner(token = token, channel_id = setup[4], u_id = c_user_id)
	channel_addowner(token = token, channel_id = setup[5], u_id = c_user_id)
	print("new permissions:")
	print(all_channels_permissions)
	token = c_token ## token of accessing user who is an owner of channel setup[4] and setup[5]
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	u_id = setup[0] ## token of user who is an owner of channel setup[4] or setup[5]

	## With all valid values, this should produce no errors:
	channel_removeowner(token = token, channel_id = channel_id_public, u_id = u_id)
	channel_removeowner(token = token, channel_id = channel_id_private, u_id = u_id)

def tests_channel_removeowner_provided_user_not_owner(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	u_id = setup[1] ## token of user who is not an owner or member of channel setup[4] or setup[5]

	## With the provided user id not being an owner of either channel already, there should be an ValueError:
	with pytest.raises(ValueError):
		channel_removeowner(token = token, channel_id = channel_id_private, u_id = u_id)
	with pytest.raises(ValueError):
		channel_removeowner(token = token, channel_id = channel_id_public, u_id = u_id)

def tests_channel_removeowner_accessing_user_not_owner(setup):
	token = setup[3] ## token of accessing user who is not an owner of channel setup[4] or setup[5]
	channel_id_private = setup[4]
	channel_id_public = setup[5]
	u_id = setup[0] ## id of user who is an owner or member of channel setup[4] or setup[5]

	## With the accessing token not being an owner of either channel already, there should be an AcessError:
	with pytest.raises(AccessError):
		channel_removeowner(token = token, channel_id = channel_id_private, u_id = u_id)
	with pytest.raises(AccessError):
		channel_removeowner(token = token, channel_id = channel_id_public, u_id = u_id)

def tests_channel_removeowner_channel_nonexisting(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id = -1
	u_id = setup[1] ## token of user who is not an owner or member of channel setup[4] or setup[5]

	## Given a channel id that does not exist, there should be a ValueError:
	with pytest.raises(ValueError):
		channel_removeowner(token = token, channel_id = channel_id, u_id = u_id)

def tests_channel_removeowner_u_id_invalid(setup):
	channel_id = setup[4] ## doesnt matter
	token = setup[2] ## doesnt matter
	u_id = -1

	## Due to an invalid u_id being provided, there should be a ValueError.
	with pytest.raises(ValueError):
		channel_removeowner(token = token, channel_id = channel_id, u_id = u_id)

def tests_channel_removeowner_token_invalid(setup):
	channel_id = setup[4]
	token = 'InvalidTokenString' ## token of accessing user
	u_id = setup[1] ## token of user who is not owner of channel setup[4] or setup[5]

	## The token passed into the function does not correspond to any accessing
	## user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_removeowner(token = token, channel_id = channel_id, u_id = u_id)

#################################################################################
##                           TESTING channels_list                             ##
#################################################################################

def tests_channels_list_valid(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	returning_channels = channels_list(token = token)
	## This should succeed:
	assert returning_channels[0]['name'] == "Channel A" ## name of first channel that user is member of
	assert returning_channels[1]['name'] == "Channel B" ## name of second channel that user is member of

def tests_channels_list_user_nonexisting(setup):
	token = setup[3] ## token of accessing user who is not an owner of channel
					## setup[4] or setup[5]. They are member of no channels.

	returning_channels = channels_list(token = token)
	## This should succeed:
	assert returning_channels == []

def tests_channels_list_token_invalid(setup):
	token = 'InvalidTokenString'

	## The token passed into the function does not correspond to any accessing
	## user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channels_list(token = token)

#################################################################################
##                           TESTING channels_listall                          ##
#################################################################################

def tests_channels_listall_valid(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	returning_channels = channels_listall(token = token)
	## This should succeed:
	assert returning_channels[0]['name'] == "Channel A" ## name of first channel that user is member of
	assert returning_channels[1]['name'] == "Channel B" ## name of second channel that user is member of

def tests_channels_listall_user_nonexisting(setup):
	token = setup[3] ## token of accessing user who is not an owner of channel setup[4] or setup[5]. They are member of no channels.

	returning_channels = channels_listall(token = token)
	## This should succeed:
	assert returning_channels[0]['name'] == "Channel A" ## name of first channel that is existing
	assert returning_channels[1]['name'] == "Channel B" ## name of second channel that is existing

def tests_channels_listall_token_invalid(setup):
	token = 'InvalidTokenString'

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channels_listall(token = token)

#################################################################################
##                           TESTING channels_create                           ##
#################################################################################
'''
	For channels_create, we will have the name and ispublic come in from flask.
	The error checking for these can be done within flask but are also done
	in the functions already. As for the values they have, we can therefore just
	use values that we come up with down here, for testing.
'''

def tests_channels_create_valid(setup):
	is_public = True ## Can be True or False -> we assume valid input comes through.
	name_one = 'Channel Z'
	token_user_1 = setup[2]

	## This should produce no errors:
	return_id = channels_create(token = token_user_1, name = name_one, is_public = is_public)
	assert return_id == get_channel_id_from_name(name_one)

def tests_channels_create_name(setup):
	assert get_channel_id_from_name(-1) == {}

def tests_channels_create_permissions_fail(setup):
	assert change_user_app_permission(-1, 1) == {}
	## This should have no errors and satisfy coverage:
	change_user_channel_permission(-1, 1, -1)

def tests_channels_create_name_over_twenty(setup):
	is_public = True ## doesnt matter
	name = 'x'*21 ## adding on a 21 character string
	token = setup[2]

	## This should produce a ValueError as name is above 20 chars long:
	with pytest.raises(ValueError):
		channels_create(token = token, name = name, is_public = is_public)

def tests_channels_create_token_invalid(setup):
	token = -1
	name = 'Anything'
	is_public = True ## doesnt matter

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channels_create(token = token, name = name, is_public = is_public)

## END OF CHANNEL TESTS
reset_data()