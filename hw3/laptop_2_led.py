import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
    

def on_message(client, userdata, message):
    # Get time 
    time = datetime.datetime.now()
    # Print time, topics, and message
    print(str(time) + ": " + str(message.topic) + " " + str(message.payload))

def main():
    # Create new client
    client = mqtt.Client()
    # Broker info
    host = "192.168.137.93"
    port = 1883
    # Connect to client
    client.connect(host, port)
    # Only get when LED 1 turns on
    client.subscribe("LightStatus")
    client.on_message = on_message
    
    
    client.loop_forever()


if __name__ == '__main__':
	main()