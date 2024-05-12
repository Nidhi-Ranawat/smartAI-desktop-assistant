import threading
import requests
import smtplib
import cv2
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import subprocess
from ecapture import ecapture as ec
import requests
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from plyer import notification
from keras.models import load_model
import json
import random
import pygame
from pygame import mixer
import re
import os

# Load tasks from JSON file
def load_tasks_from_json():
    tasks = []
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    return tasks

# Save tasks to JSON file
def save_tasks_to_json(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)
todo_list = load_tasks_from_json()

lemmatizer = WordNetLemmatizer()
# Initializing the mixer module
mixer.init()

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

# mail credentials
EMAIL_ADDRESS = "coffeecandyedits@gmail.com"
EMAIL_PASSWORD = "xoykjsawbokkqavu"

# TODOlist
todo_list = []

# Playlist
playlist = {
    'pop': ['Billie_Eilish_Copycat.mp3'],
    'rock': ['Jonas-Brothers-Sucker.mp3'],
}

# FOR ACCEPTING REQUESTS/ PROVIDING RESPONSES
def load_intent_model():
    # Load the intent classification model
    model = load_model('chatbot_model.h5')
    return model

def preprocess_input(user_input):
    # Tokenize and lemmatize user input
    input_words = nltk.word_tokenize(user_input)
    input_words = [lemmatizer.lemmatize(word.lower()) for word in input_words]

    # Create bag-of-words representation
    input_bag = [1 if w in input_words else 0 for w in words]

    return np.array(input_bag)

def classify_intent(user_input, model):
    preprocessed_input = preprocess_input(user_input)
    intent_probabilities = model.predict(np.array([preprocessed_input]))

    # Get the predicted intent
    predicted_intent_index = np.argmax(intent_probabilities)
    predicted_intent = classes[predicted_intent_index]

    return predicted_intent

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")
        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement
  
# Function to get user input either as speech or text
def get_user_input():
    while True:
        speak("Would you like to provide input as speech or text?")
        response = takeCommand().lower()

        if 'speech' in response:
            return get_speech_input()
        elif 'text' in response:
            return get_text_input()
        else:
            speak("I'm sorry, I didn't understand. Please choose either 'speech' or 'text'.")

# Function to get text input from the user
def get_text_input():
    return input()

# Function to get speech input from the user
def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please speak...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        spoken_text = recognizer.recognize_google(audio)
        return spoken_text
    except sr.UnknownValueError:
        speak("I couldn't understand what you said. Please try again.")
        return get_speech_input()
    except sr.RequestError as e:
        speak(f"Sorry, there was an error with the speech recognition service: {e}")
        return None
    
def get_random_response(intents, intent_tag):
    intent = next((item for item in intents['intents'] if item['tag'] == intent_tag), None)
    if intent:
        return random.choice(intent['responses'])
    else:
        return "I'm sorry, I don't have information on that."

def send_email(to_email, subject, body):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(EMAIL_ADDRESS, to_email, message)

        print(f"Email sent to {to_email} successfully!")
        speak(f"Email sent to {to_email} successfully!")
        main()


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        speak("Sorry, I encountered an error while sending the email.")

def open_application(app_name):
    app_urls = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "gmail": "https://mail.google.com",
        "stackoverflow": "https://stackoverflow.com"
        # Add more applications as needed
    }

    if app_name in app_urls:
        url = app_urls[app_name]
        webbrowser.open_new_tab(url)
        speak(f"Opening {app_name}...")
        time.sleep(5)  # Wait for a few seconds to allow the application to open
        speak(f"{app_name} is now open. How can I assist you further?")
    else:
        speak(f"Sorry, I don't have information on how to open {app_name}.")

def extract_application_name(statement):
    for app in ["youtube", "google", "gmail", "stackoverflow"]:
        if app in statement:
            return app
    return None  # If no matching application is found

