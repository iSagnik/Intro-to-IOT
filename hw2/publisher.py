import paho.mqtt.client as mqtt
import time

files = ["100B", "10KB", "1MB", "10MB"]
times = [5000, 1000, 100, 10]

def main():
    bytesData = 0

    #change files according to experiment
    with open("./DataFiles/{0}".format(files[0]), "rb") as f:
        data = f.read()
        bytesData = bytearray(data)

    # Online broker info
    broker_id = "broker.hivemq.com"
    broker_port = 1883
    # Create a client
    client = mqtt.Client("Sagnik")
    print("Created new instance")

    # Connect to the broker
    client.connect(broker_id, broker_port)

    print("Connected to broker")
    client.loop_start()

    # Publish the flle to the client
    for count in range(3):
        print("Iteration: ", count)
        #change time range according to experiment
        for i in range(times[0]):
            client.publish("tests/test1", qos=1, payload=bytesData)

        client.publish("tests/test1", qos=1, payload="NEW")
        time.sleep(1)
    client.publish("tests/test1", qos=1, payload="END")

    
    
    client.loop_stop() #stop the loop

    # Done sending
    print("Done")
    client.disconnect()

if __name__ == '__main__':
	main()