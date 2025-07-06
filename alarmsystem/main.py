import sys_manager as sm
import recognizer as rcg
import firebaser as fbr
import arduino_talker as at

os_type = 'unknown'
os_is_raspi = False
system_dir = ''

firebase_url = 'https://door--smart-security-default-rtdb.asia-southeast1.firebasedatabase.app/'
firebase_credentials = ''

supabase_url = 'https://tlgkpnmiwlqqkxzoequy.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsZ2twbm1pd2xxcWt4em9lcXV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MzIyNjYsImV4cCI6MjA2NzMwODI2Nn0.SuwdRYjz6yjudrVAQpdj6JxZ8b1rr9hJUjBcJeAM-uY'

DATABASE_PATH = '\\alarmsystem\\resources\\face_database'
DETECT_SPOOF = True
MODEL = ''
DETECTOR = ''

def start_system() -> None:
    global os_type
    global os_is_raspi
    global system_dir

    system_dir = sm.get_dir(os_type)

    os_type = sm.get_os_type()
    os_is_raspi = True if os_type == ' raspi' else False

    if os_is_raspi:
       sm.attach_sleeper()

    fbr.connect_to_db(firebase_url, firebase_credentials)
    fbr.fetch_face_db()

def deactivate_system() -> None:
    sm.unset_oneddn()
    sm.dettach_sleeper()
    pass

def activate_intruder_mechanism() -> None:
    at.activate_alarm()
    fbr.notify_app()    

def check_door() -> None:
    img = rcg.capture_at_door()
    if not rcg.find_match(img):
        activate_intruder_mechanism()

def main():
    start_system()
    print(os_type)

if __name__ == '__main__':
    main()
