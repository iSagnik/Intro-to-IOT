import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
#set up each LED GPIO pin
LED_1 = 17
LED_2 = 18
LED_3 = 27

#[LED 1, LED 2, LED 3]
LED_STATUS ={"17": False, "18": False, "27": False}

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_1, GPIO.OUT)
GPIO.setup(LED_2, GPIO.OUT)
GPIO.setup(LED_3, GPIO.OUT)

# Turns the LED on
def switchOn(led_id):
    if not LED_STATUS[str(led_id)]:
        GPIO.output(led_id, True)
        LED_STATUS[str(led_id)] = True

# Turns the LED off
def switchOff(led_id):
    if LED_STATUS[str(led_id)]:
        GPIO.output(led_id, False)
        LED_STATUS[str(led_id)] = False

def on_message(client, userData, message):
    # Gets the message and switch on or off depending on
    # the topic and online/offline status
    msg = message.payload.decode("utf-8")
    print(msg)
    if message.topic == "LightStatus":
        if msg == "TurnOff":
            switchOff(LED_1)
        elif msg == "TurnOn":
            switchOn(LED_1)
    elif message.topic == "Status/RaspberryPiA":
        if msg == "online":
            switchOn(LED_2)
        elif msg == "offline":
            switchOff(LED_2)
    elif message.topic == "Status/RaspberryPiC":
        if msg == "online":
            switchOn(LED_3)
        elif msg == "offline":
            switchOff(LED_3)
            switchOff(LED_1)
def main():
    #Create a new client instance
    client = mqtt.Client("PI_B")
    client.on_message=on_message
    print("Created new instance")

    # Broker info 
    broker_id = "192.168.137.93"
    broker_port = 1883

    # Connect to the broker
    client.connect(broker_id, broker_port)
    client.subscribe("LightStatus", qos=2)
    client.subscribe("Status/RaspberryPiA", qos=2)
    client.subscribe("Status/RaspberryPiC", qos=2)
    print("Subscribed to topic")

    client.loop_forever()

if __name__ == '__main__':
	main()