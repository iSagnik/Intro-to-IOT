from database import db_utill
import face_recognition
import cv2
import numpy as np
import pickle
import time
# import RPi.GPIO as GPIO
import sys, signal, time, os
from communication import send_message
import logging

# Handle ctrl-c
def interruptHandler(signal, frame):
    print("\n")
    sys.exit(0)

def open_door():
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    # GPIO.setup(18,GPIO.OUT)
    # GPIO.output(18,GPIO.HIGH)
    # time.sleep(1)
    # GPIO.output(18,GPIO.LOW)
    print("Door opened")
    #Pi stuff for led

def close_door():
    print("Door closed")
    #Pi stuff for led

def notify(number, message):
    print(message)
    # send_message(number, message)

def handle_face(encodings):
    tables = ["Owners", "Guests", "Outlaws"]
    got_match = False
    match_entry = None
    for table in tables:
        entries = db_utill.getEntries(table)

        for entry in entries:
            db_face = np.array(pickle.loads(entry[2]))
            live_face = np.array(encodings)
            try:
                matches = face_recognition.compare_faces (db_face, live_face)
                if matches == [True]:
                    got_match = True
                    match_entry = (entry, table)
            except:
                return False
    return (got_match, match_entry, encodings)

def start_camera():
    print("To capture your face encoding press q")
    face_encodings = []
    process_this_frame = True
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations( rgb_small_frame)
            face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
           
        process_this_frame = not process_this_frame
        # Display the resulting image
        cv2.imshow('Video', frame)
        
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
            print("Camera stopped")
            break
    return face_encodings

def handle_face_helper(data):
    got_match, match_entry, encodings = data
    is_door_open = False
    if not got_match:
        #stranger
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(17,GPIO.OUT)
        # GPIO.output(17,GPIO.HIGH)
        # time.sleep(1)
        # GPIO.output(17,GPIO.LOW)        
        # notify("+19199958852", "Stranger at the door")

        opt = input("1. Add stranger as a guest\n 2. Open Door\n 3. Do nothing")
        if opt == "1":
            name = input("Enter guest name: ")
            validity = db_utill.addEntry("Guests", name, encodings)
            if not validity:
                logging.info("Could not add guest. Error in db code. Door opened")
            is_door_open = True
            open_door()
        elif opt == "2":
            is_door_open = True
            open_door()
        else:
            return True
            
    elif match_entry[1] == "Owners":
        notify("+19199958852", "Welcome home darling!")
        is_door_open = True
        open_door()

    elif match_entry[1] == "Guests":
        msg = f"Guest {match_entry[0][1]} has entered the home"
        #validate later
        notify("+19199958852", msg)
        is_door_open = True
        open_door()
    elif match_entry[1] == "Outlaws":
        msg = f"An outlaw: {match_entry[0][1]} is at your door. Call law enforcement"
        notify("+19199958852", msg)
    if is_door_open:
        input("Press enter to close door")
        close_door()
        time.sleep(2)
        clearMenu()
    return True

def removeTableEntry(table_name):
    #print all entries
    entries = db_utill.getEntries(table_name)
    if table_name == "Owners" and len(entries) == 1:
        print("Cannot remove an owner when there is only one!")
        return
    for idx, entry in enumerate(entries):
        print(idx + 1, " Name: ", entry[1])
    #get which to remove by index + 1
    choice = int(input("Enter index of person to remove? ")) - 1
    if choice < 0 or choice > len(entries) - 1:
        print("Learn to read dude, try again.")
        print("Returning to menu...")
        time.sleep(5)
        clearMenu()
    else:
        #remove
        validity = db_utill.removeEntry(table_name, entries[choice][1])
        if not validity:
            print("Some error dude")

def addOwner(name):
    print("To capture your face encoding press q")
    face_encodings = []
    process_this_frame = True
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations( rgb_small_frame)
            face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
            
        process_this_frame = not process_this_frame
        
        # Display the resulting image
        cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
            logging.info("Face Captured!")
            break
    
    return db_utill.addEntry("Owners", name, face_encodings)

def print_menu():
    print (22 * "-" , "Smart Door Dashboard" , 23 * "-")
    print("1: Remove an Owner")
    print("2: Remove a  Guests")
    print("3: Add an Owner")
    print("4: Request Entry")
    print("5: Quit")
    print (67 * "-")

def clearMenu():
    os.system('clear')

def menu():
    signal.signal(signal.SIGINT, interruptHandler)
    while True:
        print_menu()
        opt = input("Option: ")
        if opt == "1":
            removeTableEntry("Owners")
        elif opt == "2":
            removeTableEntry("Guests")
        elif opt == "3":
            print("Name of Owner: ")
            name = input()
            addOwner(name)
        elif opt == "4":
            encodings = start_camera()
            if len(encodings) == 0:
                print("No face detected")
            data = handle_face(encodings)
            if data != False and not handle_face_helper(data):
                logging.warning("Could not get a good reading, try again!")
        elif opt == '5':
            quit()
        else:
            print("Please select an available menu option. Try again.")
            time.sleep(2)
            clearMenu()

if __name__=="__main__":
    menu()