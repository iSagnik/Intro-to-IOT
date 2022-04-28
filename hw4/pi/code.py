import RPi.GPIO as GPIO
import time
import os, json
import wiotp.sdk.application
import uuid

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)

client = None
   
def lightEventCallback(evt):
    payload = json.dumps(evt.data).strip("{\" }").replace('"','').split(":")
    command = payload[1].lstrip(' ')
    
    if command == "on":
            print("Turning On")
            GPIO.output(18, True)
    elif command == "off":
            print("Turning Off")
            GPIO.output(18, False)
		
def publishEventCallback():
	print("Published.")

try:
    options = wiotp.sdk.application.parseConfigFile("application.yaml")
    client = wiotp.sdk.application.ApplicationClient(config=options)
    client.connect()
    client.subscribeToDeviceEvents(eventId="light")
    client.deviceEventCallback = lightEventCallback

    while True:
        eventData = {'Test' : True}
        client.publishEvent(typeId="RaspberryPi", deviceId="1", eventId="RegularUpdate", msgFormat="json", data=eventData, onPublish=publishEventCallback)
        time.sleep(5)
except Exception as e:
    print("Exception: ", e)



