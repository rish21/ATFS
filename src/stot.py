#!python
# coding: utf-8

# Imports
import speech_recognition as sr 

def get():

	r = sr.Recognizer() 

	try: 
		with sr.Microphone() as source2: 
			
			r.adjust_for_ambient_noise(source2, duration=0.2) 
			
			audio2 = r.listen(source2) 
			
			text = r.recognize_google(audio2) 
			text = text.lower() 
		
	except sr.RequestError as e: 
		print("Could not request results; {0}".format(e)) 
		
	except sr.UnknownValueError: 
		print("unknown error occured") 

	return text


if __name__ == '__main__':

	text = get()
	print(text)