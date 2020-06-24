#!python
# coding: utf-8

# Imports
import speech_recognition as sr 
import json

def get():

	# Initialise
	r = sr.Recognizer() 

	# Recognise speech from microphone input
	try: 
		with sr.Microphone() as source2: 
			
			r.adjust_for_ambient_noise(source2, duration=0.2) 
			
			audio2 = r.listen(source2) 
			
			text = r.recognize_google(audio2) 
			text = text.lower() 

			guisett("microphone", text)
		
	except sr.RequestError as e: 
		print("Could not request results; {0}".format(e)) 
		
	except sr.UnknownValueError: 
		print("unknown error occured") 

	return text


def guisett(key, val):

	# Set GUI LED/Text
    with open('gui.JSON', 'r') as f:
        data = dict(json.load(f))
    
    data[key] = val

    with open('gui.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


if __name__ == '__main__':

	text = get()
	print(text)