from firebase_admin import db, credentials, initialize_app
import json

from supabase import create_client, Client
import requests

from datetime import datetime as dt
import os, json, shutil

fb_url = ''
fb_cred_path = ''
fb_app = None
FB_DB = 'face_db'
FB_UPLOADS = 'history'

sb_url = ''
sb_key = ''
supabaser:Client = None
SB_BUCKET = 'door-smart-security'

LOCAL_DB = './alarmsystem/resources/face_database'

def check_net() -> bool:
    pass

def load_creds(jsn_file: str) -> None:
    global fb_url 
    global fb_cred_path 
    global sb_url 
    global sb_key 

    with open(jsn_file, 'r') as file:
        properties = json.load(file)

    fb_url = properties['firebase_db']['url']
    fb_cred_path = properties['firebase_db']['cert_path']
    sb_url = properties['supabase_db']['url']
    sb_key = properties['supabase_db']['key']

def connect_to_dbs(cred_path: str) -> None:
    global supabaser
    load_creds(cred_path)

    cred_json = credentials.Certificate(fb_cred_path)
    fb_app = initialize_app(
        cred_json, 
        {'databaseURL' : fb_url})

    supabaser = create_client(sb_url, sb_key)
    
    # print("connect firebase: " + str(fb_app))
    # print("connect supabase: " + str(supabaser))    

def check_db_updates(db_path:str = LOCAL_DB, ref_path:str = FB_DB) -> bool:
    ref = db.reference(ref_path)
    ref_conts = ref.get(shallow=True)
    print(str(ref_conts))

    db_conts = {}
    for folder in os.listdir(db_path):
        name, ext = os.path.splitext(folder)
        # print("ext is " + ext)
        if ext == "":
            db_conts[folder] = True
            # print(folder)
        else:
            # print("whoops")
            pass
    # print(str(db_conts))

    if db_conts == ref_conts:
        print("they equal tho")
        return False
    else:
        print("its wrong")
        return True

def update_db(db_path:str = LOCAL_DB, ref_path:str = FB_DB) -> None:
    # clear database
    for directory in os.listdir(db_path):
        shutil.rmtree(db_path + '/'+ directory)

    # download new database
    print("get in " + ref_path)
    ref = db.reference(ref_path).get()
    if ref is None:
        return
    
    for ref_key, user in ref.items():
        # make folder
        print(user['user_name'])
        os.mkdir( LOCAL_DB + '/' + user['user_name'])
        
        # download img
        try:
            img_name = user['user_name'] + '.jpg'
            img_dir = LOCAL_DB + '/' + user['user_name'] + '/' +  img_name
            response = requests.get(user['user_img_url'], stream=True)
            response.raise_for_status() 
            with open(img_dir, 'wb+') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(user['user_name'] + " downloaded")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")

def fetch_face_db() -> None:
    db_changed = check_db_updates()
    if db_changed:
        print("updating db...")
        update_db()

def upload_entry(img_path: str, ref_path:str= FB_UPLOADS, sentstuff_dbpath:str = SB_BUCKET) -> None:
    dt_now = dt.now()

    # upload image
    img_name, img_type = os.path.splitext(img_path)
    subfolders = 'pi-captures/'
    upload_name = subfolders + str(dt_now) + img_type   
    # print("uploading :" + upload_name)
    with open(img_path, 'rb') as f:
        (supabaser.storage
        .from_('door-smart-security')
        .upload(
            file=f,
            path=upload_name,
            file_options={
                "cache-control": "3600", 
                "content-type": "image",
                "upsert": "false"})
        )
    # print("saved to supabase : " + upload_name)
    img_url = (
        supabaser.storage
        .from_(sentstuff_dbpath)
        .get_public_url(upload_name)
    )

    # log entry
    ref = db.reference(ref_path)
    pusher = ref.push()
    pusher.set(
        {
            'entry_date' : str(dt_now.strftime("%D")),
            'entry_time' : str(dt_now.strftime("%H:%M:%S")),
            'entry_img_url' : img_url
        }
    )

    print("upload complete")
