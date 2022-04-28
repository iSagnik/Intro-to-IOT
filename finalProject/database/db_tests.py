import pytest
from database import db_utill
import numpy as np
'''
Run tests:
>> pytest db_tests.py
'''

#fixture function to clear db
@pytest.fixture(scope="module", autouse=True)
def clear_db():
    #test table name check
    assert db_utill.checkTableName("LALALA") == False
    assert db_utill.clearAll() == True

def test_db_functions():

    #verify 0 entries
    owners = db_utill.getEntries("Owners")
    assert len(owners) == 0

    guests = db_utill.getEntries("Guests")
    assert len(guests) == 0

    outlaws = db_utill.getEntries("Outlaws")
    assert len(outlaws) == 0

    #add entries
    entries = [
        ("Sagnik", "Owners", np.array([2.5, 7, 10])),
        ("Stark", "Guests", np.array([8, 6, 4, 9])),
        ("Joker", "Outlaws", np.array([6.35, 9, 0, 1.11, 56])),
        ("Harley Quinn", "Outlaws", np.array([6.35, 9, 0, 1.11, 56, 101.9867, 45.2368]))
    ]

    for entry in entries:
        table = entry[1]
        name = entry[0]
        face_data = entry[2]
        assert db_utill.addEntry(table, name, face_data) == True

    #verify addition
    owners = db_utill.getEntries("Owners")
    assert len(owners) == 1

    guests = db_utill.getEntries("Guests")
    assert len(guests) == 1

    outlaws = db_utill.getEntries("Outlaws")
    assert len(outlaws) == 2

    #prevent duplicate
    assert db_utill.addEntry("Owners", "Sagnik", np.array([2.5, 7, 10])) == False

    #delete entries
    assert db_utill.removeEntry("Outlaws", "Joker") == True
    assert db_utill.removeEntry("Guests", "Stark") == True

    #verify deletion
    owners = db_utill.getEntries("Owners")
    assert len(owners) == 1

    guests = db_utill.getEntries("Guests")
    assert len(guests) == 0

    outlaws = db_utill.getEntries("Outlaws")
    assert len(outlaws) == 1