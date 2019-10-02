import pytest

###### TESTS FOR channel_invite ######
'''
	Assume these are valid ids, AND u_id 5 is a member of channel_id 2;
	u_id: 5
	channel_id: 2
	channel_id: 3

	Assume this is a token passed in from other functions that use channel:
	token = x where x is some undecided datatype/value.
'''

def tests_channel_invite_valid():
	## u_id that accesses this function:
	u_id = 5
	channel_id = 2
	token = x

	## These are valid values, and hence should not produce errors:
	channel_invite(token, channel_id, u_id)

def tests_channel_invite_channel_nonexisting():
	## u_id that accesses this function:
	u_id = 5
	channel_id = 1
	token = x

	## The channel id is a non-existing and thereby invaild id, and hence should produce a ValueError:
	with pytest.raises(ValueError):
		channel_invite(token, channel_id, u_id)

def tests_channel_invite_user_not_member():
	## u_id that accesses this function:
	u_id = 5
	channel_id = 3
	token = x

	## The user is not a member of this channel, and hence should produce a ValueError:
	with pytest.raises(ValueError):
		channel_invite(token, channel_id, u_id)

def tests_channel_invite_user_invalid():
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = x
	
	## The user id does not exist, and hence a ValueError should occur:
	with pytest.raises(ValueError):
		channel_invite(token, channel_id, u_id)

def tests_channel_invite_token_invalid():
	'''
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = not x

	## The token is passed in is not what was in the other function: hence, an AccessError should occur;
	with pytest.raises(AccessError):
		channel_invite(token, channel_id, u_id)
	'''

###### TESTS FOR channel_details ######
'''
	Assume this is a valid channel_id, and valid user id's:
	channel_id: 2
	u_id: 3
	u_id: 4

	Also, assume u_id 3 is the only user with access to channel 2.

	Assume this is a token passed in from other functions that use channel:
	token = x where x is some undecided datatype/value.
'''

def tests_channel_details_valid():
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = x

	## There should be no errors in executing this as a valid user has accessed this function:
	channel_details(token, channel_id)

def tests_channel_details_channel_nonexisting():
	## u_id that accesses this function:
	u_id = 3
	channel_id = 3
	token = x

	## There should be a ValueError produced since there is no existing channel_id of 3. 
	with pytest.raises(ValueError):
		channel_details(token, channel_id)

def tests_channel_details_user_not_member():
	## u_id that accesses this function:
	u_id = 4
	channel_id = 3
	token = x

	## There should be an AccessError produced since an authorised user is not a member of the channel.
	with pytest.raises(AccessError):
		channel_details(token, channel_id)

def tests_channel_details_token_invalid():
	'''
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = not x

	## The token is passed in is not what was in the other function: hence, an AccessError should occur;
	with pytest.raises(AccessError):
		channel_details(token, channel_id)
	'''

###### TESTS FOR channel_messages ######
'''
	Assume this is a valid channel_id, and valid user id's:
	channel_id: 2
	u_id: 3
	u_id: 4

	Also, assume u_id 3 is the only user with access to channel 2.

	Assume this is a token passed in from other functions that use channel:
	token = x where x is some undecided datatype/value.

	Assume our request for 'start' are:
	start = z where z is some integer < total messages in channel 
	start = y where y is some integer > total messages in channel
'''

def tests_channel_messages_valid():
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = x
	start = z

	## This should produce no errors as all valid values and cases are used:
	channel_messages(token, channel_id, start)

def tests_channel_messages_channel_nonexisting():
	## u_id that accesses this function:
	u_id = 3
	channel_id = 1
	token = x
	start = z

	## This should produce a ValueError as the channel_id does not exist:
	with pytest.raises(ValueError):
		channel_messages(token, channel_id, start)

def tests_channel_messages_start_invalid():
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = x
	start = y

	## This should produce a ValueError as start > total messages in channel:
	with pytest.raises(ValueError):
		channel_messages(token, channel_id, start)

def tests_channel_messages_user_not_member():
	## u_id that accesses this function:
	u_id = 4
	channel_id = 2
	token = x
	start = z

	## This should produce an AccessError as the authorised user is not a member of the channel:
	with pytest.raises(AccessError):
		channel_messages(token, channel_id, start)

def tests_channel_messages_token_invalid():
	'''
	u_id = 3
	channel_id = 2
	token = not x
	start = z

	## The token is passed in is not what was in the other function: hence, an AccessError should occur;
	with pytest.raises(AccessError):
		channel_messages(token, channel_id)
	'''

###### TESTS FOR channel_leave ######
'''
	Assume this is a valid channel_id:
	channel_id: 2
	u_id: 3
	u_id: 4

	Also, assume u_id 3 is the only user with access to channel 2.

	Assume this is a token passed in from other functions that use channel:
	token = x where x is some undecided datatype/value.
'''

def tests_channel_leave_valid():
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = x

	## This should produce no errors as all values are valid:
	channel_leave(token, channel_id)

