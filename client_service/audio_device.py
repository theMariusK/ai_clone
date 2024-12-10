import sounddevice as sd

def get_output_device(device_name: str):
    selected_device = 0
    for idx, device in enumerate(sd.query_devices()):
        if device['name'] == device_name:
            return idx
    print(f"Device {device_name} not found. Using default device.")
    return selected_device