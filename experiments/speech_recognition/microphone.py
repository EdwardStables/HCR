import time
import speech_recognition as sr

print("Test")

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

#assign to correct hardware-specific index of the microphone
MICROPHONE_INDEX = 1

# obtain audio from the microphone  
r = sr.Recognizer()
r.energy_threshold = 10000
r.pause_threshold = 0.5

m = sr.Microphone(device_index=MICROPHONE_INDEX)

# def callback(recognizer, audio):
#     try:
#         print("Wit Speech Recognition thinks you said " + r.recognize_wit(audio, key="TOUXYZM2RACQGS5ZQRJZQUQ36YK7EQKP"))
#     except sr.UnknownValueError:
#         print("Wit Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Wit Recognition service; {0}".format(e))

# with m as source:
#     r.adjust_for_ambient_noise(source)

# # start listening in the background (note that we don't have to do this inside a `with` statement)
# stop_listening = r.listen_in_background(m, callback)

# print("listening")

# for _ in range(100): time.sleep(0.1)

# print("stopping")

# # calling this function requests that the background listener stop listening
# stop_listening(wait_for_stop=False)

with m as source:  
    print("Please wait. Calibrating microphone...")  
    # listen for 5 seconds and create the ambient noise energy level  
    r.adjust_for_ambient_noise(source, duration=5)
    print("Say something!")
    audio = r.listen(source, timeout = 10.0)  
   
# recognize speech using Sphinx  
try:  
    print("Wit thinks you said '" + r.recognize_wit(audio, key="TOUXYZM2RACQGS5ZQRJZQUQ36YK7EQKP") + "'")  
except sr.UnknownValueError:  
    print("Wit could not understand audio")  
except sr.RequestError as e:  
    print("Wit error; {0}".format(e))  