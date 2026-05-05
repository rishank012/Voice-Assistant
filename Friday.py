import threading
import tkinter as t
from PIL import Image, ImageTk, ImageSequence
import speech_recognition as sr
from time import sleep
from playsound import playsound
import pygame as p
import random
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit
import pyjokes
import pyautogui as py
import queue

# Define delay globally
delay = 100  # Adjust the delay (in milliseconds) as needed

# Variables
w = "friday"
g = ["audios\\greetings\\hello.mp3", "audios\\greetings\\hey.mp3", "audios\\greetings\\hi.mp3", "audios\\greetings\\yes.mp3", "audios\\greetings\\heyy.mp3", "audios\\greetings\\helloo.mp3"]
h = ["audios\\hello\\helo.mp3", "audios\\hello\\helloo.mp3", "audios\\hello\\hello.mp3", "audios\\hello\\nice.mp3"]
hi = ["audios\\hi\\hi.mp3", "audios\\hi\\hii.mp3"]
i = ["audios\\invented\\invented.mp3", "audios\\invented\\made.mp3"]
o = ["audios\\how\\i am great.mp3", "audios\\how\\i am good.mp3"]
b = ["audios\\bye\\bye.mp3", "audios\\bye\\goodbye.mp3", "audios\\bye\\byee.mp3"]

# Function to animate the GIF
def animate():
    global frame_index, frames, label, delay
    frame_index = (frame_index + 1) % len(frames)
    label.config(image=frames[frame_index])
    r.after(delay, animate)

# Function to load a new GIF
def load_gif(file_path):
    global frames, frame_index
    image = Image.open(file_path)
    frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(image)]
    frame_index = 0
    animate()

def play(m):
    p.mixer.init()
    p.mixer.music.load(m)
    p.mixer.music.play()

def writer():
    play("audios\\file\\what is file name.mp3")
    sleep(6)
    a = listen()
    play("audios\\file\\how many lines.mp3")
    sleep(5)
    play("audios\\file\\line range.mp3")
    sleep(6)
    b = listen()
    c = int(b[-1])
    lines = [listen() for _ in range(c)]
    with open(f"{a}.txt", "w") as f:
        for line in lines:
            f.write(line + "\n")
    play("audios\\file\\file created.mp3")


# Listen function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration = 0.5)
        status_queue.put("Listening...")
        recognizer.pause_threshold = 0.5
        audio = recognizer.listen(source)
        status_queue.put("Recognizing...")
        try:
            text = recognizer.recognize_google(audio)
            status_queue.put(f"You said: {text}")
        except sr.UnknownValueError:
            status_queue.put("Sorry, I did not catch that.") 
            text = ""
        except sr.RequestError as e:
            status_queue.put(f"Could not request results; {e}")
            text = ""
    return text

# Function to process the queue in the main thread
def process_queue():
    while not command_queue.empty():
        command = command_queue.get()
        play(command)
    
    while not status_queue.empty():
        status_label.config(text=status_queue.get())

    r.after(100, process_queue)  # Continuously check for updates

def date():
    speak(f"Today the date is : {datetime.datetime.now().strftime('%d %B %Y')}")
def time():
    speak(f"The time is : {datetime.datetime.now().strftime('%I:%M %p')}")
def day():
    speak(f"Today the day is : {datetime.datetime.now().strftime('%A')}")
def month():
    speak(f"The month is : {datetime.datetime.now().strftime('%B')}")
def year():
    speak(f"The year is : {datetime.datetime.now().strftime('%Y')}")
def search(q):
    pywhatkit.search(q)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        play("wish\\good morning.mp3")
    elif hour >= 12 and hour < 18:
        play("wish\\good afternoon.mp3")
    else:
        play("wish\\good evening.mp3")
        sleep(3)

def speak(text: str, voice: str = 'en-US-JennyNeural', subtitle_file: str = 'Subtitles_File.srt') -> None:
    command = f"edge-tts --voice \"{voice}\" --text \"{text}\" --write-media \"{voice}.mp3\" --write-subtitles {subtitle_file}"
    os.system(command)
    playsound(f"{voice}.mp3")
    os.remove(subtitle_file)
    os.remove(f"{voice}.mp3")


# Function to close the application
def close_app():
    r.quit()
    r.destroy()

# Set up the main window
r = t.Tk()
r.title("Assistant")
r.config(bg="Black")
r.attributes("-fullscreen", True)
r.resizable(False, False)

# Create the label to display the GIF
label = t.Label(r, borderwidth=0)
label.pack(pady=10)  # Adjusted padding to space out the elements

# Create GUI elements with padding to adjust the position
status_label = t.Label(r, text="Speak the magic word to start...", fg="White", bg="Black", font=("Helvetica", 24, "bold"))
status_label.pack(pady=(20, 0))  # Reduced padding to ensure visibility

# Create a menu
menu_bar = t.Menu(r)
r.config(menu=menu_bar)

