import speech_recognition as sr 
import pyttsx3 
import datetime
import wikipedia 
import webbrowser
import os
import random
import requests
from bs4 import BeautifulSoup
import sys
import cv2
import pywhatkit as kit
import pyautogui
import time
import pyjokes


engine = pyttsx3.init('sapi5') 
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id)           # (0th, 1st) index = (male, female) voice

def speak(audio):
    '''
    It converts the text into speech.
    '''
    engine.say(audio)
    engine.runAndWait()


def greetings():
    '''
    It activates your personal assistant.
    '''
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  
    speak("What do you like me to do?")       

def takeCommand():
    '''
    It takes microphone input from the user and returns string output.
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...") 
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1                         # seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        
    except Exception as e:
        speak("I did not get that. Can you please say that again...")  
        return "None"

    return query


def news():
    '''
    It helps to give the short description of four latest news.
    '''

    api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=bf652e8ec4e44d37b153eeec08507c74'          #to get the news highlights
    main_page = requests.get(api_url).json()
    articles = main_page['articles']

    main_news = []
    for article in articles:
        main_news.append(article['title'])
    
    position = ['first', 'second', 'third', 'last']
    for i in range(len(position)):
        speak(f"Today's {position[i]} news is: {main_news[i]}")

def recognize_speech_from_mic():
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": True if the API request successful

    "error":   `None` if no error occured, otherwise a string containing an error message if the API could not be reached or speech was unrecognizable
   
    "transcription": `None` if speech could not be transcribed,
                      otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjusting the recognizer sensitivity to ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"

    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def day_of_the_year(guess_limit):
    days_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    get_rand_day= random.randint(1, 7)
    choose_a_day = days_list[get_rand_day-1]
    search_day = random.randint(1, 365)

    instructions = f"If first day of the year is {choose_a_day}. What is the {search_day}th day?\nYou have {guess_limit} tries to guess which one.\n"
    result = (search_day % 7) - 1       #getting the day value with. -1 because here, we start with 1st day instead of 0.

    final_day = (get_rand_day - 1 + result) % 7    #for getting the value inside 7
                                                #checked for 198th day to test.

    send = (instructions, days_list[final_day] )
    return send


def game():

    guess_limit = 3
    prompt_limit = 5
    
    current = day_of_the_year(guess_limit)
    instructions = current[0]
    found_day = current[1]
    
    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    speak(instructions)
    speak(guess_limit)
    
    time.sleep(3)

    for i in range(guess_limit):

        for j in range(prompt_limit):
            print('Guess {}. Speak!'.format(i+1))
            guess = recognize_speech_from_mic()
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            tell_this ="I didn't catch that. What did you say?"
            print("tell_this \n")
            speak(tell_this)

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            speak("Error")
            break

        print("You said: {}".format(guess["transcription"]))

        # determine if guess is correct and if any attempts remain
        guess_is_correct = guess["transcription"].lower() == found_day.lower()
        attempts_left = i < guess_limit - 1


        if guess_is_correct:
            print("Correct! You win!".format(found_day))
            speak("Correct! You win!")
            break
        elif attempts_left:
            print("Incorrect. Try again.\n")
            speak("Incorrect. Try again")
        else:
            print("Sorry, you lose!\nThe day is '{}'.".format(found_day))
            
            speak("Sorry, you lose!\nThe day is")
            speak(found_day)
            break


def taskExecution():
    '''
    Execute different tasks.
    '''
    
    greetings()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'what is' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open calculator' in query:
            webbrowser.open("calculator.com")
        
        elif 'open twitter' in query:
            webbrowser.open("twitter.com")
        
        elif 'open facebook' in query:
            webbrowser.open("facebook.com")
        
        elif 'open instagram' in query:
            webbrowser.open("instagram.com")
        
        elif 'open linkedin' in query:
            webbrowser.open("linkedin.com")
        
        elif 'open calendar' in query:
            webbrowser.open("calendar.google.com")
        
        elif 'open map' in query:
            webbrowser.open("maps.google.com")
        
        elif 'open photo' in query:
            webbrowser.open("photos.google.com")

        elif 'open google' in query:
            speak('What do you like to search on google?')
            command = takeCommand().lower()
            webbrowser.open(f"{command}")
        
        elif 'play songs on youtube' in query:
            speak('Tell me the name of the song that you would like to hear.')
            command = takeCommand().lower()
            kit.playonyt(command)
        
        elif 'switch the window' in query:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            time.sleep(0.5)
            pyautogui.keyUp('alt')

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   
        
        elif 'need a ride' in query:
            webbrowser.open(random.choice(['lyft.com', 'uber.com']))
        
        elif 'open command prompt' in query:
            os.system('start cmd')
    
        elif 'tell me a joke' in query:
            speak(pyjokes.get_joke())

        elif 'play music' in query:
            music_dir = 'D:\songs'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, random.choice(songs)))
        
        elif 'open camera' in query:
            speak("Press q whenever you want to close the camera.")
            cam = cv2.VideoCapture(0)
            while True:
                ret, frame = cam.read()
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cam.release()
            cv2.destroyAllWindows()

        elif 'the date' in query:
                sTrDate = datetime.datetime.now().strftime("%B %d, %Y")
                speak(f"Sir, the date is {sTrDate}")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
        
        elif 'shut down the computer' in query:
            os.system('shutdown /s')
        
        elif 'restart the computer' in query:
            os.system('shutdown /r')
        
        elif 'sleep the computer' in query:
            os.system('rundll32.exe powrprof.dll, SetSuspendState Sleep')
        
        elif 'tell me news' in query:
            speak('Sure. Give me a moment to fetch the latest news.')
            news()
        
        elif "what's my location" in query:
            speak("Let me check...")

            try:
                ip_address = requests.get('https://api.ipify.org/').text
                url = "https://get.geojs.io/v1/ip/geo/" + ip_address + ".json"
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                region = geo_data['region']
                country = geo_data['country']
                speak(f"I am not totally sure; however, I think you are in {region} in {country}")
            except Exception as e:
                speak("I was unable to find your location. sorry!")

        elif 'take a screenshot' in query:
            speak("Can you please tell me the name for your screenshot file?")
            name = takeCommand().lower()
            speak("Please hold the screen for 3 seconds. I am taking screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak(f"Screenshot is saved in the main folder with the name {name}")

        elif 'temperature' in  query:
            search = 'the temperature in DC'
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            speak(f"Currently {search} is {temp}")

    
        
        if "play games" in query:
                game()
        
        if 'hello' in query or 'hey' in query:
            speak("Hello sir, how can I help you?")

        elif "what's up" in query:
            speak("Everything's fine sir, what about you!")
        
        elif 'how are you' in query:
            speak("I am fine sir, how about you?")
        
        elif 'fine' in query or 'also good' in query or 'also doing well' in query:
            speak("That's awesome")

        elif 'thank you' in query or 'thanks' in query:
            speak("It's my pleasure.")

    
        elif 'you can sleep' in query or 'sleep now' in query:
            speak('Sure sir. I am going to sleep for now, but you can wake me anytime.')
            break


if __name__ == "__main__":
    while True:
        permission = takeCommand()
        if "wake up" in permission:
            taskExecution()
        elif "goodbye" in permission:
            speak("Thanks for using me. You have a good day sir.")
            sys.exit()