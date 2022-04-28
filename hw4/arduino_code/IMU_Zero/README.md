Use the following command to compile the sketch for the arduino
arduino-cli compile --fqbn arduino:avr:mega IMU_Zero.ino

Then use the following command to upload the sketch to the arduino 
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega IMU_Zero.ino

If you want to view the output of the code, use the following command
screen /dev/ttyACM0