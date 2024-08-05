import streamlit as st
import random
import json
import pickle
import time
import os
import numpy as np
import speech_recognition as sr
from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
import nltk


lemmatizer = WordNetLemmatizer()
intents = json.load(open("intents.json"))
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            treatment = intent.get('treatment', None)
            treatment_message = ""
            if treatment:
                treatment_message = "\n".join([f"- {t}" for t in treatment[1:]])
            return f"{response}\n\nPotential treatments or management strategies:\n{treatment_message}"

def calling_the_bot(txt):
    predict = predict_class(txt)
    response = get_response(predict, intents)
    return f" {response}"

def get_audio_input():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None

def initialize_bot():
    os.system(f"say -v {st.session_state.voice} 'Hello user, I am Waley, Your personal Talking Healthcare Chatbot.'")
    os.system(f"say -v {st.session_state.voice} 'If you want to continue with male voice please say male. Otherwise say female.'")
    audio_text = get_audio_input()
    if audio_text == "female":
        st.session_state.voice = 'Karen'
        os.system(f"say -v {st.session_state.voice} 'You have chosen to continue with Female Voice'")
    else:
        st.session_state.voice = 'Daniel'
        os.system(f"say -v {st.session_state.voice} 'You have chosen to continue with Male Voice'")

st.title("Healthcare Chatbot")

recognizer = sr.Recognizer()
mic = sr.Microphone()

if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.voice = 'Karen'
    st.session_state.greeted = False

if not st.session_state.started:
    st.session_state.started = True
    initialize_bot()

if not st.session_state.greeted:
    st.subheader("I am Waley, Your personal Talking Healthcare Chatbot.")
    st.write("You may tell me your symptoms now. I am listening...")
    st.session_state.greeted = True

continue_listening = True
while continue_listening:
    st.write("Say your symptoms. The bot is listening...")
    os.system(f"say -v {st.session_state.voice} 'You may tell me your symptoms now. I am listening.'")
    text = get_audio_input()
    if text:
        st.markdown(f"<span style='color: green; font-weight: bold;'>You said:</span> {text}", unsafe_allow_html=True)
        os.system(f"say -v {st.session_state.voice} 'You:{text}'")
        st.write("Scanning our database for your symptom. Please wait...")
        os.system(f"say -v {st.session_state.voice} 'Scanning our database for your symptom. Please wait.'")
        time.sleep(1)
        response = calling_the_bot(text)
        st.markdown(f"<span style='color: orange; font-weight: bold;'>Bot:</span> {response}", unsafe_allow_html=True)
        os.system(f"say -v {st.session_state.voice} 'Found it. We found that {response}'")
    else:
        st.write("Sorry, either your symptom is unclear to me or it is not present in our database. Please try again.")
        os.system(f"say -v {st.session_state.voice} 'Sorry, either your symptom is unclear to me or it is not present in our database. Please try again.'")

    os.system(f"say -v {st.session_state.voice} 'If you want to continue please say continue otherwise say please exit.'")
    st.write("If you want to continue please say '*Continue*' otherwise say '*Please Exit*'.")
    final_text = get_audio_input()

    if final_text and final_text.lower() in ['please exit', 'exit']:
        os.system(f"say -v {st.session_state.voice} 'Thank you. Shutting down now.'")
        st.write("Bot has been stopped by the user.")
        continue_listening = False
    else:
        os.system(f"say -v {st.session_state.voice} 'Continuing to listen for more symptoms.'")
        st.write("Continuing to listen for more symptoms.")