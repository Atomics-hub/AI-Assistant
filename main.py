# This is a script for a text to speech bot that uses openai's chatgpt


# Imports
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import openai
import time


listening = False
wake_word = 'Hello'
shutoff_word = 'That is all'
last_interaction_time = time.time()
api_key = 'YOUR API KEY'
openai.api_key = api_key
load_dotenv()
rec = sr.Recognizer()
messages = []


# Function to get messages to gpt
def talk_to_gpt(message):
    model = 'gpt-3.5-turbo'
    response = openai.ChatCompletion.create(model=model, messages=message, max_tokens=500, n=1, stop=None, temperature=0.8)
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


# Function to speak with the specified voice
def speak(command, voice_id="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"):
    engine = pyttsx3.init()

    # Set the selected voice by voice ID
    engine.setProperty('voice', voice_id)

    engine.say(command)
    engine.runAndWait()


# Function to get speech input
def get_text():
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=1.0)
        print('I am listening...')
        try:
            audio = rec.listen(source, timeout=5)
            text = rec.recognize_google(audio)
            print(text)
            return text
        except sr.WaitTimeoutError:
            print('No speech detected within the timeout.')
        except sr.UnknownValueError:
            print('Google Web Speech API could not understand audio.')
        except sr.RequestError as e:
            print('Could not request results from Google Web Speech API; {0}'.format(e))
        return ""


# Function to reset the conversation
def reset_conversation():
    global listening
    global last_interaction_time
    listening = False
    last_interaction_time = time.time()
    return []


# To keep the conversation going
first_interaction = True
while True:
    text = get_text()
    if listening:
        if shutoff_word in text or (time.time() - last_interaction_time) >= 5:
            messages = reset_conversation()
            first_interaction = True
        else:
            messages.append({'role': 'user', 'content': text})
            response = talk_to_gpt(messages)
            last_interaction_time = time.time()
            print(response)
            speak(response)
            messages = messages[:-1]
    elif first_interaction:
        if wake_word in text:
            listening = True
            messages.append({'role': 'user', 'content': text})
            response = talk_to_gpt(messages)
            last_interaction_time = time.time()
            print(response)
            speak(response)
            first_interaction = False
    else:
        messages.append({'role': 'user', 'content': text})
        response = talk_to_gpt(messages)
        last_interaction_time = time.time()
        print(response)
        speak(response)
