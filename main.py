import netifaces as ni
import pyttsx3
import time
import requests

def get_available_adapters():
    """
    Retrieves the list of available network adapters along with their IP addresses.
    """
    interfaces = ni.interfaces()
    adapters = {}
    for adapter in interfaces:
        addresses = ni.ifaddresses(adapter)
        if ni.AF_INET in addresses:
            ip_address = addresses[ni.AF_INET][0]['addr']
            adapters[adapter] = ip_address
    return adapters

def check_network_connection(adapters):
    """
    Checks if any of the adapters are connected to the network by accessing a well-known external IP address.
    Returns True if at least one adapter is connected, False otherwise.
    """
    url = "http://example.com"  # Replace with a well-known external IP address or URL
    for adapter, ip_address in adapters.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
    return False

def text_to_speech(text):
    """
    Converts the given text to speech using pyttsx3 library.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Speed of speech
    engine.setProperty("volume", 0.8)  # Volume (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()

# While not connected, wait and announce "Waiting for network connection"
connected = False
print("TTS NW CONTROLLER")
text_to_speech("Waiting for network connection")
while not connected:
    adapters = get_available_adapters()
    connected = check_network_connection(adapters)
    time.sleep(1)

# Once connected, announce "System is connected"
time.sleep(2)
text_to_speech("System is connected. Connection status will be controlled every 30 seconds")

time.sleep(1)
text_to_speech("All detected ip addresses are as follows")

# Initialize variable for last known connection status
last_connected = connected

# Print and speak the initial IP addresses one by one
for i, (adapter, ip_address) in enumerate(adapters.items()):
    if ip_address != "127.0.0.1":
        index = i + 1
        print("IP Address number", index, ":", ip_address)
        text_to_speech("IP Address number " + str(index) + ": " + ip_address)
        break

# Continue checking for changes in IP addresses and network connectivity in the background
while True:
    time.sleep(30)

    # Fetch the current IP addresses from the adapters
    new_adapters = get_available_adapters()

    # Check if the network connection is restored
    connected = check_network_connection(new_adapters)

    if connected and not last_connected:
        # If the connection was restored, announce "System connection restored"
        text_to_speech("System connection restored")

        # Print and speak the updated IP addresses one by one
        for i, (adapter, ip_address) in enumerate(new_adapters.items()):
            if ip_address != "127.0.0.1":
                index = i + 1
                print("IP Address number", index, ":", ip_address)
                text_to_speech("IP Address number " + str(index) + ": " + ip_address)
    
    elif not connected and last_connected:
        # If the connection was lost, announce "Connection lost waiting for  connection to be restored."
        text_to_speech("Connection lost. Waiting for  connection to be restored.")

    # Update the last known connection status
    last_connected = connected

