import tkinter as tk
import threading
import time
from tkinter import simpledialog
import openai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

openai.api_key = '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'
load_dotenv()
model = 'gpt-3.5-turbo'

class SplashScreen(tk.Toplevel):
    def __init__(self, parent, main_ui):
        super().__init__(parent)
        self.main_ui = main_ui
        self.title("Fingerprint Authentication")

        fingerprint_label = tk.Label(self, text="Place your finger on the sensor")
        fingerprint_label.pack(pady=20)

        self.after(3000, self.verify_user)

    def verify_user(self):
        self.title("User Verified")
        fingerprint_label = tk.Label(self, text="User Verified", fg="green")
        fingerprint_label.pack(pady=20)
        self.after(3000, self.destroy)
        self.main_ui.deiconify()

def get_input_method(method):
    method.withdraw()  # Hide the main UI initially

    root = tk.Tk()
    root.title("Chatbot UI")

    authentication_window = SplashScreen(root, method)
    authentication_window.attributes('-topmost', True)
    authentication_window.geometry("300x200")

    def text_input():
        user_input = user_text.get("1.0", tk.END).strip()
        if user_input:
            response = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": user_input}])
            response_text = response.choices[0].message.content
            output.config(state=tk.NORMAL)
            output.insert(tk.END, f"\nYou: {user_input}\n\nAI: {response_text}\n")
            output.insert(tk.END, f"\nDone with that prompt if you would like to enter another\n")
            output.see(tk.END)
            output.config(state=tk.DISABLED)

            root.after(650, lambda: speak(f'uh, {response_text}'))
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

    user_text = tk.Text(root, wrap=tk.WORD, height=5, width=40)
    user_text.pack(side=tk.LEFT, padx=10, pady=10)

    enter_button = tk.Button(root, text="Enter", command=text_input, bg="blue", fg="white")
    enter_button.pack(side=tk.LEFT, pady=10)

    speech_button = tk.Button(root, text="Speech Input", command=listen_and_respond, bg="blue", fg="white")
    speech_button.pack(pady=10)

    clear_button = tk.Button(root, text="CLEAR", command=clear_output, bg="red", fg="white")
    clear_button.pack(pady=10)

    exit_button = tk.Button(root, text="EXIT", command=exit_program, bg="red", fg="white")
    exit_button.pack(side=tk.RIGHT, padx=10)

    output = tk.Text(root, wrap=tk.WORD, height=20, width=40, font=("Arial", 12))
    output.pack()
    output.config(state=tk.DISABLED)

    root.mainloop()

if __name__ == "__main__":
    get_input_method(tk.Tk())
