import pytest

@pytest.fixture()
def setup():
		a_user_id, a_token = auth_register("userA@userA.com", "Go0dPa>sword", "User", "A")
    b_user_id, b_token = auth_register("userB@userB.com", "G00DPa>$word", "User", "B")
    channel_a_id = channels_create(a_token, "Channel A", False) # Private Channel created by user A
    channel_b_id = channels_create(a_token, "Channel B", True)  # Public Channel created by user A  
    return [a_user_id, b_user_id, a_token, b_token, channel_a, channel_b]
    #       setup[0], setup[1], setup[2], setup[3], setup[4], setup[5]

#################################################################################
##                           TESTING channel_invite                            ##
#################################################################################
def tests_channel_invite_valid(setup):
	u_id = setup[1] ## u_id that is being invited to channel
	channel_id_1 = setup[4]  
    channel_id_2 = setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## These are valid values, and hence should not produce errors:
	channel_invite(token, channel_id_1, u_id)
	channel_invite(token, channel_id_2, u_id)
  
def tests_channel_invite_channel_nonexisting(setup):
	u_id = setup[1] ## u_id that is being invited to channel
	channel_id = -1 ## some invalid channel_id -> chuck into assumptions
	token = setup[2]

	## The channel id is a non-existing and thereby invaild id, and hence should produce a ValueError:
	with pytest.raises(ValueError):
		channel_invite(token, invalid_id, u_id)

def tests_channel_invite_user_not_member(setup):
	u_id = setup[0] ## u_id that is being invited to channel
	channel_id = setup[4] or setup[5]
	token = setup[3] ## token of accessing user who is not an owner or member of channel setup[4] or setup[5]

	## The accessing user is not a member of this channel, and hence should produce a ValueError:
	with pytest.raises(ValueError):
		channel_invite(token, channel_id, u_id)

def tests_channel_invite_user_already_member(setup):
	u_id = setup[0] ## u_id that is being invited to channel
	channel_id = setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## The invited user is already a member of this channel, and hence should produce a ValueError:
	with pytest.raises(ValueError):
		channel_invite(token, channel_id, u_id)

def tests_channel_invite_user_invalid(setup):
	u_id = -1 ## u_id that is being invited to channel
	channel_id = setup[4] or setup[5]
	token = setup[2]
	
	## The user id does not exist, and hence a ValueError should occur:
	with pytest.raises(ValueError):
		channel_invite(token, channel_id, u_id)

def tests_channel_invite_token_invalid(setup):
	u_id = setup[0] ## u_id that is being invited to channel
	channel_id = setup[4] or setup[5]
	token = -1

	## The token passed into the function does not correspond to any accessing user, 
	## hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_invite(token, channel_id, u_id)

#################################################################################
##                           TESTING channel_details                           ##
#################################################################################

def tests_channel_details_valid(setup):
	channel_id = setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## These are valid values, and hence should not produce errors:
	assert channel_details(token, channel_id) == {'Channel A', setup[0], setup[0]} ## Work on this 

def tests_channel_details_channel_nonexisting(setup):
	channel_id = not setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## There should be a ValueError produced since the given channel_id does not exist. 
	with pytest.raises(ValueError):
		channel_details(token, channel_id)

def tests_channel_details_user_not_member(setup):
	channel_id = setup[4] or setup[5]
	token = setup[3] ## token of accessing user who is not an owner or member of channel setup[4] or setup[5]

	## There should be an AccessError produced since the accessing user is not a 
	## member of the channel.
	with pytest.raises(AccessError):
		channel_details(token, channel_id)

def tests_channel_details_token_invalid(setup):
	channel_id = setup[4] or setup[5]
	token = not setup[2] or setup[3]

	## The token passed into the function does not correspond to any accessing user, 
	## hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_details(token, channel_id)

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

##= Consider second fixture here that adds in messages ##
def tests_channel_messages_valid(setup):
	channel_id = setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	start = message_start_index() ##= consider naming function better

	## This should produce no errors as all valid values and cases are used:
	channel_messages(token, channel_id, start) ##= Assert return value corresponds to fixture above

def tests_channel_messages_channel_nonexisting(setup):
	channel_id = not setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	start = message_start_index()

	## This should produce a ValueError as the channel_id does not exist:
	with pytest.raises(ValueError):
		channel_messages(token, channel_id, start)

def tests_channel_messages_start_invalid(setup):
	channel_id = setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	start = message_start_index() + total_channel_messages() + 1

	## This should produce a ValueError as start > total messages in channel:
	with pytest.raises(ValueError):
		channel_messages(token, channel_id, start)

def tests_channel_messages_user_not_member(setup):
	channel_id = setup[4] or setup[5]
	token = setup[3] ## token of accessing user who is not an owner or member of channel setup[4] or setup[5]
	start = message_start_index()

	## This should produce an AccessError as the authorised user is not a member of the channel:
	with pytest.raises(AccessError):
		channel_messages(token, channel_id, start)

