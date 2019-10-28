# CuteRobotTest.py
# State Machine pattern using 'if' statements to determine the next state.

import string, sys
from State import State
from StateMachine import StateMachine
from PersonAction import PersonAction
from MiscFunctions import *

# States
class Idle(State):
    def run(self):
        print("Robot dances")
    def next(self, input):
        if input == PersonAction.appears:
            # Call function to see if person is known, return a number corresponding to the name or -1 if they are unknown and use a lookup function to say hello
            personVal = knownPerson()
            if (personVal != -1):
                sayHelloTo(personVal)
            return CuteRobot.watchPerson
        return CuteRobot.idle

class WatchPerson(State):
    def run(self):
        print("Robot watches person")
    def next(self, input):
        # Call function to try and answer the question
        validQuestion = questionValidity()
        if (input == PersonAction.asksQuestion and validQuestion == True):
            return CuteRobot.answerQuestion
        if (input == PersonAction.asksQuestion and validQuestion == False):
            return CuteRobot.error
        if (input == PersonAction.leaves):
            return CuteRobot.idle
        return CuteRobot.watchPerson

class AnswerQuestion(State):
    def run(self):
        # Call function to actually answer question
        answerQuestion()
        print("Robot answers question")
    def next(self, input):
        if (input == PersonAction.leaves):
            return CuteRobot.idle
        return CuteRobot.watchPerson

class Error(State):
    def run(self):
        print("Robot states some error")
    def next(self, input):
        if (input == PersonAction.leaves):
            return CuteRobot.idle
        return CuteRobot.watchPerson

class CuteRobot(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, CuteRobot.idle)

# Static variable initialization:
CuteRobot.idle = Idle()
CuteRobot.watchPerson = WatchPerson()
CuteRobot.answerQuestion = AnswerQuestion()
CuteRobot.error = Error()

personMoves = map(str.strip,
  open("PersonMoves.txt").readlines())

CuteRobot().runAll(personMoves)
