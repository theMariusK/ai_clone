import socketio
import argparse
import json
from text_to_speech import text_to_speech
from play_audio import play_audio
from audio_device import get_output_device

# Create a Socket.IO client
sio = socketio.Client()
device_name = ""

@sio.event
def connect():
    print("Connected to the server!")
    
@sio.on('test')
def handle_test(data):
    print(f"Received test message: {data}")
    
@sio.on('conversation_input')
def handle_conversation_input(data):
    print(f"Received test message: {data}")
    audio = text_to_speech(data)
    output_device = get_output_device(device_name)
    play_audio(audio, output_device)

@sio.event
def disconnect():
    print("Disconnected from the server!")
    
    
def main():
    # Connect to the WebSocket server
    try:
        sio.connect('http://localhost:5000')
        sio.wait()  # Keep the client running
    except Exception as e:
        print(f"Error connecting to the server: {e}")
    

# Path to configuration file
CONFIG_FILE = "config.json"

def load_config(file_path):
    """
    Load the configuration file. If the file doesn't exist or contains errors,
    create a new one with user input.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuration file '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file '{file_path}': {e}")
    
    # Create new config if loading fails
    return create_config_file(file_path)

def create_config_file(file_path):
    """
    Prompt the user to create a new configuration file.
    """
    output_device_name = input("Enter the name of the output device: ")
    config = {"output_device_name": output_device_name}
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)  # Add `indent=4` for readable JSON
        print(f"Configuration file '{file_path}' created successfully.")
    except Exception as e:
        print(f"Error creating configuration file: {e}")
        return {}
    return config

# Main logic
if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Python application with arguments.")

    # Add an argument called `output_device_name`
    # parser.add_argument(
    #     "--output_device_name",
    #     type=str,
    #     required=False,
    #     help="The name of the output device to use."
    # )

    # Parse arguments
    args = parser.parse_args()

    # Call the main function with the provided argument
    # main(args.output_device_name)
    
    config = load_config(CONFIG_FILE)
    output_device_name = config.get("output_device_name", "Default Device")
    device_name = output_device_name
    print(f"Output device name: {output_device_name}")  

    # Call the main function with the extracted device name
    main()
