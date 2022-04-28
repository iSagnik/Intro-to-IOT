import paho.mqtt.client as mqtt
import time
import csv
from tqdm import tqdm

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

with open("./../DataFiles/1MB", "rb") as f:
    data = f.read()

broker_id = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client("Sagnik")
client.on_message=on_message
print("Created new instance")

client.connect(broker_id, broker_port)

print("Connected to broker")
client.loop_start()

print("Subscribed to topic")

times = []
for i in tqdm(range(100)):
    client.publish("tests/test1", data, qos=2)
    # print("Message sent: ", time.time())
    times.append(time.time())
client.loop_stop() #stop the loop
client.disconnect()