def tests_channel_messages_token_invalid(setup):
	channel_id = setup[4] or setup[5]
	token = not setup[2] or setup[3] 
	start = message_start_index()

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_messages(token, channel_id)

#################################################################################
##                           TESTING channel_leave                             ##
#################################################################################
## Add in check with channel_details after execution of a member leave, to ensure amount of members 
## has changed in channel (Add assumption that details works)
def tests_channel_leave_valid(setup):
	channel_id = setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## This should produce no errors as all values are valid:
	channel_leave(token, channel_id)

def tests_channel_leave_channel_nonexisting(setup):
	channel_id = not setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## This should produce a ValueError as the channel does not exist:
	with pytest.raises(ValueError):
		channel_leave(token, channel_id)

def tests_channel_leave_user_not_member(setup):
	channel_id = setup[4] or setup[5]
	token = setup[3] ## token of accessing user who is not an owner or member of channel setup[4] or setup[5]

	## This should produce a AccessError as the authorised user is not a member of the channel:
	with pytest.raises(AccessError):
		channel_leave(token, channel_id)
def tests_channel_leave_token_invalid(setup):
	channel_id = setup[4] or setup[5]
	token = not setup[2] or setup[3] ## token of accessing user

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_leave(token, channel_id)

#################################################################################
##                           TESTING channel_join                              ##
#################################################################################

def tests_channel_join_valid(setup):
	channel_id = setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## This should produce no errors as all values are valid:
	channel_join(token, channel_id)

def tests_channel_join_channel_nonexisting(setup):
	channel_id = not setup[4] or setup[5]
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	## This should produce a ValueError as the channel does not exist:
	with pytest.raises(ValueError):
		channel_join(token, channel_id)

