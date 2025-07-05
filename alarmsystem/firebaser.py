from firebase_admin import db, credentials, initialize_app, storage
import json

from datetime import datetime as dt
import os

def connect_to_db(url: str,cred: str, opts: str = None) -> None:
    cred_json = credentials.Certificate(cred)
    initialize_app(
        cred_json, 
        opts, 
        {'databaseURL' : url})    

def check_db_updates(db_path:str, ref_path:str = '/') -> bool:
    ref = db.reference(ref_path)
    ref_conts = ref.get(shallow=True)


    db_conts = {}
    for folder in os.listdir(db_path):
        db_conts[folder] = True
    
    if db_conts == ref_conts:
        return True
    else:
        return False

def update_db(db_path:str, ref_path:str = '/') -> None:
    
    pass

def fetch_face_db() -> None:
    db_changed = check_db_updates()
    if db_changed:
        update_db()


def send_notify_img(ref_path:str, sentstuff_dbpath:str, img_path: str) -> None:
    # upload image
    bucket = storage.bucket(sentstuff_dbpath)
    blob = bucket.blob(img_path)
    blob.upload_from_filename(img_path)
    
    download_url = blob.generate_signed_url()

    # log entry
    dt_now = str(dt.now())
    ref = db.reference(ref_path)
    pusher = ref.push()
    pusher.set(
        {
            'time:' : dt_now,
            'img_url' : download_url
        }
    )
