import time
import os, json
import wiotp.sdk.application

client = None

def commandCallback(event):
    if event.eventId == "doorStatus":
        # Received event 'doorStatus' 
        payload = json.loads(event.payload)
        # Get the status and time
        status = payload['status']
        time = payload['time']
        print("Status: " + status)
        print("Time: " + time)
    
def main():
    try:
        # Try and connect the client to the IBM Server
        options = wiotp.sdk.application.parseConfigFile("application.yaml")
        client = wiotp.sdk.application.ApplicationClient(config=options)
        client.connect()
        while True:
            # Continually subscribe to the event and call the callback function
            client.deviceEventCallback = commandCallback
            client.subscribeToDeviceEvents(eventId="doorStatus")
            time.sleep(0.1)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()