def tests_channel_leave_channel_nonexisting():
	## u_id that accesses this function:
	u_id = 3
	channel_id = 1
	token = x

	## This should produce a ValueError as the channel does not exist:
	with pytest.raises(ValueError):
		channel_leave(token, channel_id)

def tests_channel_leave_user_not_member():
	'''
	## u_id that accesses this function:
	u_id = 4
	channel_id = 2
	token = x

	## This should produce a AccessError as the authorised user is not a member of the channel:
	with pytest.raises(AccessError):
		channel_leave(token, channel_id)
	'''
def tests_channel_leave_token_invalid():
	'''
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = not x

	## The token is passed in is not what was in the other function: hence, an AccessError should occur;
	with pytest.raises(AccessError):
		channel_leave(token, channel_id)
	'''	

###### TESTS FOR channel_join ######
'''
	Assume this is a valid channel_id, and valid u_id's:
	channel_id: 2
	u_id: 2
	u_id: 3
	u_id: 4

	Also, assume u_id 3 and 4 have access to channel 2, but only 4 is an admin.

	Assume this is a token passed in from other functions that use channel:
	token = x where x is some undecided datatype/value.
'''

def tests_channel_join_valid():
	## u_id that accesses this function:
	u_id = 4
	channel_id = 2
	token = x

	## This should produce no errors as all values are valid:
	channel_join(token, channel_id)

def tests_channel_join_channel_nonexisting():
	## u_id that accesses this function:
	u_id = 4
	channel_id = 1
	token = x

	## This should produce a ValueError as the channel does not exist:
	with pytest.raises(ValueError):
		channel_join(token, channel_id)

def tests_channel_join_user_not_admin():
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = x

	## This should produce a AccessError as the authorised user is not an admin:
	with pytest.raises(AccessError):
		channel_join(token, channel_id)

def tests_channel_join_user_not_member():
	'''
	## u_id that accesses this function:
	u_id = 2
	channel_id = 2
	token = x

	## This should produce a AccessError as the authorised user is not a member of the channel:
	with pytest.raises(AccessError):
		channel_join(token, channel_id)
	'''
def tests_channel_join_token_invalid():
	'''
	## u_id that accesses this function:
	u_id = 3
	channel_id = 2
	token = not x

	## The token is passed in is not what was in the other function: hence, an AccessError should occur;
	with pytest.raises(AccessError):
		channel_leave(token, channel_id)
	'''	

###### TESTS FOR channel_addowner ######
'''
	Assume this is a valid channel_id, and valid u_id's:
	channel_id: 2
	u_id: 2
	u_id: 3
	u_id: 4

	Also, assume u_id 3 and 4 have access to channel 2, but only 4 is 
	an owner of the slackr, or an owner of channel 2.

	Assume the u_id's that access this channel are:
	u_id: 4
	u_id: 5

	Assume this is a token passed in from other functions that use channel:
	token = x where x is some undecided datatype/value.
'''

def tests_channel_addowner_valid():
	## u_id that accesses the function:
	u_id = 4

	## u_id and data provided to function, by the above user:
	u_id = 3
	channel_id = 2
	token = x

	## With all valid values, this should produce no errors:
	channel_addowner(token, channel_id, u_id)

def tests_channel_addowner_provided_user_already_owner():
	## u_id that accesses the function:
	u_id = 4

	## u_id and data provided to function, by the above user:
	u_id = 4
	channel_id = 2
	token = x

	## Given a user id that is already an owner, there should be a ValueError:
	with pytest.raises(ValueError):	
		channel_addowner(token, channel_id, u_id)

def tests_channel_addowner_access_user_not_owner():
	## u_id that accesses the function:
	u_id = not 4

	## u_id and data provided to function, by the above user:
	u_id = 4
	channel_id = 2
	token = x

	## With the user id of the authorised user accessing this function not being an owner, or potentially even a valid user id at all, there should be an AccessError:
	with pytest.raises(ValueError):	
		channel_addowner(token, channel_id, u_id)

def tests_channel_addowner_channel_nonexisting():
	## u_id that accesses the function:
	u_id = 4

	## u_id and data provided to function, by the above user:
	u_id = 4
	channel_id = 1
	token = x

	## Given a channel id that is does not exist, there should be a ValueError:
	with pytest.raises(ValueError):	
		channel_addowner(token, channel_id, u_id)

def tests_channel_addowner_token_invalid():	
	'''
	## u_id that accesses the function:
	u_id = 4

	## u_id and data provided to the function, by the above user:
	u_id = 3
	channel_id = 2
	token = not x

	## The token is passed in is not what was in the other function: hence, an AccessError should occur;
	with pytest.raises(AccessError):
		channel_addowner(token, channel_id, u_id)
	'''	

