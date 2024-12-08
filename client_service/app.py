import socketio

# Create a Socket.IO client
sio = socketio.Client()


@sio.event
def connect():
    print("Connected to the server!")
    
    
@sio.on('audio_chunk')
def handle_audio_chunk(data):
    print(f"Received audio chunk of size: {len(data)}")
    
@sio.on('test')
def handle_test(data):
    print(f"Received test message: {data}")
    
@sio.on('conversation_input')
def handle_test(data):
    with open('received_audio.wav', 'wb') as f:
        f.write(data)
    print(f"Received test message: {data}")
    

@sio.event
def disconnect():
    print("Disconnected from the server!")
    
    
# Connect to the WebSocket server
try:
    sio.connect('http://localhost:5000')
    sio.wait()  # Keep the client running
except Exception as e:
    print(f"Error connecting to the server: {e}")