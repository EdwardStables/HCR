import speech_recognition as sr

# return found microphone index numbers to select the correct input microphone
def microphone_index_numbers():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

def speech_function(r, m):

    # map keywords with weightings to emotion state
    emotion_dict = {
        "happy": {"hello": 1, "hi": 1, "great": 2, "good": 1, "dance": 2, "joke": 2, "happy": 2, "how are you": 2, "love": 2, "like": 1},
        "sad": {"sad": 2, "horrible": 2, "terrible": 2, "bad": 2, "hate": 2, "stupid" :2},
        "content": {"thank": 2, "content": 2, "thanks": 2, "thank you": 2},
        "thinking": {"how": 1, "why": 2, "what": 2, "where": 2, "when": 2, "help": 2, "think": 2}
    }

    #set of unique keywords present in the emotion dictionary mapping
    emotion_keywords = set(item for sublist in emotion_dict.values() for item in sublist)

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

    while True:
        #initialize emotion scoring for the current iteration of listening
        score = {
            "happy": 0,
            "sad": 0,
            "content": 0,
            "thinking": 0    
        }
        print("-----listen-----")
        with m as source:  
            print("Please wait. Calibrating microphone...")  
            # listen for 5 seconds and create the ambient noise energy level  
            r.adjust_for_ambient_noise(source, duration=5)
            print("Hi, say something!")
            audio = r.listen(source, timeout = 10.0)  
        
        # recognize speech using Sphinx  
        print("-----recog-----")
        try:
            # recognized_words_wit = r.recognize_wit(audio, key="TOUXYZM2RACQGS5ZQRJZQUQ36YK7EQKP")
            # print("Wit thinks you said '" + recognized_words_wit + "'")

            recognized_words = r.recognize_google(audio)
            print("I think you said '" + recognized_words + "'")

            # only store keywords recognized from the input audio string for mapping
            recognized_keywords = [w for w in recognized_words.split() if w in emotion_keywords]

            # iterate through found keywords in the audio for the current iteration
            for w in recognized_keywords:
                # search for key-value pair in emotion dictionary mapping with current keyword
                for k,v in emotion_dict.items():
                    if w in v:
                        # increment score for relevant emotion(s) for current keyword by weighting of keyword
                        score[k] += v[w]

            # recognized_words_sphinx = r.recognize_sphinx(audio)
            # print("Sphinx thinks you said '" + recognized_words_sphinx + "'")  

            print ("I am " + str(max(score, key=score.get)))

        except sr.UnknownValueError:  
            print("Could not understand audio")  
        except sr.RequestError as e:  
            print("Error; {0}".format(e))  


def speech_setup(microphone_index_number, energy_threshold, pause_threshold):
    #assign to correct hardware-specific index of the microphone
    MICROPHONE_INDEX = microphone_index_number

    # obtain audio from the microphone  
    r = sr.Recognizer()

    # minimum audio energy to consider for recording
    # energy_threshold = 8000
    r.energy_threshold = energy_threshold

    # seconds of non-speaking audio before a phrase is considered complete
    # pause_threshold = 0.5
    r.pause_threshold = pause_threshold

    # set to use correct microphone input
    m = sr.Microphone(device_index=MICROPHONE_INDEX, sample_rate=44100)

    speech_function(r, m)

if __name__ == "__main__":
    speech_setup(2,8000, 0.5)


