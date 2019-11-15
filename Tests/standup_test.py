'''
This file contains tests for the standup related functions
'''
import datetime
import time
import pytest
import sys
sys.path.append('server/')
from functions.standup_functions import standup_start, standup_active, standup_send
from functions.helper_functions import (add_to_standup_queue,
                                        reset_data)
from functions.channel_functions import channels_create, channel_join
from functions.auth_functions import auth_register
from functions.Errors import AccessError

#################################################################################
##                              STANDUP TESTS                                  ##
#################################################################################

@pytest.fixture
def _setup():

    reset_data()

    user_1_details = auth_register(email="PokemonMaster@gmail.com", 
                                   password="validP@sswrd1",
                                   name_first="Ash",
                                   name_last="Ketcham")
    user_2_details = auth_register(email="TheRealPokemonMaster@gmail.com", 
                                   password="ValidP@sswordRocks1",
                                   name_first="Gary", 
                                   name_last="Oak")
    user_3_details = auth_register(email="FreddieMercury@gmail.com", 
                                   password="We@reTheChampions123",
                                   name_first="Freddie",
                                   name_last="Mercury")


    user_1_created_channel_id = channels_create(token=user_1_details['token'],
                                                name="ValidChannelName", 
                                                is_public=True)

    return {'user_1_u_id': user_1_details['u_id'], 'user_1_token' : user_1_details['token'],
            'user_2_u_id': user_2_details['u_id'], 'user_2_token' : user_2_details['token'],
            'user_3_u_id': user_3_details['u_id'], 'user_3_token' : user_3_details['token'],
            'channel_created_by_user_1' : user_1_created_channel_id}


#################################################################################
##                           TESTING standup_start                             ##
#################################################################################

def test_standup_start_correct_details(_setup):
    '''Test for standup_start with correct details provided'''
    user_1_token = _setup['user_1_token']

    channel_id = _setup['channel_created_by_user_1']

    #Should produce no errors
    standup_start(token=user_1_token, channel_id=channel_id, length=60)

def test_standup_invalid_helpers(_setup):
    '''Test for standup helpers with incorrect details provided'''

    assert add_to_standup_queue(-1, "hi") == {}

def test_standup_attempt_to_start_already_active_standup(_setup):
    '''Test for standup_start when another standup already active in channel'''
    user_1_token = _setup['user_1_token']

    channel_id = _setup['channel_created_by_user_1']

    #Should produce no errors
    standup_start(token=user_1_token, channel_id=channel_id, length=60)
    
    print(standup_active(token=user_1_token, channel_id=channel_id)['standup_active'])
    #Should produce ValueError as standup is already active
    with pytest.raises(ValueError):
        standup_start(token=user_1_token, channel_id=channel_id, length=60)


def test_standup_start_nonexistant_channel(_setup):
    '''Test for standup_start in nonexistant channel'''
    user_1_token = _setup['user_1_token']

    channel_id = -1

    #Should produce ValueError as channel with channel_id = -1 does not exist
    with pytest.raises(ValueError):
        standup_start(token=user_1_token, channel_id=channel_id, length=60)


def test_standup_start_unauthorised_user_access(_setup):
    '''Test for standup_start with unautherised user'''
    user_2_token = _setup['user_2_token']

    channel_id = _setup['channel_created_by_user_1']

    #Should produce AccessError as the user is not a member of the channel
    with pytest.raises(AccessError):
        standup_start(token=user_2_token, channel_id=channel_id, length=60)


def test_standup_start_time_finish_greater_than_time_current(_setup):
    '''Testing standup_start and checking for correct time difference'''
    time_current = datetime.datetime.now()

    user_1_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']

    time_finish = standup_start(token=user_1_token, channel_id=channel_id, length=60)

    #Testing if time_finish is greater than the time_current
    assert (time_finish > time_current) is True


def test_standup_start_correct_time_difference_1_minute(_setup):
    '''Testing standup_start and checking for correct time difference of 1 minute'''
    time_current = datetime.datetime.now()

    user_1_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']

    time_finish = standup_start(token=user_1_token, channel_id=channel_id, length=60)

    time_difference = time_finish - time_current

    #Testing if time_finish has a 1 minute differnce in time from time_current
    assert (time_difference.seconds/60) == 1

def test_standup_start_correct_time_difference_3_minute(_setup):
    '''Testing standup_start and checking for correct time difference of 3 minutes'''
    time_current = datetime.datetime.now()

    user_1_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']

    time_finish = standup_start(token=user_1_token, channel_id=channel_id, length=180)

    time_difference = time_finish - time_current

    #Testing if time_finish has a 15 minute differnce in time from time_current
    assert (time_difference.seconds/60) == 3

def test_standup_start_correct_time_difference_15_minute(_setup):
    '''Testing standup_start and checking for correct time difference of 15 minutes'''
    time_current = datetime.datetime.now()

    user_1_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']

    time_finish = standup_start(token=user_1_token, channel_id=channel_id, length=60*15)

    time_difference = time_finish - time_current

    #Testing if time_finish has a 15 minute differnce in time from time_current
    assert (time_difference.seconds/60) == 15

