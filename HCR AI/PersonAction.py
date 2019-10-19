# PersonAction.py
# Defining the actions that a person can do

class PersonAction:
    def __init__(self, action):
        self.action = action
    def __str__(self):
            return self.action
    def __cmp__(self, other):
        return cmp(self.action, other.action)
    # Necessary when __cmp__ or __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        return hash(self.action)

# Static fields; an enumeration of instances:
PersonAction.appears = "person appears"
PersonAction.leaves = "person leaves"
PersonAction.asksQuestion = "person asks question"
