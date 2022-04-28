from flask import Flask, request, jsonify
from main import *
from database import db_utill
import logging
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'itsasecret!10'
app.config['CORS_HEADERS'] = 'Content=Type'
DOOR_OPEN = False
cur_encodings = None

sem = threading.Semaphore()

@app.route("/openDoor")
def open_the_door():
    print("Door opened")
    sem.acquire()
    global DOOR_OPEN
    DOOR_OPEN = True
    open_door()
    sem.release()

@app.route("/closeDoor", methods=["POST"])
def close_the_door():
    logging.info("Door closed")
    sem.acquire()
    global DOOR_OPEN
    DOOR_OPEN = False
    close_door()
    sem.release()

    return jsonify(True)

@app.route("/addOwner", methods=["POST"])
def add_owner():
    name = request.args.get("name")
    msg = f"Adding Owner: {name}"
    logging.info(msg)
    res = addOwner(name)
    res = True
    return jsonify(res)

@app.route("/getEntries",  methods=["GET"])
def get_entries():
    table_name = request.args.get("tableName")
    entries = db_utill.getEntries(table_name)
    result = []
    if entries == False:
        return jsonify(entries)
    for entry in entries:
        result.append((entry[1]))
    return jsonify(result)

@app.route("/removeTableEntry",  methods=["POST"])
def remove_table_entry():
    table_name = request.args.get("tableName")
    name = request.args.get("name")
    validity = db_utill.removeEntry(table_name, name)
    if not validity:
        return jsonify(False)
    else:
        return jsonify(True)

@app.route("/")
def main():
    return "lol"

@app.route("/requestEntry")
def request_entry():
    global DOOR_OPEN
    global cur_encodings

    encodings = start_camera()
    if len(encodings) == 0:
        logging.info("No face detected")
    if not handle_face(encodings):
        logging.warning("Could not get a good reading, try again!")
    data = handle_face(encodings)
    if data == False:
        return {"msg": "Could not get a good reading, please try again!", "table": "Error" }
    got_match, match_entry, encodings = data
    
    if not got_match:
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(17,GPIO.OUT)
        # GPIO.output(17,GPIO.HIGH)
        # time.sleep(1)
        # GPIO.output(17,GPIO.LOW)
        sem.acquire()
        cur_encodings = encodings
        sem.release()
        return {"msg": "", "table": "Stranger"}
        
    elif match_entry[1] == "Owners":
        msg = "Welcome home darling!"
        notify("+19199958852", msg)
        sem.acquire()
        DOOR_OPEN = True
        open_door()
        sem.release()
        return {"msg": msg, "table": "Owners"}
    elif match_entry[1] == "Guests":
        msg = f"Guest {match_entry[0][1]} has entered the home"
        #validate later
        notify("+19199958852", msg)
        sem.acquire()
        DOOR_OPEN = True
        open_door()
        sem.release()
        return {"msg": msg, "table": "Guests"}
    elif match_entry[1] == "Outlaws":
        msg = f"An outlaw: {match_entry[0][1]} is at your door. Call law enforcement"
        notify("+19199958852", msg)
        return {"msg": msg, "table": "Outlaws"}
    
@app.route("/handleStranger", methods=["POST"])
def handleStranger():
    global DOOR_OPEN
    global cur_encodings
    opt = request.args.get("option")
    result = True
    if opt == "1":
        name = request.args.get("name")
        if cur_encodings is not None:
            encodings = cur_encodings
            cur_encodings = None
        else:
            logging.error("Idk how this happened but lol")
            return jsonify(False)
        validity = db_utill.addEntry("Guests", name, encodings)
        if not validity:
            logging.info("Could not add guest. Error in db code. Door opened")
            result = False
        sem.acquire()
        DOOR_OPEN = True
        open_door()
        sem.release()
    elif opt == "2":
        sem.acquire()
        DOOR_OPEN = True
        open_door()
        sem.release()
    return jsonify(result)
        
if __name__ == '__main__':
    app.run()

