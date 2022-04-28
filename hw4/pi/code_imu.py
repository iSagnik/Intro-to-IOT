# Code from https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi

import smbus			#import SMBus module of I2C
from time import sleep          
import wiotp.sdk.application
import signal, sys, csv
import time

# some MPU6050 Registers and their Address
# https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
client = None

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address (sudo i2cdetect -y 1)

def publishAccCallback():
    print("Accelerometer Published.")
def publishGyroCallback():
    print("Gyroscope Published.")

def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)
    
    # to get signed value from mpu6050
    if value > 32768:
        value = value - 65536
    return value

def signal_handler(sig, frame):
    sys.exit(0)

def main():
    # Handle ctrl-c
    signal.signal(signal.SIGINT, signal_handler)
    
    MPU_Init()

    print(" Reading Data of Gyroscope and Accelerometer")

    try:
        # Try logging into the cloud
        options = wiotp.sdk.application.parseConfigFile("application.yaml")
        client = wiotp.sdk.application.ApplicationClient(config=options)
        client.connect()

        while True:
                
            #Read Accelerometer raw value
            acc_x = read_raw_data(ACCEL_XOUT_H)
            acc_y = read_raw_data(ACCEL_YOUT_H)
            acc_z = read_raw_data(ACCEL_ZOUT_H)
            
            #Read Gyroscope raw value
            gyro_x = read_raw_data(GYRO_XOUT_H)
            gyro_y = read_raw_data(GYRO_YOUT_H)
            gyro_z = read_raw_data(GYRO_ZOUT_H)
            
            # Calibrate based on the value range
            Ax = acc_x/16384.0
            Ay = acc_y/16384.0
            Az = acc_z/16384.0
            
            Gx = gyro_x/131.0
            Gy = gyro_y/131.0
            Gz = gyro_z/131.0
            
            # Get the accelerometer data from the pi
            acc_event_data = {'acc_x': Ax, 'acc_y': Ay, 'acc_z': Az}
            # Get the gyroscope data from the pi
            gyr_event_data = {'gyr_x': Gx, 'gyr_y': Gy, 'gyr_z': Gz}
 # Combine the accelerometer data and the gyroscope data into a single array
            combined_event_data = {'gyr_x': Gx, 'gyr_y': Gy, 'gyr_z': Gz, 'acc_x': Ax, 'acc_y': Ay, 'acc_z': Az}
            
            # If the second argument when running code_imu is "publish", then publish the data
            if (sys.argv[1] == "publish"):
                # Publish the accelerometer data to the "imu_acc" topic
                # client.publishEvent(typeId="RaspberryPi", deviceId="1", eventId="imu_acc", msgFormat="json", data=acc_event_data, qos=2, onPublish=publishAccCallback)
                # Publish the gyroscope data the "imu_gyro" topic
                # client.publishEvent(typeId="RaspberryPi", deviceId="1", eventId="imu_gyro", msgFormat="json", data=gyr_event_data, qos=2, onPublish=publishGyroCallback)
                client.publishEvent(typeId="RaspberryPi", deviceId="1", eventId="imu_data", msgFormat="json", data=combined_event_data, qos=2, onPublish=publishGyroCallback)
            
            # If the second argument when running code_imu is "collect" then we are collecting data
            elif (sys.argv[1] == "collect"):

                # Get the current time when the program starts
                timestr = time.strftime("%Hh%Mm%Ss")
                # Are collecting a door opening motion?
                if (sys.argv[2] == "open"):
                    timestr = "../door_data/open/" + timestr
                # Or are we collecting a door closing motion?
                elif (sys.argv[2] == "close"):
                    timestr = "../door_data/close/" + timestr
                filename = timestr + "_data.csv"

                # Start writing the data you're collecting from the door motion to a csv file
                with open(filename, 'a') as f:
                    # create the csv writer
                    writer = csv.writer(f)

                    # write a row to the csv file
                    writer.writerow(combined_event_data)
            # Print out whatever is collected during the data collection process
            print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
            sleep(0.1)
    except Exception as e:
        print("Exception: ", e)
        

if __name__ == '__main__':
	main()