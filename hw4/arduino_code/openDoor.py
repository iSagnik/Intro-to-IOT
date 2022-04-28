import serial
import csv
import time
import sys


def getValues(line):
    line = line.split(":")
    ax = float(line[0])
    ay = float(line[1])
    az = float(line[2])
    gx = float(line[3])
    gy = float(line[4])
    gz = float(line[5])
    
    return line

def main():
    # Gets values from the arduino
    counter = 0
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            # ax, ay, az, gx, gy, gz, false 
            data = getValues(line)
            data.append(' 0')
            print(data)
            with open('openDoor50.csv', 'a') as f:
                # create the csv writer
                writer = csv.writer(f)

                # write a row to the csv file
                writer.writerow(data)
                counter = counter + 1
            
            
if __name__ == '__main__':
	main()