

##Standup Changes:

Initially standup was specified to have a duration of 15 minutes. The spec then changed to allow
for a standup of a specified length. Initally whenever time was specified in the standup functions,
it was coded to be fixed to 15 minutes. This was changed to be variable. For example, initally the standup function contained lines of code such as 'threading.Timer(60 * 15, end_standup, [channel_id])'. Each of these lines were 
changed to the following, 'threading.Timer(60 * length, end_standup, [channel_id])'. 

As the functions were changed, the tests had to changed as well to test for a variable time. The flask wrapping was
to be modified to reflect the changes as well.

A new function for standup was specified to be implemented called standup_active. This returned time_finish. To be
able to return this, we had to store the time_finish in all_channel_messages so that it could be retrieved with the
channel_id which was passed into the function.