def get_news_headlines(news_source):
    news_sources = {
        'times_of_india': 'https://timesofindia.indiatimes.com/home/headlines',
        'bbc': 'https://www.bbc.com/news',
        # Add more news sources as needed
    }

    if news_source.lower() in news_sources:
        news_url = news_sources[news_source.lower()]
        webbrowser.open_new_tab(news_url)
        speak(f"Here are some headlines from {news_source.capitalize()}. Happy reading!")
        time.sleep(6)  # Wait for a few seconds to allow the user to read the headlines
    else:
        speak("I'm sorry, I don't have headlines for that news source.")

def extract_news_source(statement):
    # Define keywords for each news source
    times_of_india_keywords = ["times of india", "toi", "india times"]
    bbc_keywords = ["bbc", "bbc news"]

    # Check for keywords in the statement
    statement_lower = statement.lower()

    if any(keyword in statement_lower for keyword in times_of_india_keywords):
        return 'times_of_india'
    elif any(keyword in statement_lower for keyword in bbc_keywords):
        return 'bbc'

    # Default to an empty string if no matching source is found
    return ''

def capture_photo():
    # Open the camera (0 is the default camera, you can change it if needed)
    cap = cv2.VideoCapture(0)

    # Capture a single frame
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    # Save the captured frame as an image
    img_path = "captured_photo.jpg"
    cv2.imwrite(img_path, frame)

    return img_path

def perform_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(search_url)

def get_current_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    return f"The current time is {current_time}."

def perform_eda(csv_path):
    try:
        if csv_path.endswith('.csv'):
            df = pd.read_csv(csv_path)

            # Display basic information about the DataFrame
            print("\n\nOVERVIEW OF THE DATASET \n")
            print(df.sample())  # Display the first few rows

            print("\n\nNumber of rows and columns : ")
            print(df.shape)
            
            print("\n\nSummary statistics: \n")
            print(df.describe())     

            if df.duplicated().any():
                print(df.duplicated().sum(), "duplicate rows present")

            total_rows = df.shape[0]
            null_percentage_per_column = (df.isnull().sum() / total_rows) * 100
            columns_with_null = null_percentage_per_column[null_percentage_per_column > 0]

            print("\n\n\% \of null values in Columns")
            print(columns_with_null)

            # Additional EDA steps can be added as needed

        else:
            speak("Invalid file format. Please provide a CSV file.")

    except Exception as e:
        print(f"An error occurred during EDA: {str(e)}")
        speak("An error occurred during exploratory data analysis.")


# TODOLIST
def add_task_to_do_list(task):
    todo_list.append(task)
    save_tasks_to_json(todo_list)
    print(f"Added '{task}' to your to-do list.")
    speak(f"Sure, added '{task}' to your to-do list.")

def show_to_do_list():
    tasks = load_tasks_from_json()
    if tasks:
        tasks_str = ', '.join(tasks)
        print("Here's your to-do list:", tasks_str)
        speak("Here's your to-do list: " + tasks_str)
    else:
        print("Your to-do list is empty.")
        speak("Your to-do list is empty.")

def complete_task(task):
    if task in todo_list:
        todo_list.remove(task)
        save_tasks_to_json(todo_list)
        print(f"Great! You've marked '{task}' as completed.")
        speak(f"Great! You've marked '{task}' as completed.")
    else:
        print(f"The task '{task}' is not in your to-do list.")
        speak(f"The task '{task}' is not in your to-do list.")

def remove_task(task):
    if task in todo_list:
        todo_list.remove(task)
        save_tasks_to_json(todo_list)
        print(f"'{task}' has been removed from your to-do list.")
        speak(f"'{task}' has been removed from your to-do list.")
    else:
        print(f"The task '{task}' is not in your to-do list.")
        speak(f"The task '{task}' is not in your to-do list.")

