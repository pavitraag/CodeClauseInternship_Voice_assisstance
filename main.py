import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

API_KEY = "7d57cd5da6a8e544d38f0840e65b0cd6"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
CITY_NAME = "Hyderabad"  # Replace with the desired city name


def take_command():
    command=""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print("You said:", command)
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except Exception as e:
        print("Error:", e)

    return command


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # You can change units to 'imperial' for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        return f"The weather in {city} is {weather_desc}. The temperature is {temp}°C, and the humidity is {humidity}%."
    else:
        return "Sorry, I couldn't fetch weather information at the moment."


def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
        # Pause listening until song ends or user manually stops
        input("Press Enter to stop listening...")
        talk("Listening resumed")

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'tell a joke' in command:
        talk(pyjokes.get_joke())
    elif 'weather' in command:
        weather_info = get_weather(CITY_NAME)
        talk(weather_info)
    elif 'search images' in command:
        search_query = command.replace('search images', '').strip()
        try:
            pywhatkit.search(search_query)
        except Exception as e:
            print("Error while searching images:", e)
            talk("Sorry, there was an error while searching images.")
    elif 'exit' in command:
        talk('Goodbye!See you again')
        exit()
    else:
        talk('Please say the command again.')


while True:
    run_alexa()