#MODULES REQUIRED 
import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import os
import time
import random
from GoogleNews import GoogleNews
import mysql.connector
import pywhatkit as wt
import contacts
import pyautogui
from googlesearch import search
import smtplib

#DATABASE CONNECTION
con = mysql.connector.connect(host = 'localhost', port = '3306', user ='root', passwd = 'ayan.com', database = 'jarvis')
cur=con.cursor()

#VOICE FUNCTION
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1 ].id)

#SPEAK FUNCTION
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#WISHME FUNCTION
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <12:
        speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("good afternoon")
    else:
        speak("good evening")
    speak("hello sir! telll what to do")

#TAKE COMMAND FUNCTION
def takecommond():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        
        audio = r.listen(source)
        r.pause_threshold  = 1
     
    try:
        print("recoginizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
    except Exception as e:
        print(e)    
        print("say again...")
    return query

#GOOGLENEWS FUNCTION
def GoogleNews():
    googlenews =  GoogleNews()
    googlenews =  GoogleNews(period = '7d')
    googlenews.search('INDIA')
    result = googlenews.result()
    for x in result:
        print("-"*50)
        print("Title--", x['tittle'])
        print("Date/Time--", x['date'])
        print("Description--", x['desc'])
        print("Link--",  x['link'])

#WHATSAPP MESSAGE
def whatsapp():
    rec_name = input(speak('whom do you want to send message?'))
    speak(f'what message do you want me to send to')
    msg = input(f"what message do you want me to send to {rec_name}")
    speak("tell me the hour.")
    hour = int(input('enter the hour'))
    speak('tell me the min.')
    minute = int(input('enter the minute.')) 
    wt.sendwhatmsg(a, msg, hour,minute)

def sentemail():
    sender_mail = 'sahilbaki55@gmail.com'
    reciver = input(speak('please enter the recievers email address :-'))    
    receivers_mail = [f'{reciver}']    
    message = input(speak('what dou you want to send message:- '))   
    try:    
        password = input(speak('Enter the password'));    
        smtpObj = smtplib.SMTP('gmail.com',587)    
        smtpobj.login(sender_mail,password)    
        smtpObj.sendmail(sender_mail, receivers_mail, message)    
        print("Successfully sent email")    
        speak('successfully sent email')
    except Exception as e :    
        print("Error: unable to send email")
        print(e)
        speak(f'unable to send email due to {e}')   

#MAIN FUNCTION
if __name__=="__main__":
    wishme()
    while True:
        query=takecommond().lower()
        if 'wikipedia' in query:
            speak('searching wikipedia...')
            results = wikipedia.summary(query, sentences=2)
            speak('according to wikipedia')
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com/farhaad3730/")

        elif 'play music' in query:
            songnumber=random.randint(1,15)
            music_dir= 'D:\\music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir,songs[songnumber]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'open visual studio code' in query:
            codepath = ("C:\\Users\\The Coder\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
            os.starfile(codepath)

        elif 'open browser ' in query:
            path = ('C:\\Program Files\\BraveSoftware\\Brave-Browser\\brave.exe')
            speak('opening browser')
            os.startfile(path)

        elif 'what day is today' in query:
            today=time.localtime().tm_wday
            speak(today)
 
        elif 'send whatsapp message' in query:
            whatsapp()

        elif 'stop jarvis' in query:
            speak('ok sir. See you soon.')
            break
        elif 'shutdown' in query:
            xy = input(speak('please confirm you wnat to shutdown the system'))
            if xy == 'no':
                exit()
            else:
                speak("shutingdown...meet you soon")
                os.system('shutdown /r /t 1')
        
        elif 'whatsapp message' in query:
            whatsapp()      

        elif 'search' in query:
            speak('searching..')
            for j in search(query, tld="co.in" , num = 10, stop=10, pause=2):
                print(j)
            speak("search complete")
        
        elif 'send an email' in query:
            speak('sending mail')
            sentemail()

        elif 'take notes' in query:
            with open('notes.txt' , 'a') as f:
                speak('taking notes...')
                print("taking notes..")
                a = sr.Recognizer()
                with sr.Microphone() as source:
                    input = a.listen(source)

                    content = a.recognize_google(input, language='en-in')
                f.write(content)
                f.close()

        elif 'show notes' in query:
            with open('notes.txt' , 'r') as f:
                data = f.read
                print(data)
                speak(data)

        