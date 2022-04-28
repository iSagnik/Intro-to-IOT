#!/usr/local/bin/python

import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import serial

# Threshold values we determined 
MAX_VAL = 1023
MIN_VAL = 0
LDR_THRESHOLD = 10
POTEN_THRESHOLD = 100

#Normalize -> zi = (xi – min(x)) / (max(x) – min(x))
def getValues(line):
    line = line.split(":")
    poten = float(line[0])
    ldr = float(line[1])
    
    #normalize
    poten = (poten - MIN_VAL) / (MAX_VAL - MIN_VAL)
    ldr = (ldr - MIN_VAL) / (MAX_VAL - MIN_VAL)
    return (poten, ldr)

def getPayload(poten, ldr):
    # diff_poten = abs(poten - previousPoten)
    # diff_ldr = abs(ldr - previosLDR)
    # Determine if the led's should be on or off
    if(ldr > LDR_THRESHOLD and poten < POTEN_THRESHOLD):
        return "TurnOn"
    else:
        return "TurnOff"

def main():
    # Broker info 
    broker_id = "192.168.137.93"
    broker_port = 1883
    client = mqtt.Client("PI_A")
    print("Created new instance")
    # Sets the last will message
    client.will_set("Status/RaspberryPiA", "offline", retain=True)
    
    # Connect to the broker
    client.connect(broker_id, broker_port)
    
    # Publish and subscribe to topics
    client.publish("Status/RaspberryPiA", "online", retain=True)
    client.subscribe("LightStatus", qos=2)
    client.subscribe("Threshold", qos=2)

    print("Connected to broker")
    client.loop_start()
    # Gets values from the arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            poten, ldr = getValues(line)
            # Log the values of the LDR and potentiometer
            log = f"LDR: {ldr} | Poten: {poten}"
            print(log)
            client.publish("Threshold", qos=2, payload=poten)
            client.publish("LightSensor", qos=2, payload=ldr)

    client.loop_stop()
    # Done sending
    print("Done")
    client.disconnect()


if __name__ == '__main__':
	main()

