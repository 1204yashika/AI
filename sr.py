from __future__ import unicode_literals
import requests
import gtts
import os
import youtubesearchpython
import webbrowser
from playsound import playsound
import speech_recognition as sr
import random
import glob
import re
global i
global y_player
import youtube_dl
import vlc
import threading
import time

ydl_opts = {
    'format': 'bestaudio',
}
ydl = youtube_dl.YoutubeDL(ydl_opts)

i = 1
r = sr.Recognizer()

def listen():
    Text=None
    while Text == None:
        print("Listening...")
        try:
            with sr.Microphone() as source2: 
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2) 
                MyText = r.recognize_google(audio2) 
                Text = MyText.lower()
                print("You said '" + Text +"'...")
        except:
            None
        if Text == None:
            speak("didn't get that. Please ask again")
    return Text

def speak(d,lang="en"):
    global i
    print("Converting to speech...")
    t1 = gtts.gTTS(d,lang=lang)
    print("Listen carefully. \n")
    i +=1
    c = "a"+str(i)+".mp3"
    t1.save(c)
    playsound(c)
    os.remove(c)
    
def youtubemusic(Text):
    global y_player
    try:
        y_player.stop()
    except:
        None
    a = youtubesearchpython.SearchVideos(Text,mode="list",max_results=1).result()
    t = threading.Thread(target=speak,args=["Playing " + a[0][3].lower().replace("video","music")])
    t.daemon = True
    t.start()
    url = ydl.extract_info(a[0][2], download=False)['formats'][0]["url"]
    y_player = vlc.MediaPlayer(url)
    while t.is_alive():
        time.sleep(1)
    y_player.play()
   

def speech(Text):
    global y_player
    words = Text.split()
    # if 'joke' in words :
    #     j = requests.get("https://gofugly.in/api/content/18").json()["result"]
    #     ran = random.randint(0,len(j))
    #     d = j[ran]["joke"].replace('\n','')
    #     print(d)
    #     speak(d,"hi")
    #     laugh = glob.glob("audio/joke/*")
    #     playsound(random.choice(laugh))
    if Text == "roll a dice" or Text == "roll dice":
        roll = random.randint(1,6)
        print(roll)
        d = "Rolling a dice........... It's "+ str(roll)
        speak(d)
    elif Text == "flip a coin" or Text == "flip coin":
        item = ['head' , 'tail']
        d = "Flipping a coin........... It's "+ str(random.choice(item))
        print(d)
        speak(d)
    elif Text in ["play a music", "play some music","play a song" , "play some song"] :
        speak("Which song you ant to play")
        s = listen()
        youtubemusic(s)

    elif Text in ["play music","play", "play the music","play song","play the song"] :
        try:
            y_player.play()
        except:
            speak("Which song you want to play")
            s = listen()
            youtubemusic(s)
    elif re.search('^play', Text)!=None :
        Text = Text.replace("play ","")
        youtubemusic(Text)

    elif Text in["stop music" , "stop" ,"stop the music","stop song","stop the song"]:
        y_player.stop()
    
    elif Text in ["pause music" ,"pause", "pause the music","pause song","pause the song"]:
        y_player.pause()
    else:
        b = "http://api.wolframalpha.com/v1/spoken?appid=9W7R9J-535TX5J43Y"
        # UGTA5X-66UKQ5QRG7"
        get = requests.get(b,params={'i':Text})
        d = get.text
        
        if d == "No spoken result available" or d == "Wolfram Alpha did not understand your input":
            d = "Searching it on google"
            speak(d)
            g = "https://www.google.com/search?q="+ Text
            webbrowser.open(g)
        else:
            speak(d)
# speech("play raabta")
t1 = gtts.gTTS("Your assistant is in your service. Press Enter and ask anything.",lang="en")
i +=1
c = "a"+str(i)+".mp3"
t1.save(c)
playsound(c)
os.remove(c)
while True:
    input()
    a = listen()
    speech(a)