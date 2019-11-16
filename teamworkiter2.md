TEAMWORK:-

## How often you met, and why you met that often

Meetings were spread out throughout the iteration, every few days on discord and hangouts with daily conversations on messenger. 

Our initial meeting involved discussing team member availability and setting of milestones to be achieved. The milestones set were:- 

* Familiarise with Lectures and Spec (12/10 - 14/10)
* Code Draft - Functions (14/10 - 18/10)
* Style, Flask, Content Meeting (17/10 - 18/10)
* Completed Draft of All Functions (16/10 - 20/10)
* Wrap draft in flask and implement (17/10 - 20/10)
* Style, Flask, Content Meeting (18/10 - 20/10)
* Completed Draft Meeting (19/10 - 20/10)
* Test Implementation (20/10)
* Work on Feedback (21/10 - 22/10)
* Meeting on Updates (23/10)
* Work on Flask (21/10 - 24/10)
* Teamwork (25/10)
* Assurance (26/10)

## What methods you used to ensure that meetings were successful

We planned out our meeting times in advance.
At the start of each meeting, we set out our goals for the meeting and how long we thought it would take. We met at key stages during the project development, when decisions needed to be made or methods discussed as a group. We shared screens with each other using google hangouts, enabling us to share and view one another’s code with ease. We reviewed progress of each member and provided constructive feedback. 

## What steps you took when things did not go to plan during iteration two

We turned to different sources when it came to problems being raised. For internal and team based problems (each person’s workload, making sure each person is on track, etc), we would comment in our group chat on messenger to ensure the and directly resolve the conflict via talking. We also resorted to contacting one another to look at eachothers code if there is a problem.
 
In terms of problems with the front end, team members commonly posted and referred to piazza. This allowed us to directly come into contact with course instructors, and other students who may have a similar problem to us. 

We also had group calls multiple times a week, just as a general checkup to make sure that each person was on track with our schedule. This call also each members to address problems or questions that they had. This was productive as we used an application which allowed screen sharing, enabling each member to express and show what they were talking about.

The core process involved an Agile approach. As seen in the milestones, we first developed our drafts for our functions, in a logical order such that functionality can be tested via our previously written tests from Iteration One. (Eg, we first had auth functionality complete so the fixtures in other function testing which first registered users, can be applied effectively and tested). 

At the absolute crux of our process, we went from:
A:
* Develop function drafts
* Apply tests from Iteration 1
* Reiterate over the function drafts with the changes needed to be made, for failed tests
* Discuss the reason for failures, and explore how to optimise these issues
* Repeat
B:
* Develop flask wrapping drafts
* Apply different testing methods with server and frontend, as explained in Assurance (eg integration and systems testing)
* Reiterate over function drafts and flask drafts with changes needed to be made for the failed tests
* Discuss reasons behind the failures
* Repeat

Our group had daily discussions and checkups throughout this process, within Messenger and some calls, but had 1 main large Google Hangouts call where screensharing is possible, so that we could run through the whole frontend process and functionality, and just test everything. We then went through some topics of discussion which we wanted to clarify with better depth, such as how to understand what is being sent from the server and to debug from that (inspect element). We then had another call with the same platform, after a few iterations of our flask drafts and server testing, where we did another full test and had all basic functionalities ultimately working and functioning with the current version of the frontend, keeping in mind the bugs that are yet to be fixed.

After receiving a requirement change about the timeline for our project, as to the need for frontend functionality, we still used the frontend to confirm most of our functionality, and used Postman or curl otherwise. For example, we confirmed the correct functionality of our standup functions using Postman in our second group Hangouts call. 

Ultimately, this process was long but broken down into achievable shorter term goals, and we all pursued our best efforts and are satisfied with how we have turned out by the end of this iteration, and look forward to the challenge of the next iteration! 

## Details on how you had multiple people working on the same code

It was planned to work on the function for which each team member had written 
tests for. The functions were divided as follows:- 

* Author-> Shoan
* Channel-> Adi
* Message-> Liam
* User Profiles-> Harry
* Standup-> Shoan
* Search-> Harry
* Admin-> Harry

Through the process of writing code, we realised that we could have common helper
functions and made a helper_functions.py file. With this file, any member could
add their helper functions as well as use other member's helper code. 

There was also some overlap when writing functions; both Liam and Adi worked on channel_messages together. When initially working with flask (before front end was removed as a requirement), we all tried to figure out the implementation together for the auth_functions, so that every other member could follow a similar structure when wrapping their functions.



