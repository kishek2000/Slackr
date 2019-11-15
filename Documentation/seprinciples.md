Things to include and talk about:

1) DESIGN SMELLS:

- Rigidity
- Fragility
- Immobility
- Viscosity
- Opacity
- Needless complexity
- Needless repetition
- Coupling

2) DESIGN PRINCIPLES (How our code is):

- Extensible
- Reusable
- Maintainable
- Understandable
- Testable

3) KISS

4) ENCAPSULATION

5) TOP-DOWN THINKING

6) SINGLE RESPONSIBILITY PRINCIPLE

##Standup Changes:

Initially standup was specified to have a duration of 15 minutes. The spec then changed to allow
for a standup of a specified length. Initally whenever time was specified in the standup functions,
it was coded to be fixed to 15 minutes. This was changed to be variable. For example, initally the standup function contained lines of code such as 'threading.Timer(60 * 15, end_standup, [channel_id])'. Each of these lines were 
changed to the following, 'threading.Timer(length, end_standup, [channel_id])' where length was in seconds. 

As the functions were changed, the tests had to changed as well to test for a variable time. The flask wrapping was
to be modified to reflect the changes as well.

A new function for standup was specified to be implemented called standup_active. This returned time_finish. To be
able to return this, we had to store the time_finish in all_channel_messages so that it could be retrieved with the
channel_id which was passed into the function.

##Auth/Standup Changes:

It was observed that other that a lot of conditions such as 'check_token_in_channel' were to be met for functions to perform the required tasks otherwise errors were thrown. These conditions were wrapped in decorators so that functions performed only the tasks which were required from them. E.g. The standup_start function will now simply start a standup rather than checking whether or not a standup can be started or not (checked in decorator). **kwargs was used for decorators with parameters of functions having default values of None. Overall, this allowed the code in functions to be more readable and understandable. The use of decorators however reduced coverage branching scores. Initially for example, in the auth_login function, there is a loop which searches for a user and if not found a ValueError is raised that the provided login details are not of a registered user. However, a valid user check has already been done in the decorator for the function. This means that a user will always be successfully found in the auth_login loop which searches for a user. Since a user is always successfully found in the loop, the loop is never completed and hence the coverage branch will throw an error stating that the loop was never completed. However, for cleaner, understandable and non redundant code the small amount of the coverage branch score was sacrificed and overall was used a guide of good coding practices. 

Functions in both function and test files were each given docstrings to briefly describe them. This would add to the codes understandability if referred to at a future date as each function has been described. Further, intially all the contents of files rather than the required contents were imported. This created inefficiant code and was changed to only import the required functions from other files. Code style was further improved by improving variable names, removing trailing whitespaces and breaking down long lines. This brought up our overall pylint scores which were in the negatives at the start of the iteration.

##Message Changes:
Followed PEP guidelines more closely:
    Moved standard library imports above custom imports (eg. import sys above from helper_functions)
    Eliminated spaces on empty lines
    Changed == None to is None
    Changed == False to Not
    Removed == True
    Changed constant name valid_reacts to VALID_REACTS
    Added docstrings to the start of functions briefly explaining their purpose
    Added header in message_functions identifying who wrote it, what functions are in it, and sub-functions
    Declared a list just before using it to prevent lines from being too long.
    Split import from helper_functions over multiple lines to make it more readable.

Moved checks that appear in more than one function to a decorator.
Added support for kwargs

