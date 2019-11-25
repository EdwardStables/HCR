
from states import flag
from stateMachine import StateMachine
import os

robot = StateMachine()

prompt = "\n> "
while True:

    os.system('clear')
    print("")

    robot.event("")

    print("\nCurrent State:", robot.state)
    flag.printFlags()
    
    x = input(prompt)

    if x == "person appears":
        flag.person = True
        prompt = "\n> person "
    elif x == "disappears" or x == "(person disappears)":
        flag.person = False
        prompt = "\n> "
    elif x == "asks question":
        flag.processing = True
        prompt = "\n> their question is "
    elif x == "invalid":
        flag.processing = False
        flag.question = -1
        prompt = "\n> person "
    elif x == "valid":
        flag.processing = False
        flag.question = 10
        prompt = "\n> person "
    elif x == "cancelled":
        flag.processing = False
        flag.question = 1
        prompt = "> person "
    elif x == "quit":
        break

