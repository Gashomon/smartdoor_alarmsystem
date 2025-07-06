from firebase_admin import db, credentials, initialize_app, storage
import json

from datetime import datetime as dt

import os

file_path = ''
find_file = os.path.exists(file_path)
print("file exists is " + str(find_file))
cred_json = credentials.Certificate(file_path)
initialize_app(
    cred_json, 
    {'databaseURL' : ''})

try:
    ref = db.reference('/')
    data = ref.get()
    print("data is this: " + str(data))
    print("data type is " + type(data))

    print('\n')
    data = db.reference('face_db').get(shallow=True)
    kys = list(data.keys())
    print("data is this: " + str(kys))
    print("data type is " + type(kys))

    
except Exception as e:
    print("this is error: " + str(e))
