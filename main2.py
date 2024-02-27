# This is a script for a text to speech bot that uses openai's chatgpt


# Imports
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import openai
import time
import subprocess
from pocketsphinx import LiveSpeech


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
def speak(command):
    subprocess.call(['espeak', '-ven-us', command])


# Function to get speech input
def get_text():
    speech = LiveSpeech()
    print('I am listening...')
    for phrase in speech:
        text = str(phrase)
        print(text)
        return text


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
        if shutoff_word in text or (time.time() - last_interaction_time) >= 35:
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
