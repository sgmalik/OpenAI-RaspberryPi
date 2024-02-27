import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np

# ... (rest of your imports)

# Set up the speech recognition and text-to-speech engines
# ... (rest of your setup)

# Function to display the user interface
def display_user_interface():
    print("Choose input method:")
    print("1. Text Input")
    print("2. Voice Input")

    choice = input("Enter your choice (1 or 2): ")
    return choice

# Function to handle text input
def handle_text_input():
    user_text = input("Enter your message: ")
    return user_text

# Function to handle voice input
def handle_voice_input():
    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Error accessing the Google API: {e}")
            return ""

# Main function to drive the conversation
def main():
    while True:
        choice = display_user_interface()

        if choice == '1':
            user_input = handle_text_input()
        elif choice == '2':
            user_input = handle_voice_input()
        else:
            print("Invalid choice. Please enter 1 or 2.")
            continue

        if "exit" in user_input.lower():
            print("Exiting the chatbot. Goodbye!")
            break

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{user_input}"}])
        response_text = response.choices[0].message.content
        print(f"Bot: {response_text}")

        os.system(f"espeak ' {response_text} '")

# Run the chatbot
if __name__ == "__main__":
    load_dotenv()
    openai.api_key = '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'
    model = 'gpt-3.5-turbo'
    r = sr.Recognizer()

    main()