def tests_channel_join_user_not_admin(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id = setup[5] ## channel_id of the public channel created by the user of token setup[2]
	u_id = setup[1] ## token of user who is not owner of channel setup[4] or setup[5]
	channel_addowner(token, channel_id, u_id) ## now user setup[3] is member of public channel [5] 

	channel_id = setup[4] ## reassign to private channel
	token = setup[3] ## token of accessing user who is an owner of public channel [5] but not private channel [4]

	## This should produce a AccessError as the authorised user is not an admin of the private channel [4]:
	with pytest.raises(AccessError):
		channel_join(token, channel_id)

def tests_channel_join_user_not_member(setup): ## Is this a repeat?
	channel_id = setup[4]
	token = setup[3] ## token of accessing user who is not an owner or member of channel setup[4] or setup[5]

	## This should produce a AccessError as the authorised user is not a member of the channel:
	with pytest.raises(AccessError):
		channel_join(token, channel_id)

def tests_channel_join_token_invalid(setup):
	channel_id = setup[4] or setup[5]
	token = not setup[2] or setup[3] ## token of accessing user

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_join(token, channel_id)

#################################################################################
##                           TESTING channel_addowner                          ##
#################################################################################

def tests_channel_addowner_valid(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id = setup[4] or setup[5] 
	u_id = setup[1] ## token of user who is not an owner or member of channel setup[4] or setup[5]

	## With all valid values, this should produce no errors:
	channel_addowner(token, channel_id, u_id)

def tests_channel_addowner_provided_user_already_owner(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id = setup[4] or setup[5] 
	u_id = setup[0] ## token of same user

	## Given a user id that is already an owner, there should be a ValueError:
	with pytest.raises(ValueError):	
		channel_addowner(token, channel_id, u_id)

def tests_channel_addowner_access_user_not_owner(setup):
	token = setup[3] ## token of accessing user who is not an owner or member of channel setup[4] and setup[5]
	channel_id = setup[5] ## channel_id of the public channel created by the user of token setup[2]
	u_id = setup[0] ## token of user who is an owner of channel setup[4] or setup[5]

	## With the accessing authorised user not being an owner of the channel, there should be an AccessError:
	with pytest.raises(ValueError):	
		channel_addowner(token, channel_id, u_id)

def tests_channel_addowner_channel_nonexisting(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id = not setup[4] or setup[5] 
	u_id = setup[1] ## token of user who is not owner of channel setup[4] or setup[5]

	## Given a channel id that does not exist, there should be a ValueError:
	with pytest.raises(ValueError):	
		channel_addowner(token, channel_id, u_id)
## chuck in user invalid
def tests_channel_addowner_token_invalid(setup):	
	channel_id = setup[4] or setup[5] 
	token = not setup[2] or setup[3] ## token of accessing user
	u_id = setup[1] ## token of user who is not owner of channel setup[4] or setup[5]

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_addowner(token, channel_id, u_id)

#################################################################################
##                           TESTING channel_removeowner                       ##
#################################################################################

def tests_channel_removeowner_valid(setup, add_extra_owner):
	## Adding extra owner:
	token = setup[2] ## token of user who is owner of channel setup[4] and setup[5]
	c_user_id, c_token = auth_register("userC@userC.com", "gO0dPa$$3orD", "User", "C")['u_id'] 
  c_token = auth_register("userC@userC.com", "gO0dPa$$3orD", "User", "C")['token']
	channel_addowner(token, setup[4], c_user_id) ## this now means that user C is an owner of channel setup[4] 
																							 ## assume that it adds them into channel as member and owner
	channel_addowner(token, setup[5], c_user_id) ## this now means that user C is an owner of channel setup[5]

	token = c_token ## token of accessing user who is an owner of channel setup[4] and setup[5]
	channel_id = setup[4] or setup[5] 
	u_id = setup[0] ## token of user who is an owner of channel setup[4] or setup[5]

	## With all valid values, this should produce no errors:
	channel_removeowner(token, channel_id, u_id)

def tests_channel_removeowner_access_user_not_owner(setup):
	token = setup[3] ## token of accessing user who is not an owner or member of channel setup[4] and setup[5]
	channel_id = setup[4] or setup[5] 
	u_id = setup[0] ## token of user who is an owner of channel setup[4] or setup[5]

	## Given an authorised accessing user that is not an owner, there should be a ValueError:
	with pytest.raises(ValueError):	
		channel_removeowner(token, channel_id, u_id)

def tests_channel_removeowner_provided_user_not_owner(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id = setup[4] or setup[5] 
	u_id = setup[1] ## token of user who is not an owner or member of channel setup[4] or setup[5]
	
	## With the provided user id not being an owner of the channel already, there should be an AccessError:
	with pytest.raises(ValueError):	
		channel_removeowner(token, channel_id, u_id)

def tests_channel_removeowner_channel_nonexisting(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]
	channel_id = not setup[4] or setup[5] 
	u_id = setup[1] ## token of user who is not an owner or member of channel setup[4] or setup[5]

	## Given a channel id that does not exist, there should be a ValueError:
	with pytest.raises(ValueError):	
		channel_removeowner(token, channel_id, u_id)
## chuck in user invalid
def tests_channel_removeowner_token_invalid(setup):	
	channel_id = setup[4] or setup[5] 
	token = not setup[2] or setup[3] ## token of accessing user
	u_id = setup[1] ## token of user who is not owner of channel setup[4] or setup[5]

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_removeowner(token, channel_id, u_id)

#################################################################################
##                           TESTING channels_list                             ##
#################################################################################

def tests_channels_list_valid(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	returning_channels = channels_list(token)
	## This should succeed:
	assert returning_channels == {setup[4], setup[5]} ## specify assumptions 

def tests_channels_list_user_nonexisting(setup):
	token = setup[3] ## token of accessing user who is not an owner of channel setup[4] or setup[5]. They are member of no channels.
	
	returning_channels = channels_list(token)
	## This should succeed:
	assert returning_channels == {}

def tests_channels_list_token_invalid(setup):	
	token = not setup[2] or setup[3]

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_channels_list(token)

#################################################################################
##                           TESTING channels_listall                          ##
#################################################################################

def tests_channels_listall_valid(setup):
	token = setup[2] ## token of accessing user who is owner of channel setup[4] and setup[5]

	returning_channels = channels_listall(token)
	## This should succeed:
	assert returning_channels == {setup[4], setup[5]} ## specify assumption 

def tests_channels_listall_user_nonexisting(setup):
	token = setup[3] ## token of accessing user who is not an owner of channel setup[4] or setup[5]. They are member of no channels.
	
	returning_channels = channels_listall(token)
	## This should succeed:
	assert returning_channels == {setup[4], setup[5]}

def tests_channels_listall_token_invalid(setup):	
	token = not setup[2] or setup[3]

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channel_channels_listall(token)

#################################################################################
##                           TESTING channels_create                           ##
#################################################################################
'''
	For channels_create, assume there is some function/functionality within channels_create()
	that prompts users for an input of some channel name, called get_channel_name(), and some 
	function/functionality that prompts users for an input of 'Yes' or 'No' for the option of 
	making a public or private channel, called get_public_status().
'''

def tests_channels_create_valid(setup):
	is_public = get_public_status() 
	name = get_channel_name()
	token = setup[2] or setup[3]

	## This should produce no errors:
	channels_create(token, name, is_public)

def tests_channels_create_name_over_twenty(setup):
	is_public = get_public_status()
	name = get_channel_name() + "IloveHaydenAndHayden!" ## adding on a 21 character string
	token = setup[2] or setup[3]

	## This should produce a ValueError as name is above 20 chars long:
	with pytest.raises(ValueError):
		channels_create(token, name, is_public)

def tests_channels_create_token_invalid(setup):
	token = not setup[2] or setup[3]

	## The token passed into the function does not correspond to any accessing user, and hence AccessError should occur;
	with pytest.raises(AccessError):
		channels_create(token, name, is_public)