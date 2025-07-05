from firebase_admin import db, credentials, initialize_app, storage
import json

from datetime import datetime as dt

import os

file_path = 'D:\\MON Stuff\\Work Stuff\\SmartDoor\\smartdoor_alarmsystem\\alarmsystem\\resources\\sd_acckey.json'
find_file = os.path.exists(file_path)
print("file exists is " + str(find_file))
cred_json = credentials.Certificate(file_path)
initialize_app(
    cred_json, 
    {'databaseURL' : 'https://door--smart-security-default-rtdb.asia-southeast1.firebasedatabase.app/'})

try:
    ref = db.reference('/')
    data = ref.get()
    print("data is this: " + str(data))
    print("data type is " + str(data))

    data_set = ref.set(
        {
            'key1' : 'val1',
            "key2" : "val2"
        }
    )
    print("data is this: " + str(data))
    print("data type is " + str(data))
except Exception as e:
    print("this is error: " + str(e))
