import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe 

def on_message(client, userdata, message):
    # Get the current time and print the topic/payload
    time = datetime.datetime.now()
    print(str(time) + ": " + str(message.topic) + " " + str(message.payload))

def main():
    # Create new client
    client = mqtt.Client()
    # Broker info
    host = "192.168.137.93"
    port = 1883
    # Connect to broker
    client.connect(host, port)
    client.on_message = on_message
    # Subscribe to all topics
    client.subscribe("LightSensor", qos = 2)
    client.subscribe("LightStatus", qos = 2)
    client.subscribe("Threshold", qos = 2)
    client.subscribe("Status/RaspberryPiA", qos = 2)
    client.subscribe("Status/RaspberryPiC", qos = 2)

   
    client.loop_forever()

if __name__ == '__main__':
	main()


