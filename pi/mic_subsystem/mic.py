import speech_recognition as sr
from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody

class mic(subsystem):

    def __init__(self):
        super().__init__("mic", "id_only")

        # map keywords with weightings to emotion state
        self.emotion_dict = {
            "happy": {"hello": 1, "hi": 1, "great": 2, "good": 1, "dance": 2, "joke": 2, "happy": 2, "how are you": 2, "love": 2, "like": 1},
            "sad": {"sad": 2, "horrible": 2, "terrible": 2, "bad": 2, "hate": 2},
            "content": {"thank": 2, "content": 2, "thanks": 2, "thank you": 2},
            "thinking": {"how": 1, "why": 2, "what": 2, "where": 2, "when": 2, "help": 2, "think": 2}
        }

        #set of unique keywords present in the emotion dictionary mapping
        self.emotion_keywords = set(item for sublist in self.emotion_dict.values() for item in sublist)

    def _run(self):
        self.speech_setup(2, 10000, 0.5)
        while True:
            self.mic_loop()

    def speech_setup(self, mic_index, energy_threshold, pause_threshold):
        #assign to correct hardware-specific index of the microphone
        MICROPHONE_INDEX = mic_index

        # obtain audio from the microphone  
        self.r = sr.Recognizer()

        # minimum audio energy to consider for recording
        # energy_threshold = 8000
        self.r.energy_threshold = energy_threshold

        # seconds of non-speaking audio before a phrase is considered complete
        # pause_threshold = 0.5
        self.r.pause_threshold = pause_threshold


        # set to use correct microphone input
        self.m = sr.Microphone(device_index=MICROPHONE_INDEX, sample_rate=44100)

    def mic_loop(self):
        #initialize emotion scoring for the current iteration of listening
        score = {
            "happy": 0,
            "sad": 0,
            "content": 0,
            "thinking": 0    
        }

        with self.m as source:  
            print("Please wait. Calibrating microphone...")  
            # listen for 5 seconds and create the ambient noise energy level  
            self.r.adjust_for_ambient_noise(source, duration=2)
            print("Hi, say something!")
            audio = self.r.listen(source, timeout = 5)  
        
        # recognize speech using Sphinx  
        try:
            # recognized_words_wit = r.recognize_wit(audio, key="TOUXYZM2RACQGS5ZQRJZQUQ36YK7EQKP")
            # print("Wit thinks you said '" + recognized_words_wit + "'")

            recognized_words = self.r.recognize_google(audio)
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

            #print ("I am " + str(max(score, key=score.get)))
            self.send_emotion(max(score, key=score.get))

        except sr.UnknownValueError:  
            print("Could not understand audio")  
        except sr.RequestError as e:  
            print("Error; {0}".format(e))  
    
    def send_emotion(self, emotion):
        self.send_message("ai", "speech_emotion", emotion)
