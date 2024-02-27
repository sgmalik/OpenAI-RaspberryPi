import tkinter as tk
import openai
import speech_recognition as sr
import pyttsx3
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

class FullScreenSplashScreen(tk.Toplevel):
    def __init__(self, parent, message, timeout, callback, background_color=None):
        super().__init__(parent)
        self.attributes('-fullscreen', True)
        self.title("Splash Screen")

        label = tk.Label(self, text=message, font=("Arial", 36))
        label.pack(pady=40)

        if background_color:
            self.configure(bg=background_color)

        self.after(timeout, lambda: self.close(callback))

    def close(self, callback):
        self.destroy()
        callback()

class FingerprintSplashScreen(FullScreenSplashScreen):
    def __init__(self, parent, callback):
        super().__init__(parent, "Fingerprint required", 5000, callback)

class FingerprintDeniedSplashScreen(FullScreenSplashScreen):
    def __init__(self, parent, callback):
        super().__init__(parent, "Fingerprint not found", 3000, callback, background_color="red")

class UserVerifiedSplashScreen(FullScreenSplashScreen):
    def __init__(self, parent, callback):
        super().__init__(parent, "User Verified", 3000, callback, background_color="green")

def get_input_method():
    def simulate_fingerprint_verification():
        # Simulate fingerprint verification logic
        fingerprint_verified = True  # Set to False to simulate denial
        if fingerprint_verified:
            show_user_verified_splash()
        else:
            show_fingerprint_denied_splash()

    def show_fingerprint_splash():
        fingerprint_splash = FingerprintSplashScreen(root, simulate_fingerprint_verification)

    def show_fingerprint_denied_splash():
        fingerprint_denied_splash = FingerprintDeniedSplashScreen(root, show_main_ui)

    def show_user_verified_splash():
        user_verified_splash = UserVerifiedSplashScreen(root, show_main_ui)

    def show_main_ui():
        root.deiconify()

    root = tk.Tk()
    root.title("Chatbot UI")
    root.geometry("500x600")
    root.withdraw()  # Hide the main UI initially

    fingerprint_splash = FingerprintSplashScreen(root, show_fingerprint_denied_splash)

    user_text = tk.Text(root, wrap=tk.WORD, height=5, width=40)
    user_text.pack(side=tk.LEFT, padx=10, pady=10)

    enter_button = tk.Button(root, text="Enter", command=lambda: None, bg="blue", fg="white")
    enter_button.pack(side=tk.LEFT, pady=10)

    speech_button = tk.Button(root, text="Speech Input", command=lambda: None, bg="blue", fg="white")
    speech_button.pack(pady=10)

    clear_button = tk.Button(root, text="CLEAR", command=lambda: None, bg="red", fg="white")
    clear_button.pack(pady=10)

    exit_button = tk.Button(root, text="EXIT", command=root.destroy, bg="red", fg="white")
    exit_button.pack(side=tk.RIGHT, padx=10)

    output = tk.Text(root, wrap=tk.WORD, height=20, width=40, font=("Arial", 12))
    output.pack()
    output.config(state=tk.DISABLED)

    root.mainloop()

if __name__ == "__main__":
    get_input_method()