# Add a 'File' menu
file_menu = t.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add options for predefined GIFs
file_menu.add_command(label="Theme 1", command=lambda: load_gif("Themes\\1.gif"))
file_menu.add_command(label="Theme 2", command=lambda: load_gif("Themes\\2.gif"))
file_menu.add_command(label="Theme 3", command=lambda: load_gif("Themes\\3.gif"))
file_menu.add_command(label="Theme 4", command=lambda: load_gif("Themes\\4.gif"))
file_menu.add_command(label="Theme 5", command=lambda: load_gif("Themes\\5.gif"))
file_menu.add_command(label="Theme 6", command=lambda: load_gif("Themes\\6.gif"))
file_menu.add_command(label="Theme 7", command=lambda: load_gif("Themes\\7.gif"))
file_menu.add_command(label="Theme 8", command=lambda: load_gif("Themes\\8.gif"))


# Add 'Exit' option to the 'File' menu
file_menu.add_separator()
file_menu.add_command(label="Exit", command=close_app)

# Open the initial GIF image
initial_image = "Themes\\1.gif"
load_gif(initial_image)

# Start the animation
frame_index = 0

# Initialize command queue for background processing
command_queue = queue.Queue()
status_queue = queue.Queue()

# Start listening in a thread
def start_listening():
    while True:
        user = listen()

        if user and w in user.lower():
            command_queue.put(random.choice(g))
            sleep(4)
            while True:
                user = listen().lower()

                if "date" in user:
                    date()
                    break

                elif "time" in user:
                    time()
                    break

                elif "day" in user:
                    day()
                    break

                elif "month" in user:
                    month()
                    break

                elif "year" in user:
                    year()
                    break

                elif "hata" in user:
                    py.hotkey("alt", "f4")
                    break

                elif "de" in user:
                    day()
                    break

                elif "exit" in user:
                    py.hotkey("alt", "f4")
                    break

                elif "close" in user:
                    py.hotkey("alt", "f4")
                    break

                elif "good" in user:
                    wishMe()
                    break

                elif "here" in user:
                    play("audios\\wish\\call me.mp3")
                    break

                elif "hello" in user:
                    play(random.choice(h))
                    break

                elif "how are you" in user:
                    play(random.choice(o))
                    break

                elif "how r u" in user:
                    play(random.choice(o))
                    break

                elif "write" in user:
                    writer()
                    break

                elif "type" in user:
                    writer()
                    break

                elif "file" in user:
                    writer()
                    break

                elif 'search' in user:
                    u = user.replace("search", "").strip()
                    play("audios\\open\\search.mp3")
                    search(u)
                    break

                elif 'open youtube' in user:
                    webbrowser.open("youtube.com")
                    break

                elif 'open google' in user:
                    webbrowser.open("google.com")
                    break

                elif 'my name is' in user:
                    name = user.replace('my name is', '').strip()
                    speak('hello ' + name)
                    play("audios\\name\\beautiful name.mp3")
                    break

                elif 'play my music' in user:
                    music_dir = 'C:\\Users\\risha\\Music\\My Music'
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir, songs[0]))
                    break

                elif 'play my song' in user:
                    music_dir = 'C:\\Users\\risha\\Music\\My Music'
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir, songs[16]))
                    break

                elif 'open vs code' in user:
                    codePath = "C:\\Users\\risha\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                    os.startfile(codePath)
                    break

                elif 'play' in user:
                    song = user.replace('play', '').strip()
                    play("audios\\open\\playing.mp3")
                    pywhatkit.playonyt(song)
                    break

                elif 'joke' in user:
                    speak(pyjokes.get_joke())
                    break

                elif "banaya" in user:
                    play(random.choice(i))
                    break

                elif "invented" in user:
                    play(random.choice(i))
                    break

                elif 'hi' in user:
                    play(random.choice(hi))
                    break

                elif 'open notepad' in user:
                    notepad = "C:\\Users\\risha\\OneDrive\\Desktop\\Notepad.lnk"
                    os.startfile(notepad)
                    break

                elif 'open discord' in user:
                    discord = "C:\\Users\\risha\\OneDrive\\Desktop\\Discord.lnk"
                    os.startfile(discord)
                    break

                elif 'open file manager' in user:
                    manager = "C:\\Users\\risha\\OneDrive\\Desktop\\This PC.lnk"
                    os.startfile(manager)
                    break

                elif 'open facebook' in user:
                    webbrowser.open("facebook.com")
                    break

                elif 'will you marry me' in user:
                    play("audios\\marry\\hmm.mp3")
                    break

                elif 'your name' in user:
                    play("audios\\name\\name.mp3")
                    break

                elif 'who is your best friend' in user:
                    play("audios\\friend\\best friend.mp3")
                    break

                elif 'do you like me' in user:
                    play("audios\\friend\\yeah.mp3")
                    break

                elif 'whatsapp' in user:
                    play("open\\whatsapp.mp3")
                    whatsapp = "C:\\Users\\risha\\OneDrive\\Desktop\\WhatsApp - Shortcut.lnk"
                    os.startfile(whatsapp)
                    break

                elif "bye" in user:
                    play(random.choice(b))
                    break

                else:
                    play("audios\\don't know\\not understand.mp3")
                    sleep(5)

# Start the listening thread
threading.Thread(target=start_listening, daemon=True).start()

# Process queued updates in the main thread
process_queue()

r.mainloop()
