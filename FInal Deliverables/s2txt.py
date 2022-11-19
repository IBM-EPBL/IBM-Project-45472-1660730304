import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
     
with sr.Microphone() as source:
    print("Listening...")
    r.pause_threshold = 1
    audio = r.listen(source,phrase_time_limit=5)
    print("Recognizing...")   
    text = r.recognize_google(audio, language ='en-in')
    print(f"User said: {text.lower()}\n")
    f = open("mod.txt", 'w')
    f.write("Spoken : " + text)
    f.close