import pyttsx3
import webbrowser
import datetime
import pyjokes
import speech_recognition as sr
import os
import time
import requests

# Function to recognize speech and convert to text
def sptext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            print("Recognizing...")
            data = recognizer.recognize_google(audio)
            print(f"You said: {data}")
            return data
        except sr.UnknownValueError:
            speechtx("Sorry, I didn't understand that.")
            return ""
        except Exception as e:
            speechtx("Sorry, there was an error with the microphone.")
            print(e)
            return ""

# Function for text-to-speech
def speechtx(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change index for different voices
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Function to get current weather
def get_weather(api_key):
    location = "India"  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather_desc = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            return f"The current weather in {location} is {weather_desc} with a temperature of {temperature}°C."
        else:
            return "Sorry, I couldn't fetch the weather information."
    except Exception as e:
        print(e)
        return "Error fetching weather data."

if __name__ == '__main__':
    speechtx("Say 'Hey Peter' to start.")
    if sptext().lower() == "hey peter":
        speechtx("How can I help you?")
        while True:
            command = sptext().lower()
            
            if "your name" in command:
                speechtx("My name is Peter.")

            elif "how old are you" in command:
                speechtx("I am a virtual assistant. Age doesn't apply to me!")

            elif 'now time' in command:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speechtx(f"The time is {current_time}")

            elif 'youtube' in command:
                speechtx("Opening YouTube.")
                webbrowser.open("https://www.youtube.com/")
                
            elif "joke" in command:
                joke = pyjokes.get_joke(language="en", category="neutral")
                print(joke)
                speechtx(joke)
                
            elif 'play song' in command:
                music_folder = "E:\\music"  
                try:
                    songs = os.listdir(music_folder)
                    if songs:
                        print(songs)
                        speechtx("Playing a song.")
                        os.startfile(os.path.join(music_folder, songs[0]))
                    else:
                        speechtx("No songs found in the folder.")
                except Exception as e:
                    speechtx("Sorry, there was an error accessing the music folder.")
                    print(e)


            elif "exit" in command:
                speechtx("Thank you, goodbye!")
                break

            time.sleep(1) 
    
    else:
        print("Thanks!")
