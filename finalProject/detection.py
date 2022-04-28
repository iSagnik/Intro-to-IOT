
import glob
import os
import face_recognition
import cv2
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
import numpy as np
import pickle
from database import db_utill
from database import dbInfo


import numpy as np
from psycopg2.extensions import register_adapter, AsIs

def addOwner(name):
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
            print("You quit!")
            break
    
    db_utill.addEntry("Owners", name, face_encodings)

if __name__ == "__main__":
    print("To add a new owner type add. If you don't want to add a new owner, hit any key to continue.")
    command = input()
    if command == "add":
        print("Name of Owner:")
        name = input()
        addOwner(name)
    else:
        # Get all face encodings from the db tables
        owner_rows = db_utill.getEntries("Owners")
        guest_rows = db_utill.getEntries("Guests")
        outlaw_rows = db_utill.getEntries("Outlaws")
        face_data = []
        for row in owner_rows:
            face_data.append(pickle.loads(row[2]))
        for row in guest_rows:
            face_data.append(pickle.loads(row[2]))
        for row in outlaw_rows:
            face_data.append(pickle.loads(row[2]))
        
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

            # Display the resulting image
            cv2.imshow('Video', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("You quit!")
                break
           
        for j in range(len(face_data)):
            matches = face_recognition.compare_faces (np.array(face_data[j]), np.array(face_encodings))
            print(matches)
            if matches == [True]:
                print("Match")
            else:
                print("Stranger")
           
