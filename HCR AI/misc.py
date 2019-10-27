# misc.py

import time
from termios import tcflush, TCIFLUSH
import sys

def getName():
    """
    Clean the input buffer and get a name that's typed in
    \n(Note, may only work on Linux)
    """

    tcflush(sys.stdin, TCIFLUSH)
    name = input()
    updateNameDatabase(name)
    return name

def updateNameDatabase(name):
    """
    Take a name and if it isn't a recognised name, add it to the name list
    """
    
    with open("knownPeople.txt") as f:
        knownPeople = f.readlines()
    knownPeople = [x.strip() for x in knownPeople] 

    if name not in knownPeople:
        knownPeople.append(name)

    with open('knownPeople.txt', 'w') as f:
        for item in knownPeople:
            f.write("%s\n" % item)

def validQuestion(question):
    temp = question.split()[2:]
    questions = [
        ['1'], 
        ['1', '0'],
        ['2'],
        ['3'],
        ['4'],
        ['5']
        ]
    try:
        return questions.index(temp)
    except:
        return -1

def answerQuestion(question):
    if question == 0:
        say("Answer: Yes")
    elif question == 1:
        say("Answer: No")
    elif question == 2:
        say("Answer: I don't know")

def returnError():
    say("Invalid Question.")

def parseEvent(event):
    temp = event.split()
    if temp[0:2] == ['person', 'appears']:
        return "person_appears"
    if temp[0:2] == ['person', 'leaves']:
        return "person_leaves"
    if temp[0:2] == ['person', 'asks']:
        return "person_asks"

def updatePosition():
    print("Update position\n")

def say(thing):
    print('     ', thing, '\n')