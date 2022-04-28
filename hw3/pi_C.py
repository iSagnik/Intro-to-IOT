import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import signal
# Globally set the status, lightsensor, and threshold
status = False
lightSensor = 0.0
threshold = 0.0
def on_message(client, userData, message):
    global status, lightSensor, threshold
    # Get the last status to compare
    last = status
    # Get the threshold and light sensor values
    if (message.topic == "LightSensor"):
        lightSensor = float(message.payload)
        print(f"Light Sensor Value: {lightSensor}")
    elif (message.topic == "Threshold"):
        threshold = float(message.payload)
        print(f"Threshold Value: {threshold}")

    # Set the status to determine if the light should be on 
    # or off.
    status = lightSensor <= threshold
    print(f"Current status: {status}")
    if (status != last):
        if (status):
            payload = "TurnOn"
        else:
            payload = "TurnOff"
        # Publish so pi B can actually turn the LED on/off
        client.publish("LightStatus", payload, retain=False)

def main():
    broker_id = "192.168.137.93"
    broker_port = 1883
    client = mqtt.Client("PI_C")
    client.on_message = on_message
    print("Created new instance")
    
    client.will_set("Status/RaspberryPiC", "offline", qos=2, retain=True)
    # Connect to the broker
    client.connect(broker_id, broker_port)
    client.publish("Status/RaspberryPiC", "online", retain=True)
    
    
    client.subscribe("LightSensor", qos=2)
    client.subscribe("Threshold", qos=2)

    print("Connected to broker")

    
    client.loop_forever()

if __name__ == '__main__':
	main()
