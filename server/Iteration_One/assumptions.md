================ Assumptions Document ================

The following document of Assumptions will be categorised into the
different stages of the project: that is, Iterations 1-3. 

==== Iteration One ====

This iteration will be grouped into the assumptions made in each category
of functions, namely:
	- auth_*
	
	- channel(s)_*

	- message_*
	
    - user_*
    
    - standup_*
    
    - search
    
    - admin_userpermission_change  


auth_*:
	
    - Assume an accepted password used in the logging in and registration has the following requirements 
      (A function called is_valid_password() will check against these requirements and return either
      True or False) :-
    
    			- Passoword length between 5 and 20 characters inclusive
    			- At least 1 upper character
    			- At least 1 lower case character
    			- At least 1 number
    			- At least 1 special character
      
    - Assume we have a function token_is_valid() which returns either True if token is active
	 	and False inactive
	- Similalry we have a funtion, u_id_is_valid() which returns either True or False
    - For the use of auth_passwordreset_reset and its testing, assume that get_reset_code() provides 
      a valid reset code
    - Assume that -1 is an invalid reset_code 
    
channel_*:
    - Within channel_details, we intepret from the spec, and 'assume', that the 
    	function returns a dictionary that provides the channel name as a string, 
		then a list of the owners ids, then a list of all members ids.
	- For channel_messages, we assume there is some function within  channel_messages() 
    	that promptsusers for an input of some start value, called message_start_index().
    - We also assume there is some function within channel_messages() that provides 
		us the number of messages in the channel, as long as the token given pertains 
		to a user that is a member of the channel, called total_channel_messages().
    - In the testing of channel_messages, we assume that message_send has complete functionality.
    - Although not fully implemented in Iteration One, we plan to consider the addition
		of a test in channel_leave where we check the previous member list, and post 
		member list using channel_details. The assumption will be that channel_details
		is fully functioning in this usage (with valid arguments given to the function).
	- In our testing of channel_removeowner, when we add an extra owner of our created
		public and private channels made in the first fixture 'setup' in channel_tests, 
		we are assuming that the function channel_addowner() adds a user to a channel, and also 
		then makes them an owner; that is, they are a member of the channel and an owner of it. 
	- For the testing of channels_create, we are assuming that we will create some function
		that prompts users for an input of some channel name, called get_channel_name()
    - For the testing of channels_create, we are also assuming that we will create some function
		that prompts users for an input of 'Yes' or 'No' for the option of making a public or 
		private channel, called get_public_status() (it returns True or False)


message_*:
    - Assuming trying to send an empty string will send no message
    - Assuming trying to send a string of spaces will send no message
    - Assuming sending a string containing special characters (\0, \n, \b) will send the characters as is
    	This would be consistent with Slack
    - Assuming message_send_later and message_edit have the same 1000 character limit as message_send
    - Assuming testing computer is fast enough to perform sequential commands in less than a second
    - Assuming the empty string is an invalid token
    - Assuming no valid id's will be -1
    - Assuming helper functions return valid tokens
    - Assuming channels_create, channel_invite, channel_join, channel_leave and channel_message is working
    - Assuming sending the empty string will throw a value error
    - Assuming AccessError has been defined
    - Assuming the stored time sent for message_send_later will be the time it was posted to the channel
    - There is currently no specified way to store the reacts and pins, so testing these is going to be difficult
    - Assuming a valid react id is 1 and 2
    - Assuming only one person can use each react_id on each message (probably a mistake with the specs)
    - Assuming messages sent later can only be removed, edited, reacted and pinned once they've actually been posted
    - Assuming all message functions will throw an access error without a valid token
    - Assuming anyone can unreact any existing react on a message (regardless of if they made it)
    - Assuming there is a function that tests if a channel has no messages in it called channel_is_empty
    - Assuming message functions are implemented in the order they are in the test file
    - Assuming editing a message ONLY changes the messasge, and not time_created, is_read, u_id, or message_id
    
user_*:
	- Assuming an invalid token will cause raise an error
    - Assuming an empty string will raise an error
    - Assuming an invalid u_id will raise an error
    - Handle should not be the same as one that already exists
