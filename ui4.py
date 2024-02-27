import openai
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from dotenv import load_dotenv
import numpy as np

openai.api_key = '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'
load_dotenv()
model = 'gpt-3.5-turbo'

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "YOUR NAME HERE"
greetings = [
    f"whats up master {name}",
    "yeah?",
    "Well, hello there, Master of Puns and Jokes - how's it going today?",
    f"Ahoy there, Captain {name}! How's the ship sailing?",
    f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?"
]

def get_input_method(method):
    method.destroy()

    def text_input():
        user_input = user_text.get()
        if user_input:
            response = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": user_input}])
            response_text = response.choices[0].message.content
            output.config(state=tk.NORMAL)
            output.insert(tk.END, f"\nYou: {user_input}\nAI: {response_text}\n")
            output.insert(tk.END, f"Done with that prompt if you would like to enter another")
            output.see(tk.END)
            output.config(state=tk.DISABLED)
            speak(response_text)

    def speak(text):
        engine.say(text)
        engine.runAndWait()

    def listen_and_respond():
        with sr.Microphone() as source:
            output.config(state=tk.NORMAL)
            output.insert(tk.END, "\nListening...\n")
            output.see(tk.END)
            output.config(state=tk.DISABLED)
            output.update()

            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                output.config(state=tk.NORMAL)
                output.insert(tk.END, f"\nYou: {text}\n")
                output.see(tk.END)
                output.config(state=tk.DISABLED)
                output.update()

                response = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": text}])
                response_text = response.choices[0].message.content
                output.config(state=tk.NORMAL)
                output.insert(tk.END, f"AI: {response_text}\n")
                output.insert(tk.END, f"Done with that prompt if you would like to enter another")
                output.see(tk.END)
                output.config(state=tk.DISABLED)
                output.update()
                speak(response_text)


            except sr.UnknownValueError:
                pass

    def exit_program():
        root.destroy()

    root = tk.Tk()
    root.title("Chatbot UI")

    user_text = tk.Entry(root, width=80)  # Increased width for larger input space
    user_text.pack(side=tk.LEFT, padx=10)

    enter_button = tk.Button(root, text="Enter", command=text_input)
    enter_button.pack(side=tk.LEFT)

    speech_button = tk.Button(root, text="Speech Input", command=listen_and_respond)
    speech_button.pack()

    exit_button = tk.Button(root, text="EXIT", command=exit_program, bg="red", fg="white")
    exit_button.pack(side=tk.RIGHT, padx=10)

    output = tk.Text(root, wrap=tk.WORD, height=20, width=80, font=("Arial", 12))  # Increased font size
    output.pack()
    output.config(state=tk.DISABLED)

    root.mainloop()

get_input_method(tk.Tk())
