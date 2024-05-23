import json
import openai
from openai import OpenAI

# Initialize the OpenAI client with the base URL and API key
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# File to store the conversation history
history_file = "C:\\Users\\91988\\Desktop\\J.A.R.V.I.S\\JARVIS_OFFLINE\\DATA\\log.txt"

# Function to read history from the file
def read_history(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to write history to the file
def write_history(file_path, history):
    with open(file_path, "w") as file:
        json.dump(history, file, indent=2)

# Initialize history with a system message or read from file
history = read_history(history_file)
if not history:
    history = [
        {
            "role": "system",
            "content": "You are an intelligent assistant named JARVIS. You always provide well-reasoned answers that are both correct and helpful. Your owner, developer, creator is Daksh Mishra."
        }
    ]

while True:
    # Get user input and ensure it's not empty
    user_input = input("> ").strip()
    if not user_input:
        print("Input cannot be empty. Please provide a valid input.")
        continue

    # Add the user input to the history
    history.append({"role": "user", "content": user_input})

    try:
        # Create a chat completion request
        completion = client.chat.completions.create(
            model="TheBloke/phi-2-GGUF",
            messages=history,
            temperature=0.7,
            stream=False,
            tool_choice="auto",
        )

        # Prepare a new message from the assistant
        new_message = {"role": "assistant", "content": ""}

        # Iterate through the choices in the completion
        for choice in completion.choices:
            message = choice.message
            # Check the attributes of the message object
            if message.role == "assistant":
                # Print the assistant's response immediately
                print(message.content, end="", flush=True)
                # Add the response content to the new message
                new_message["content"] += message.content

        # Append the new message to the history
        history.append(new_message)

        # Print a new line for better readability in the console
        print()

        # Write the updated history to the file
        write_history(history_file, history)

    except openai.OpenAIError as e:
        print(f"Error occurred: {e}")
        continue
