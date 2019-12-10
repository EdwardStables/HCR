# misc.py

# Greeting function
def greetPerson():
    print("Hello")

# Display question function
def makeQuestion(current_emotion):
    print("Question")
    # if done then set processing flag to false
    """
    ans = 1
    # If response bad then make robot sad for 5 cycles by returning the value to lock with
    if ans < 3:
        return 5
        
    """ 
    # return value is number of seconds to lock the emotion and sad or current emotion
    return (current_emotion, 0)