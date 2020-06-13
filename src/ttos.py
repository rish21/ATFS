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
        convert = convert.replace('\varepsilon', 'epsilon')
        convert = convert.replace('\vartheta', 'theta')
        convert = convert.replace('\mu', 'mew')
        convert = convert.replace('\nu', 'new')
        convert = convert.replace('\\xi', 'sigh')
        convert = convert.replace('\varrho', 'rho')
        convert = convert.replace('\varphi', 'phi')

        # Other Symbols
        convert = convert.replace('\infty', 'infinity')
        convert = convert.replace('\Re', 'real')
        convert = convert.replace('\nabla', 'differential')
        convert = convert.replace('\mu', 'mew')
        convert = convert.replace('\neg', 'negative')
        convert = convert.replace('\Im', 'imaginary')
        convert = convert.replace('\nexists', 'does not exist')
        convert = convert.replace('\varnothing', 'nothing')
        convert = convert.replace('\cdots', ' and so on ')
        convert = convert.replace('\surd', 'square root of')
        convert = convert.replace('\angle', 'an angle of')

        # Operations
        convert = convert.replace('\div', 'divided by') 
        convert = convert.replace('\cup', 'union')
        convert = convert.replace('\cap', 'intersection')
        convert = convert.replace('\subset', 'is a proper subset of')
        convert = convert.replace('\not\subset', 'is not a proper subset of')
        convert = convert.replace('\subseteq', 'is a subset of')
        convert = convert.replace('\nsubseteq', 'is not a subset of')
        convert = convert.replace('\supset', 'is a proper super of')
        convert = convert.replace('\not\supset', 'is not a proper super of')
        convert = convert.replace('\supseteq', 'is a super of')
        convert = convert.replace('\nsupseteq', 'is not a super of')

        convert = convert.replace('\neq', 'is not equal to')
        convert = convert.replace('\ne', ' is not equal to')
        convert = convert.replace('\nless', 'is not less than')
        convert = convert.replace('\leqslant', 'is less than or equal to')
        convert = convert.replace('\nleq', 'is neither less than or equal to')
        convert = convert.replace('\nleqslant', 'is neither less than or equal to')
        convert = convert.replace('\geq', 'greater than or equal to')
        convert = convert.replace('\gtr', ' is not greater than')
        convert = convert.replace('\ngtr', 'is not greater than')
        convert = convert.replace('\geqslant', 'is greater than or equal to')
        convert = convert.replace('\ngeq', 'is neither greater than or equal to')
        convert = convert.replace('\ngeqslant', 'is neither greater than or equal to')

        convert = convert.replace('\in', 'belongs to')
        convert = convert.replace('\perp', ' is perpendicular to')
        convert = convert.replace('\notin', 'does not belong to')
        convert = convert.replace('\simeq', 'is similarly equal to')
        convert = convert.replace('\sim', 'is similar to')
        convert = convert.replace('\approx', 'is approximately equal to')
        convert = convert.replace('\equiv', 'is equivalent to')
        convert = convert.replace('\cong', 'is congruent to')
        convert = convert.replace('\propto', 'is proportional to')

        convert = convert.replace('\sinh', 'sine')
        convert = convert.replace('\cosh', 'cosine')
        convert = convert.replace('\tanh', 'cosine')

        convert = convert.replace('\int', 'the integral of')
        convert = convert.replace('\sum', 'the sum of')
        convert = convert.replace('\prod', 'the product of')
        convert = convert.replace('\lim_', 'with a lower limit of')
        convert = convert.replace('_{', 'with a lower limit of')
        

    ssml_text = '<speak>{}</speak>'.format(convert)

    return ssml_text


def go(input_text, equ):

    ssml_text = text_to_ssml(input_text, equ)
    ssml_to_speech(ssml_text)

    return 


if __name__ == '__main__':

    random = "Hello there, I want to see if this works"
    go(random, False)
