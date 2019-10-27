# misc.py

import time
from termios import tcflush, TCIFLUSH
import sys


def getName():
    """
    Clean the input buffer and get a name that's typed in.
    \n(Note: 'tcflush' may only work on Linux)
    """

    tcflush(sys.stdin, TCIFLUSH)
    name = input()
    updateNameDatabase(name)
    return name


def updateNameDatabase(name):
    """
    Take a name and if it isn't a recognised name, add it to the name list.
    """
    
    with open("knownPeople.txt") as f:
        knownPeople = f.readlines()
    f.close()

    knownPeople = [x.strip() for x in knownPeople] 
    if name not in knownPeople:
        knownPeople.append(name)

    with open('knownPeople.txt', 'w') as f:
        for item in knownPeople:
            f.write("%s\n" % item)
    f.close()


def getQuestion():
    """
    Clean the input buffer and get a question that's typed in.
    Check whether the question is valid and assign it a number.
    \n(Note: 'tcflush' may only work on Linux)
    """

    say("What is your question?")
    tcflush(sys.stdin, TCIFLUSH)
    question = input()

    return validQuestion(question)


def validQuestion(question):
    """
    Checks if the question is valid and either returns the idex of the answer or -1 if the question is invalid.
    """

    with open("validQuestions.txt") as f:
        questions = f.readlines()
    questions = [x.strip() for x in questions] 
    f.close()

    if question not in questions:
        return -1
    else:
        return questions.index(question)


def answerQuestion(questionIndex):
    """
    Takes the index of a valid question and answers it.
    """

    with open("validQuestionAnswers.txt") as f:
        answers = f.readlines()
    answers = [x.strip() for x in answers] 
    f.close()
    
    say(answers[questionIndex])


def say(thing):
    """
    Function to simulate the robot saying something.
    """
    
    print('     ', thing, '\n')