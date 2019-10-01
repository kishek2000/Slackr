import pytest

######TESTS FOR auth_login#######

'''
Assume these are the usernames and passwords for existing slackr users

1) Username: sorakumar@gmail.com
   Password: SoraIsGreat413
   
2) Username: PikachuEatsSquirtle@hotmail.com
   Password: 123PokemonDontEatPokemon123

'''

def test_auth_login_correct_details():

    email = "sorakumar@gmail.com"
    password = "SoraIsGreat413"
    
    #Should produce no errors
    auth_login(email, password)
    
    
def test_auth_login_invalid_email():

    email = "sorakumarm"
    password = "SoraIsGreat413"
    
    #Should produce ValueError as an invalid email is provided
    with pytest.raises(ValueError):
        auth_login(email, password)
        
        
def test_auth_login_email_not_registered():

    email = "soraDesai@gmail.com"
    password = "SoraIsGreat413"
    
    #Should produce ValueError as an invalid email entered does not belong to a user
    with pytest.raises(ValueError):
        auth_login(email, password)
          
        
def test_auth_login_incorrect_password():

    email = "PikachuEatsSquirtle@hotmail.com"
    password = "This_Is_Definetely_Not_The_Right_Password"
    
    #Should produce ValueError as an incorrect password is provided
    with pytest.raises(ValueError):
        auth_login(email, password)
        
        
def test_auth_login_email_and_password_mismatch():

    email = "sorakumar@gmail.com"
    password = "123PokemonDontEatPokemon123"
    
    #Should produce ValueError as the password does not match to the email provided, hence is incorrect
    with pytest.raises(ValueError):
        auth_login(email, password)
        
######TESTS FOR auth_logout#######

def test_logout    
