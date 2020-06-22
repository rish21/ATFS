#!python
# coding: utf-8

# Imports
import html
import os
import json
from google.cloud import texttospeech

# Additional setup for presentation purposes
#import sys
#import os
#sys.stdout = open(os.devnull, "w")


def ssml_to_speech(ssml_text):

    print("pkg_TtoS - Converting SSML to speech")

    #sys.stdout = sys.__stdout__

    # Setup enviroment and instantiate client
    client = texttospeech.TextToSpeechClient()

    # Assigns input text
    synthesis_input = texttospeech.types.SynthesisInput(ssml=ssml_text)

    # Configure the voice request (Language, Gender and Voice Type)
    with open('standard.JSON', 'r') as f:
        data = dict(json.load(f))

    gender = str(data["settings"][0]["gender"])

    if gender == "mail" or gender == "male":
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-GB',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE,
            name='en-GB-Wavenet-B')
    elif gender == "female":
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-GB',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE,
            name='en-GB-Wavenet-A')

    # Determine the encoding
    audio_config = texttospeech.types.AudioConfig(
        speaking_rate=float(data["settings"][0]["speaking_rate"]),
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

    # Request for text to speech conversion
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # Write the results to a temporary file
    try:
        with open("temp/audio/ttos.wav", 'wb') as out:
            out.write(response.audio_content)
    except:
        print("ERR - SSML failed to write to file")

    return


def text_to_ssml(input_text, equ):

    print("pkg_TtoS - Converting text to SSML")

    convert = html.escape(input_text)

    if equ == True:
        
        # Greek Letters
        convert = convert.replace('\varepsilon', ' epsilon ')
        convert = convert.replace('\vartheta', ' theta ')
        convert = convert.replace('\mu', ' mew ')
        convert = convert.replace('\nu', ' new ')
        convert = convert.replace('\\xi', ' sigh ')
        convert = convert.replace('\varrho', ' rho ')
        convert = convert.replace('\varphi', ' phi ')

        # Other Symbols
        convert = convert.replace('\infty', ' infinity ')
        convert = convert.replace('\Re', ' real ')
        convert = convert.replace('\nabla', ' differential ')
        convert = convert.replace('\mu', ' mew ')
        convert = convert.replace('\neg', ' negative ')
        convert = convert.replace('\Im', ' imaginary ')
        convert = convert.replace('\nexists', ' does not exist ')
        convert = convert.replace('\varnothing', ' nothing ')
        convert = convert.replace('\cdots', ' and so on ')
        convert = convert.replace('\surd', ' square root of <break time="0.5s"/> ')
        convert = convert.replace('\angle', ' an angle of ')

        # Operations
        convert = convert.replace('\div', ' divided by ') 
        convert = convert.replace('\cup', ' union ')
        convert = convert.replace('\cap', ' intersection ')
        convert = convert.replace('\subset', ' is a proper subset of ')
        convert = convert.replace('\not\subset', ' is not a proper subset of ')
        convert = convert.replace('\subseteq', ' is a subset of ')
        convert = convert.replace('\nsubseteq', ' is not a subset of ')
        convert = convert.replace('\supset', ' is a proper super of ')
        convert = convert.replace('\not\supset', ' is not a proper super of ')
        convert = convert.replace('\supseteq', ' is a super of ')
        convert = convert.replace('\nsupseteq', ' is not a super of ')

        convert = convert.replace('\neq', ' is not equal to ')
        convert = convert.replace('\ne', ' is not equal to ')
        convert = convert.replace('\nless', ' is not less than ')
        convert = convert.replace('\leqslant', ' is less than or equal to ')
        convert = convert.replace('\nleq', ' is neither less than or equal to ')
        convert = convert.replace('\nleqslant', ' is neither less than or equal to ')
        convert = convert.replace('\geq', ' greater than or equal to ')
        convert = convert.replace('\gtr', ' is not greater than ')
        convert = convert.replace('\ngtr', ' is not greater than ')
        convert = convert.replace('\geqslant', ' is greater than or equal to ')
        convert = convert.replace('\ngeq', ' is neither greater than or equal to ')
        convert = convert.replace('\ngeqslant', ' is neither greater than or equal to ')

        convert = convert.replace('\sinh', ' sine ')
        convert = convert.replace('\cosh', ' cosine ')
        convert = convert.replace('\tanh', ' cosine ')

        convert = convert.replace('\int', ' the integral of <break time="0.5s"/> ')
        convert = convert.replace('\sum', ' the sum of <break time="0.5s"/> ')
        convert = convert.replace('\prod', ' the product of <break time="0.5s"/> ')
        convert = convert.replace('\lim_', ' with a lower limit of <break time="0.5s"/> ')
        convert = convert.replace('_{', ' with a lower limit of <break time="0.5s"/> ')
        convert = convert.replace('^', ' to the power of ')

        convert = convert.replace('\in', ' belongs to <break time="0.5s"/> ')
        convert = convert.replace('\perp', ' is perpendicular to ')
        convert = convert.replace('\notin', ' does not belong to <break time="0.5s"/> ')
        convert = convert.replace('\simeq', ' is similarly equal to <break time="0.5s"/> ')
        convert = convert.replace('\sim', ' is similar to <break time="0.5s"/> ')
        convert = convert.replace('\approx', ' is approximately equal to ')
        convert = convert.replace('\equiv', ' is equivalent to <break time="0.5s"/> ')
        convert = convert.replace('\cong', ' is congruent to <break time="0.5s"/> ')
        convert = convert.replace('\propto', ' is proportional to <break time="0.5s"/> ')
        
    ssml_text = '<speak>{}</speak>'.format(convert)

    guisett("speech", ssml_text)

    return ssml_text


def guisett(key, val):

    with open('gui.JSON', 'r') as f:
        data = dict(json.load(f))
    
    data[key] = val

    with open('gui.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


def go(input_text, equ):

    ssml_text = text_to_ssml(input_text, equ)
    ssml_to_speech(ssml_text)

    return 


if __name__ == '__main__':

    random = "\int x^2 dx"
    go(random, True)
