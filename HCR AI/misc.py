# misc.py

import time

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

def getName():
    time.sleep(3)
    name = "Bob"
    updateNameDatabase(name)
    return name

def updateNameDatabase(name):
    print("updateNameDatabase() not yet implemented.")

def sayHello(event):
    with open("knownPeople.txt") as f:
        knownPeople = f.readlines()
    knownPeople = [x.strip() for x in knownPeople] 

    temp = event.split()[2]

    try:
        personIndex = knownPeople.index(temp)
    except:
        personIndex = -1
    
    if personIndex >= 0:
        say(('Hello ' + knownPeople[personIndex]))
    else:
        say('I don\'t know you, what is your name?')
        name = "Bob"
        knownPeople.append(name)

        with open('knownPeople.txt', 'w') as f:
            for item in knownPeople:
                f.write("%s\n" % item)

        say(('Hello ' + name))

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