# **Software Engineering Design Principles**

When entering the final iterative cycles or sprints of the development of a software product, it is important to ensure that it effectively aligns with core software engineering design principles which ultimately guide us about how to ultimately create an efficient and functional system, that follows these basic design smells and principles:

- Smells: Rigidity, Fragility, Immobility, Viscosity, Opacity, Needless complexity, Needless repetition, Coupling

- Principles: Extensible, Reusable, Maintainable, Understandable, Testable

## Before any refactoring any code, we wanted to extend our already functional system by **adapting the changes required given in the spec, and making sure that it functions.**

Although we encountered bugs in these new changes throughout our refactoring process, we were able to debug these as a team and it was always better to start with functional and refactor together, incase we needed to go back to the original commit where everything functions (however this never happened).

In this final iteration where refactoring has been a core process, there have also been further concepts which we have considered before we pursued our changes. These include the idea of _KISS, DRY, Encapsulation, Top-down thinking_ and finally _Single Responsibility Principle._

## With this long list of principles and guidelines, as a team our main interpretation was to **start simple and slowly build up the way we improve our code and refactor it**.

In light of this, we began by first using pylint which advised us upon:

1. Important errors such as using a proper method of imports
2. Using docstrings to be clear on what each function does
3. Ensuring that we have code that does not extend into too many branches within its execution.

In this trio of interpretation from **pylint** , we immediately enhanced our backend functions for their _readability_ and _maintainability_ as **we fixed our imports to be absolute imports** , and by amending **over-branched code** we improved the ease with which anyone can parse our code.

## Within this interpretation, we extended our efforts into the _understandability_ and _readability_ of our functions by considering the principle that each function should only have one key responsibility.

Most of our functions originally had a main/key section of error checking, and then some also had 2-3 responsibilities/executions from different areas in our overall system. _For example, channel\_messages should have the main responsibility of collecting all sent messages of a channel and returning this in a dictionary, but it also contained an extra processing responsibility of reacts. To amend this, we simply transferred this functionality into a helper function and executed this function within the original channel\_messages when necessary._

This kind of process was supplemented by **pylint** , and then accelerated with our in depth perusing through the code each of us wrote to ultimately follow the _Single Responsibility Principle_ as well as we can, while also following the idea of _Encapsulation_ and _Top-down thinking_ as these are quite similar in that **each function should only commit to what it is required to do with a given input, and then work on this input to reach our output. Only when there are more requirements for the pathway between input and output to work, do we introduce more layers of helper functions.**

Our key method of separating the error checks which we constantly have atop most of our function code was through decorators - defined in our Errors.py file. This ultimately asserted the _extensibility_ and _maintainability_ of our code as it is easier to extend into more functions that want to use the same forms of error checking, and then maintaining our error checking messages can easily be done in one go for the multiple places it is used, through changes in the Errors.py file.

Through our relocation of several functionalities such as helper functions for needless branching and repetition within our function code, and decorators to remove repeated code of error checks, we improved the _viscosity_ of our backend code and consequently, have developed a system that has _very __low__ rigidity_ and _can be easily changed across the full system_.

## Following this process, and throughout the whole iteration, **we extensively exercised the importance of testing any code that we change or write each day.** This involved:

- Using **pytest** and **coverage with branches.** By nature, these executed _integrated and system testing_ since the system is run on the backend functionalities, and any integrated links between them such as channel\_messages and message\_send, or user photos and channel data, are also tested.
- _Constant live testing_ through _frontend tests_, where we can take the place of a user and ensure that their experience from the UI is of **ease and clarity** - especially as we want users to be more than satisfied with their use of the Slackr app.

These allowed us to ensure that the instances of coupling and dependencies within our code are working and not rigid or difficult to change. The most important observation in this constant testing process, was to understand the _fragility_ of our code and system, **and to constantly improve and amend this.** Now as we make changes, **there is very minor impacts in the integrated components concerned, and often the debugging process may have been long, but not a difficult issue to solve.**

## From all these actions which we undertook, **the overall**  **opacity**  **of our code has improved tremendously,** and our data storage system is already a very simply implemented system of lists of dictionaries where the data desired from frontend is the keys of these dictionaries in our backend.

Overall, we have truly given an earnest and humble effort throughout, to maintain a system of code and data that works together in a way that **aligns in the best way possible with the principles of Software Engineering and Design, but all within reason and not for the sake of numbers such as coverage, or pylint scores.**