#################################################################################
##                           TESTING standup_active                            ##
#################################################################################

def test_standup_active_valid(_setup):
    '''Testing standup_active with active standup'''
    #Start the standup on the channel with channel id 'channel_id_user_1'

    user_token = _setup['user_1_token']
    channel_id_1 = _setup['channel_created_by_user_1']
    standup_start(token=user_token, channel_id=channel_id_1, length=60)

    #Should return true

    assert standup_active(token=user_token, channel_id=channel_id_1)['standup_active'] is True


def test_standup_active_invalid_channel(_setup):
    '''Testing standup_active with invalid channel'''
    #Start the standup on the channel with channel id 'channel_id_user_1'

    user_token = _setup['user_1_token']
    channel_id_1 = _setup['channel_created_by_user_1']
    standup_start(token=user_token, channel_id=channel_id_1, length=60)

    channel_id_2 = -1

    #Since channel is nonexistant and hence invalid
    with pytest.raises(ValueError):
        standup_active(token=user_token, channel_id=channel_id_2)


def test_standup_active_user_not_in_channel(_setup):
    '''Testing standup_active with user not in the channel of the standup'''
    #Start the standup

    user_1_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']
    standup_start(token=user_1_token, channel_id=channel_id, length=60)


    #Should produce AccessError as the user is not a member of the channel

    user_3_token = _setup['user_3_token']

    with pytest.raises(AccessError):
        standup_active(token=user_3_token, channel_id=channel_id)

def test_standup_active_end_of_standup(_setup):
    '''Testing standup_active after standup's completion'''
    #Start the standup

    user_1_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']
    standup_start(token=user_1_token, channel_id=channel_id, length=10)

    #Wait till standup ends
    time.sleep(11)

    assert(standup_active(token=user_1_token, channel_id=channel_id) == {'standup_active' : False,
                                                        'time_finish' : None})

def test_standup_active_correct_time_difference(_setup):
    '''Testing standup_active after standup's completion'''
    #Start the standup

    user_1_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']
    time_finish = standup_start(token=user_1_token, channel_id=channel_id, length=60)

    assert standup_active(token=user_1_token, channel_id=channel_id)['time_finish'] == time_finish


#################################################################################
##                           TESTING standup_send                              ##
#################################################################################

def test_standup_send_valid(_setup):
    '''Testing standup_send with valid details'''
    user_1_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']

    #add registered_user_2 to the channel
    user_2_token = _setup['user_2_token']
    channel_join(token=user_2_token, channel_id=channel_id)

    #registered_user_1 starts the standup

    standup_start(token=user_1_token, channel_id=channel_id, length=60)

    #Should produce no error as a valid message is sent by both registered_users during the standup

    message = "This is a valid message"

    standup_send(token=user_1_token, channel_id=channel_id, message=message)
    standup_send(token=user_2_token, channel_id=channel_id, message=message)

def test_standup_send_nonexistant_channel(_setup):
    '''Testing standup_send with nonexistant channel'''
    #Start the standup on the channel with channel id 'channel_id_user_1'

    user_token = _setup['user_1_token']
    channel_id_1 = _setup['channel_created_by_user_1']
    standup_start(token=user_token, channel_id=channel_id_1, length=60)

    #Should produce ValueError as channel with channel_id = -1 does not exist

    channel_id_2 = -1

    message = "This is a valid message"

    with pytest.raises(ValueError):
        standup_send(token=user_token, channel_id=channel_id_2, message=message)

def test_standup_send_message_too_long(_setup):
    '''Testing standup_send with message over 1000 characters'''
    #Start the standup

    user_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']
    standup_start(token=user_token, channel_id=channel_id, length=60)

    #Should produce ValueError as the message is greater than 1000 characters

    message = "x" * 1001

    with pytest.raises(ValueError):
        standup_send(token=user_token, channel_id=channel_id, message=message)

def test_standup_send_unauthorised_user(_setup):
    '''Testing standup_send with unauthorised user'''
    #Start the standup

    user_1_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']
    standup_start(token=user_1_token, channel_id=channel_id, length=60)


    #Should produce AccessError as the user is not a member of the channel

    user_3_token = _setup['user_3_token']
    message = "This is a valid message"

    with pytest.raises(AccessError):
        standup_send(token=user_3_token, channel_id=channel_id, message=message)

def test_standup_send_standup_time_finished_5_seconds(_setup):
    '''Testing standup_send by attempting to send message after completion of the standup'''
    #Start the standup

    user_token = _setup['user_1_token']
    channel_id = _setup['channel_created_by_user_1']
    standup_start(token=user_token, channel_id=channel_id, length=5)

    #Sleep 6 seconds

    time.sleep(6)

    #Standup time should be finished so now sending a message to the standup should produce
    #an AccessError even if the user sending a message to the standup belongs to the channel

    message = "This is a valid message"

    with pytest.raises(ValueError):
        standup_send(token=user_token, channel_id=channel_id, message=message)

