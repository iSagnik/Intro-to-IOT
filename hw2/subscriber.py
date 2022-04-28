from os import times
import paho.mqtt.client as mqtt
import time
import csv
import sys
from statistics import mean, stdev

times = []
sizes = []
file_sizes = [100, 10000, 1000000, 10000000]
total_times = []
count = 0
def on_message(client, userData, message):
    global count
    count += 1
    if(count % 100 == 0):
        print(count)
    global times
    # Determines when the file is done sending
    if message.payload == b'END':
        client.disconnect()
    elif message.payload == b'NEW':
        print("File done")
        # Calculates the total time taken, the number of packets, and the bytes per second
        time_taken = times[-1] - times[0]
        total_times.append({
            "time_taken": time_taken,
            "packet_count": len(times),
            "bytesPerSec": (len(times) / time_taken) * file_sizes[0]
        })
        times = []
    else:
        # If the packet is not done sending, keep adding time
        times.append(time.time())
        size = sys.getsizeof(message.payload)
        # print(size)
        #change file size accroding to experiment
        sizes.append(size / file_sizes[0])

def main():
    #Create a new client instance
    client = mqtt.Client("Lauren")
    client.on_message=on_message
    print("Created new instance")

    # Online broker 
    broker_id = "broker.hivemq.com"
    broker_port = 1883

    # Connect to the broker
    client.connect(broker_id, broker_port)
    client.subscribe("tests/test1", qos=1)
    print("Subscribed to topic")

    client.loop_forever()

    total_time_list = []
    bytes_sec_list = []
    packet_count_list = []

    # Gets the total time, bytes per second, and packet count
    for count, stat in enumerate(total_times):
        print("Iteration: ", count)
        total_time_list.append(stat["time_taken"])
        bytes_sec_list.append(stat["bytesPerSec"])
        packet_count_list.append(stat["packet_count"])

    # Calculates the average, standard deviation, and average app layer data transfered
    print("Time average : ", mean(total_time_list))
    print("Time stdev: ", stdev(total_time_list))

    print("Avg packet count: ", mean(packet_count_list))

    print("Avg bytes / second: ", mean(bytes_sec_list))
    print("Stdev bytes / second: ", stdev(bytes_sec_list))
    
    print("Size avg / exp file size: ", mean(sizes))

    with open("timestamps_r_100.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(times)

if __name__ == '__main__':
	main()