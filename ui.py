import tkinter as tk

import openai


# Set your OpenAI API key

openai.api_key='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'



class OpenAIGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("OpenAI Interface")


        # Create input entry

        self.input_entry = tk.Entry(root, width=50)

        self.input_entry.pack(pady=10)


        # Create button to trigger OpenAI processing

        self.process_button = tk.Button(root, text="Process", command=self.process_input)

        self.process_button.pack()


        # Create text widget for displaying OpenAI output

        self.output_text = tk.Text(root, height=10, width=50)

        self.output_text.pack(pady=10)


    def process_input(self):

        # Get input from the entry widget

        user_input = self.input_entry.get()


        # Process input using OpenAI

        try:

            response = openai.Completion.create(

                engine="text-davinci-002",

                prompt=user_input,

                max_tokens=50

            )

            output_text = response["choices"][0]["text"]

        except Exception as e:

            output_text = f"Error: {str(e)}"


        # Display the output in the text widget

        self.output_text.delete(1.0, tk.END)  # Clear previous content

        self.output_text.insert(tk.END, output_text)


if __name__ == "__main__":

    # Create the main Tkinter window

    root = tk.Tk()


    # Create an instance of the OpenAIGUI class

    openai_gui = OpenAIGUI(root)


    # Start the Tkinter event loop

    root.mainloop()  
