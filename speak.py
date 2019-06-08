import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 125)
#engine.setProperty('voice', voices[1].id)
#engine.say("C")
#engine.say("a")
voices = engine.getProperty('voices')


engine.setProperty('voice', "croatian")
engine.say("radi li i z č,đ")
engine.runAndWait()
engine.stop()