###### TESTS FOR channel_removeowner ######
'''
	Assume this is a valid channel_id, and valid u_id's:
	channel_id: 2
	u_id: 2
	u_id: 3
	u_id: 4

	Assume the u_id's that access this channel are:
	u_id: 4
	u_id: 5

	Also, assume u_id 3 and 4 have access to channel 2, and only 4 and 5 are 
	an owner of the slackr, or an owner of channel 2.

	Assume this is a token passed in from other functions that use channel:
	token = x (where x is some undecided datatype/value)
'''

def tests_channel_removeowner_valid():
	## u_id that accesses the function:
	u_id = 4

	## u_id and data provided to function, by the above user:
	u_id = 5
	channel_id = 2
	token = x

	## With all valid values, this should produce no errors:
	channel_removeowner(token, channel_id, u_id)

def tests_channel_removeowner_provided_user_not_owner():
	## u_id that accesses the function:
	u_id = 4

	## u_id and data provided to function, by the above user:
	u_id = 3
	channel_id = 2
	token = x

	## Given a user id that is not an owner, there should be a ValueError:
	with pytest.raises(ValueError):	
		channel_removeowner(token, channel_id, u_id)

def tests_channel_removeowner_access_user_not_owner():
	## u_id that accesses the function:
	u_id = not 4 or 5

	## u_id and data provided to function, by the above user:
	u_id = 4
	channel_id = 2
	token = x

	## With the user id of the authorised user accessing this function not being an owner, or potentially even a valid user id at all, there should be an AccessError:
	with pytest.raises(ValueError):	
		channel_removeowner(token, channel_id, u_id)

def tests_channel_removeowner_channel_nonexisting():
	## u_id that accesses the function:
	u_id = 4

	## u_id and data provided to function, by the above user:
	u_id = 5
	channel_id = 1
	token = x

	## Given a channel id that is does not exist, there should be a ValueError:
	with pytest.raises(ValueError):	
		channel_removeowner(token, channel_id, u_id)

def tests_channel_removeowner_token_invalid():	
	'''
	## u_id that accesses the function:
	u_id = 4

	## u_id and data provided to the function, by the above user:
	u_id = 4
	channel_id = 2
	token = not x

	## The token is passed in is not what was in the other function: hence, an AccessError should occur;
	with pytest.raises(AccessError):
		channel_removeowner(token, channel_id, u_id)
	'''	

###### TESTS FOR channels_list ######
'''
	Assume this is a valid u_id:
	u_id: 2

	Assume the list of channels for this user is {valid_authorised_channels}

	Assume this is a token passed in from other functions that use channel:
	token = x (where x is some undecided datatype/value)
'''

def tests_channels_list_valid():
	## u_id that accesses the function:
	u_id = 2
	token = x
	
	returning_channels = channels_list(token)
	## This should succeed:
	assert returning_channels == {valid_authorised_channels}

def tests_channels_list_user_nonexisting():
	## u_id that accesses the function:
	u_id = not 2
	token = x
	
	returning_channels = channels_list(token)
	## This should fail:
	assert returning_channels == {valid_authorised_channels}

def tests_channels_list_token_invalid():	
	'''
	## u_id that accesses the function:
	u_id = 2

	## The token is passed in is not what was in the other function: hence, an AccessError should occur;
	with pytest.raises(AccessError):
		channel_channels_list(token)
	'''	

###### TESTS FOR channels_listall ######
'''
	Assume the list of all channels is {all_channels}

	Assume this is a token passed in from other functions that use channel:
	token = x (where x is some undecided datatype/value)
'''

def tests_channels_list_valid():
	token = x
	
	returning_channels = channels_list(token)
	## This should succeed:
	assert returning_channels == {valid_authorised_channels}

def tests_channels_list_token_invalid():	
	'''
	token = not x

	returning_channels = channels_list(token)
	## The token is passed in is not what was in the other function: hence, this should fail:
	assert returning_channels == {valid_authorised_channels}
	'''

###### TESTS FOR channels_create ######
'''
	The boolean is_public cannot have any error-producing values, so let us just
	use both is_public = True and is_public = False cases in each test.

	Assume the string name has values:
	name = z where z is a string < 20 characters long and > 0 characters long
	name = y where y is a string > 20 characters long

	Assume this is a token passed in from other functions that use channel:
	token = x (where x is some undecided datatype/value)
'''	

def tests_channels_create_valid_public():
	is_public = True
	name = z
	token = x

	## This should produce no errors:
	channels_create(token, name, is_public)

def tests_channels_create_valid_private():
	is_public = False
	name = z
	token = x

	## This should produce no errors:
	channels_create(token, name, is_public)

def tests_channels_create_name_over_twenty():
	is_public = True
	name = y
	token = x

	## This should produce a ValueError as name is above 20 chars long:
	with pytest.raises(ValueError):
		channels_create(token, name, is_public)

def tests_channels_create_token_invalid():
	'''
	is_public = True
	name = z
	token = not x

	## This should produce a ValueError as token is invalid:
	with pytest.raises(ValueError):
		channels_create(token, name, is_public)
	'''	
