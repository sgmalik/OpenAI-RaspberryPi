import tkinter as tk
import openai
import speech_recognition as sr
import pyttsx3
import threading
from dotenv import load_dotenv

openai.api_key = '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'
load_dotenv()
model = 'gpt-3.5-turbo'

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # You can adjust the speech rate
engine.setProperty('voice', 'english')  # Set the language to English
name = "YOUR NAME HERE"
greetings = [
    f"whats up master {name}",
    "yeah?",
    "Well, hello there, Master of Puns and Jokes - how's it going today?",
    f"Ahoy there, Captain {name}! How's the ship sailing?",
    f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?"
]

class FingerprintSplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Fingerprint Authentication")

        fingerprint_label = tk.Label(self, text="Fingerprint required")
        fingerprint_label.pack(pady=20)

        self.after(5000, self.verify_user)

    def verify_user(self):
        self.title("User Verified")
        fingerprint_label = tk.Label(self, text="User Verified", fg="green")
        fingerprint_label.pack(pady=20)
        self.after(3000, self.destroy)
        self.main_ui.deiconify()

def get_input_method(method):
    method.destroy()

    def text_input():
        user_input = user_text.get("1.0", tk.END).strip()
        if user_input:
            response = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": user_input}])
            response_text =  response.choices[0].message.content
            output.config(state=tk.NORMAL)
            output.insert(tk.END, f"\nYou: {user_input}\n\nAI: {response_text}\n")
            output.insert(tk.END, f"\nDone with that prompt if you would like to enter another\n")
            output.see(tk.END)
            output.config(state=tk.DISABLED)

            # Delay the spoken output
            root.after(650, lambda: speak(f'uh, {response_text}'))

            # Clear the input box
            user_text.delete("1.0", tk.END)

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
                output.insert(tk.END, f"\nAI: {response_text}\n")
                output.insert(tk.END, f"\nDone with that prompt if you would like to enter another\n")
                output.see(tk.END)
                output.config(state=tk.DISABLED)
                output.update()

                root.after(650, lambda: speak(f'uh, {response_text}'))

            except sr.UnknownValueError:
                pass

    def clear_output():
        output.config(state=tk.NORMAL)
        output.delete("1.0", tk.END)
        output.config(state=tk.DISABLED)

    def exit_program():
        root.destroy()

    root = tk.Tk()
    root.title("Chatbot UI")

    authentication_window = FingerprintSplashScreen(root)
    authentication_window.attributes('-topmost', True)
    authentication_window.geometry("300x200")

    authentication_window.withdraw()  # Hide the splash screen initially

    user_text = tk.Text(root, wrap=tk.WORD, height=5, width=40)  # Resized to span multiple lines and reduced width
    user_text.pack(side=tk.LEFT, padx=10, pady=10)

    enter_button = tk.Button(root, text="Enter", command=text_input, bg="blue", fg="white")
    enter_button.pack(side=tk.LEFT, pady=10)

    speech_button = tk.Button(root, text="Speech Input", command=listen_and_respond, bg="blue", fg="white")
    speech_button.pack(pady=10)

    clear_button = tk.Button(root, text="CLEAR", command=clear_output, bg="red", fg="white")
    clear_button.pack(pady=10)

    exit_button = tk.Button(root, text="EXIT", command=exit_program, bg="red", fg="white")
    exit_button.pack(side=tk.RIGHT, padx=10)

    output = tk.Text(root, wrap=tk.WORD, height=20, width=40, font=("Arial", 12))  # Increased font size
    output.pack()
    output.config(state=tk.DISABLED)

    authentication_window.main_ui = root  # Set the main UI reference for the splash screen

    root.mainloop()

get_input_method(tk.Tk())