# MUSIC 
def play_music_threaded(genre):
    if not genre:
        # If no genre is specified, choose a random genre from the playlist
        genre = random.choice(list(playlist.keys()))
    # This is a simple example using pygame to play music
    if genre in playlist:
        song_list = playlist[genre]
        if song_list:
            song_to_play = random.choice(song_list)
            mixer.music.load(song_to_play)
            mixer.music.play()
        else:
            speak("Sorry, I don't have any songs in that genre.")
    else:
        speak("I don't have song of this genre")

def handle_music_intent(user_input):
    music_intents = [intent for intent in intents['intents'] if intent['tag'] == 'music']

    for music_intent in music_intents:
        patterns = music_intent['patterns']
        responses = music_intent['responses']

        for pattern, response in zip(patterns, responses):
            regex_pattern = re.sub(r'{(\w+)}', r'(?P<\1>.+?)', pattern)
            match = re.match(regex_pattern, user_input, re.IGNORECASE)

            if match:
                entities = match.groupdict()
                play_music_threaded(entities.get('genre'))
                speak(response.format(**entities))
                return

# FOR NOTIFICATIONS
def speech_reminder():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        spoken_text = recognizer.recognize_google(audio)
        return spoken_text

def extract_time_from_spoken_text(spoken_text):
    # Use regular expression to find time in the spoken text
    time_match = re.search(r'\b(?:[01]?\d|2[0-3]):?[0-5]?\d(?:\s?[apAP]\.?[mM]\.?)?\b', spoken_text)

    if time_match:
        # If a match is found, clean and format the time
        cleaned_time = re.sub(r'[^0-9:apmAPM]', '', time_match.group())
        return cleaned_time
    else:
        return None

def set_reminder():
    speak("Sure, I can help you set a reminder. What task would you like to be reminded of?")
    task = takeCommand()

    while not task:
        speak("Please provide a valid task.")
        task = takeCommand()

    speak("Great! Now, when would you like to be reminded? Please provide the time in HH:MM format.")

    while True:
        time_input = takeCommand()
        extracted_time = extract_time_from_spoken_text(time_input)

        if extracted_time:
            try:
                datetime_obj = datetime.datetime.strptime(extracted_time, "%I:%M%p")
                extracted_time_24h = datetime_obj.strftime("%H:%M")

                speak(f"Okay, I will remind you to '{task}' at {extracted_time}.")

                current_time = datetime.datetime.now().strftime("%H:%M")
                time_difference = (datetime.datetime.strptime(extracted_time_24h, "%H:%M") - datetime.datetime.strptime(current_time, "%H:%M")).total_seconds()

                reminder_thread = threading.Thread(target=sleep_and_notify, args=(time_difference, task))
                reminder_thread.start()

                break
            except ValueError:
                speak("Invalid time format. Please provide the time in HH:MM am/pm format. Let's try again.")
        else:
            speak("Invalid time format. Please provide the time in HH:MM am/pm format. Let's try again.")

def sleep_and_notify(seconds_until_reminder, task):
    # Sleep until the reminder time
    time.sleep(seconds_until_reminder)

    # Trigger the notification after sleeping
    schedule_notification(task)

def schedule_notification(task):
    notification_title = "Reminder"
    notification_message = f"Don't forget to: {task}"

    # Use a notification library like plyer to show a notification
    notification.notify(
        title=notification_title,
        message=notification_message,
        timeout=None,
    )

