from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, redirect
import atexit, os, json, datetime, sys, time
import wiotp.sdk.application
import signal
import logging
from joblib import load

# Load our trained ML model
door_model = load('./door_model.joblib')
app = Flask(__name__, static_url_path='')
# Set the client to none originally
client = None
# Define an array where our imu values will be stored
sensorValues = []
# Define the port
port = int(os.getenv('PORT', 8000))

# Create a json object for the last received data
lastReceivedData = {
    # Get the gyroscope x-column from the data
    "gyr_x": 0,
    "gyr_y": 0,
    "gyr_z": 0,
    "acc_x": 0,
    "acc_y": 0,
    "acc_z": 0,
    # Include a timestamp
    "time": str(datetime.datetime.now())
}

# Create a json object for the door status
currentDoorStatus = {
    # Start the status as closed
    "status": "closed",
    # Include a timestamp
    "time": str(datetime.datetime.now())
}

def myCommandCallback(event):
    global lastReceivedData, sensorValues, door_model, currentDoorStatus
    if event.eventId == "imu_data":
        # Received event 'imu_gyro' from RaspberryPi:1 as a JSON object
        # Extract that data into a JSON object
        payload = json.loads(event.payload)
        # Get the gyroscope x value from the payload
        Gx = payload['gyr_x']
        Gy = payload['gyr_y']
        Gz = payload['gyr_z']
        Ax = payload['acc_x']
        Ay = payload['acc_y']
        Az = payload['acc_z']
        combinedData = [Gx, Gy, Gz, Ax, Ay, Az]
        # Store whatever else we got into our lastReceievedData JSON object
        lastReceivedData = {
            # Get the gyroscope x-column from the data
            "gyr_x": payload['gyr_x'],
            # Get the gyroscope y-column from the data
            "gyr_y": payload['gyr_y'],
            # Get the gyroscope z-column from the data
            "gyr_z": payload['gyr_z'],
            # Get the accelerometer x-column from the data
            "acc_x": payload['acc_x'],
            # Get the accelerometer y-column from the data
            "acc_y": payload['acc_y'],
            # Get the accelerometer z-column from the data
            "acc_z": payload['acc_z'],
            # Include a timestamp
            "time": str(datetime.datetime.now())
        }
    # If the gyroscope x value is greater than 1.0, this means the door is being opened.
    if (Gx > 0.5):
        # print(sensorValues) # debugging
        prediction = str(door_model.predict([combinedData]))
        # print(prediction) # debugging
        if (prediction == '[0.]'):
            currentDoorStatus['status'] = 'CLOSED'
        else:
            currentDoorStatus['status'] = 'OPEN'
        # Get the timestamp
        currentDoorStatus['time'] = str(datetime.datetime.now())
        # print(currentDoorStatus) # debugging
        # Publish the model's decision to a DIFFERENT EVENTID
        client.publishEvent(typeId="RaspberryPi", deviceId="2", eventId="doorStatus", msgFormat="json", data=currentDoorStatus, qos=2)
# If the gyroscope x value is less than -1.0, this means the door is being closed.
    elif (Gx < -0.5):
        # print(sensorValues) # debugging
        prediction = str(door_model.predict([combinedData]))
        # print(prediction) # debugging
        if (prediction == '[0.]'):
            currentDoorStatus['status'] = 'CLOSED'
        else:
            currentDoorStatus['status'] = 'OPEN'
        # Get the timestamp
        currentDoorStatus['time'] = str(datetime.datetime.now())
        # print(currentDoorStatus) # debugging
        # Publish the model's decision to a DIFFERENT EVENTID
        client.publishEvent(typeId="RaspberryPi", deviceId="2", eventId="doorStatus", msgFormat="json", data=currentDoorStatus, qos=2)

# Handle ctrl-c
def interruptHandler(signal, frame):
    client.disconnect()
    sys.exit(0)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

# Load index.html as our frontend
@app.route('/')
def root():
    return app.send_static_file('index.html')

# /doorStatus API route where the current status of the door will be displayed
@app.route('/doorStatus', methods=['GET', 'POST', 'PUT'])
def getDoorStatus():
    global currentDoorStatus
    return jsonify(currentDoorStatus)

# /lastReceivedData API where the last received values from the sensor will be displayed
@app.route('/lastReceivedData', methods=['GET', 'POST', 'PUT'])
def getLastReceivedData():
    global lastReceivedData
    return jsonify(lastReceivedData)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, interruptHandler)

    # Setup login configuration
    options = wiotp.sdk.application.parseConfigFile("application.yaml")
    client = wiotp.sdk.application.ApplicationClient(config=options)

    # Create a debugger logger
    # client.logger.setLevel(logging.DEBUG)
    # Connect to the ibmcloud
    client.connect()
    # Trigger myCommandCallback every time a message is receieved
    client.deviceEventCallback = myCommandCallback
    # Subscribe to the imu_gyro topic
    client.subscribeToDeviceEvents(eventId="imu_data")
    app.run(host='0.0.0.0', port=port, debug=True)