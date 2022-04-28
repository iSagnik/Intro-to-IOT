import paho.mqtt.client as mqtt
import time
import csv
isEnd = False

def on_message(client, userdata, message):
    times.append(time.time())
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)

times = []
client = mqtt.Client("Lauren")
client.on_message=on_message
print("Created new instance")

broker_id = "broker.hivemq.com"
broker_port = 1883

client.connect(broker_id, broker_port)
client.subscribe("tests/test1", qos=2)
print("Subscribed to topic")


# if counter > 100001:
#     with open("timestamps_r_100.csv", 'w', newline='') as myfile:
#         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#         wr.writerow(times)
#     client.loop_stop()
#     quit()
client.loop_start()
time.sleep(300)
client.loop_stop()
print(str(times[-1] - times[0]))
print(len(times))
with open("timestamps_r_100.csv", 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(times)
