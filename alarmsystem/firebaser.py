from firebase_admin import db, credentials, initialize_app, storage
import json

from datetime import datetime as dt

def connect_to_db(url: str, bucket: str, cred: str, opts: str = None) -> None:
    cred_json = credentials.Certificate(cred)
    initialize_app(
        cred_json, 
        opts, 
        {'databaseURL' : url,
         'storageBucket': bucket})
    

def fetch_face_db() -> None:

    pass


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
