#!python
# coding: utf-8

# Imports
import html
import os
from google.cloud import texttospeech

# Additional setup for presentation purposes
#import sys
#import os
#sys.stdout = open(os.devnull, "w")


def ssml_to_speech(ssml_text):

    print("pkg_TtoS - Converting SSML to speech")

    #sys.stdout = sys.__stdout__

    # Setup enviroment and initiliase client
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/home/rishmanju/atfs/documents/static-forest-277817-d4e340a3e881.json'
    client = texttospeech.TextToSpeechClient()

    # Assigns input text
    synthesis_input = texttospeech.types.SynthesisInput(ssml=ssml_text)

    # Configure the voice request (Language, Gender and Voice Type)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-GB',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE,
        name='en-GB-Wavenet-C')

    # Determine the encoding
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Request for text to speech conversion
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # Write the results to a temporary file
    try:
        with open("temp/ttos.mp3", 'wb') as out:
            out.write(response.audio_content)
    except:
        print("ERR - SSML failed to write to file")

    return


def text_to_ssml(input_text):

    print("pkg_TtoS - Converting text to SSML")

    # Replace special characters with HTML Ampersand Character Codes to prevent the API failing
    escaped_lines = html.escape(input_text)

    # Convert text attributes to SSML
    ssml_text = '<speak>{}</speak>'.format(
        escaped_lines.replace('\n', '\n<break time="2s"/>'))

    # Return the concatenated string of ssml script
    return ssml_text


def go(input_text):

    ssml_text = text_to_ssml(input_text)
    ssml_to_speech(ssml_text)

    return


if __name__ == '__main__':

    random = "Hello there, I want to see if this works"
    print(random)
    go(random)