def main():
    model = load_intent_model()

    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()

        if statement == 0:
            continue

        predicted_intent = classify_intent(statement, model)

        # Implement logic based on the predicted intent
        if predicted_intent == 'greetings':
            response = get_random_response(intents, 'greetings')
            speak(response)

        elif "stop music" in statement.lower() or "pause music" in statement.lower():
            mixer.music.stop()

        elif predicted_intent == 'open_app':
            # Extract the specific application name from the statement
            app_name = extract_application_name(statement)
            open_application(app_name)
            # speak(f"{app_name} is open now. How can I assist you further?")

        elif predicted_intent == 'wikipedia':
            # Search Wikipedia
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif predicted_intent == 'news':
            # 'source' is the extracted news source from the user's statement
            # Example: "news from times of india"
            source = extract_news_source(statement)  # a function to extract the news source
            get_news_headlines(source)

        elif predicted_intent == 'camera':
            speak("Sure, capturing a photo for you...")
            time.sleep(6) 
            captured_photo_path = capture_photo()
            speak("Photo captured and saved as img.jpg.")
            print("Photo captured and saved as:", captured_photo_path)

        elif predicted_intent == 'search':
            speak("What exactly would you like to search for?")
            search_query = takeCommand()
            perform_search(search_query)
            
            speak(f"Searching the web for {search_query}...")
            print(f"Searching the web for {search_query}.")

        # elif predicted_intent == 'send_email':
        #     # Ask the user for recipient's name and email address
        #     speak("To whom would you like to send the email, Please provide the person's name.")
        #     person = takeCommand()

        #     speak(f"Great! What is the email address of {person}?")
        #     email = get_user_input()

        #     # Ask the user for email details
        #     speak(f"Sure, I can help you send an email to {person}. What is the subject of the email?")
        #     subject = get_user_input()

        #     speak("Great! Now, what would you like to say in the email?")
        #     body = get_user_input()

        #     # Send the email
        #     send_email(email, subject, body)
        elif predicted_intent == 'send_email':
            # Ask the user for recipient's name and email address
            speak("To whom would you like to send the email, Please provide the person's name.")
            person = takeCommand()

            speak(f"Great! What is the email address of {person}?")
            email = get_user_input()

            # Ask the user for email details
            speak(f"Sure, I can help you send an email to {person}. What is the subject of the email?")
            subject = get_user_input()

            speak("Great! Now, what would you like to say in the email?")

            # Initialize an empty string to store the email body
            body = ""

            while True:
                body_part = takeCommand()
                body += body_part

                speak("Do you want to add more to the email body or are you finished? If so say break")
                response = takeCommand().lower()

                if 'break' in response:
                    break  # Exit the loop if the user indicates they are finished

                speak("Sure, go ahead and continue.")

            # Send the email
            send_email(email, subject, body)

        elif "weather" in statement:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("what is your city name")
            city_name=takeCommand()
            print(city_name)
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f"Temperature in kelvin unit in {city_name} is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))
            else:
                speak(" City Not Found ")

        elif predicted_intent == 'who_are_you':
            response = get_random_response(intents, 'who_are_you')
            speak(response)

        elif predicted_intent == 'creator':
            speak("I was built by Aditi, Nidhi, Nishi, and Ritika.")

        elif predicted_intent == 'time':
            speak("Sure, let me check the time for you.")
            time_result = get_current_time()
            speak(time_result)

        elif predicted_intent == 'log_off':
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif predicted_intent == 'perform_eda':
            speak("Sure, please provide the path to the CSV file for analysis.")
            csv_path = "movies_metadata.csv"
            perform_eda(csv_path)

        elif predicted_intent == 'reminder':
            set_reminder()

        elif predicted_intent == 'to_do_list':
            speak("Sure, what task would you like to add to your to-do list?")
            task = takeCommand()
            add_task_to_do_list(task)

        elif predicted_intent == 'show_to_do_list':
            show_to_do_list()

        elif predicted_intent == 'complete_task':
            speak("Which task would you like to mark as complete?")
            task = takeCommand()
            complete_task(task)

        elif predicted_intent == 'remove_task':
            speak("Which task would you like to remove from your to-do list?")
            task = takeCommand()
            remove_task(task)

        elif predicted_intent.lower() == "music":
            handle_music_intent(statement)

        if predicted_intent == 'goodbye':
            speak('Your personal assistant is shutting down. Goodbye!')
            print('Your personal assistant is shutting down. Goodbye!')
            break

        else:
            # Handle unknown intent
            speak("")
            # speak("I didn't understand that.")

if __name__ == "__main__":
    main()
