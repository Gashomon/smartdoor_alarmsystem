import sys_manager as sm
import recognizer as rcg
import firebaser as fbr

import time

os_type = 'unknown'
os_is_raspi = False
system_dir = ''

CRED_PATH = './alarmsystem/resources/passes.json'
DATABASE_PATH = './alarmsystem/resources/face_database'
DETECT_SPOOF = True
MODEL = ''
DETECTOR = ''

DEFAULT_IMG_PATH = DATABASE_PATH + '/latest.jpg'

system_timer = 0

# called only at start
def start_system() -> None:
    " DocString: call to initialize variables of system "
    global os_type
    global os_is_raspi
    global system_dir
    
    system_dir = sm.get_dir()

    os_type = sm.get_os_type()
    os_is_raspi = True if os_type == ' raspi' else False

    # initiate db
    fbr.connect_to_dbs(CRED_PATH)
    fbr.fetch_face_db()

    if os_is_raspi:
        print("actual system running...")
        # auto sleep
        sm.set_oneddn()

        # system start
        sm.set_pins()
        sm.sleep_pi()

# called only at end
def deactivate_system() -> None:
    " DocString: call to gracefully shutdown system "
    if os_is_raspi:
        sm.pi_power_off()

# main system loops
def check_door() -> None:
    if os_is_raspi:
        img = rcg.capture_at_door()
        if not rcg.find_match(img):
            sm.activate_alarm()
            fbr.upload_entry(img)

def wait_for_people(timeout: int = 10, timeskip: int = 2) -> bool:
    global system_timer
    # check some time if there is face
    # person_detected = rcg.find_face()
    person_detected = True
    # if face found run codes, dont allow power off if running other stuff
    if person_detected:
        check_door()
        # after successful run, return True to reset the loop. Reset timer if ever
        return True
    else:
        # if button pressed shutdown
        manual_off = sm.pi_power_off()
        if manual_off:
            return False 
        
        # counter increment if timeout reached, sleep pi. Run continuosly until then
        system_timer += timeskip
        if system_timer >= timeout:
            system_timer = 0
            sm.sleep_pi()
            return True
        time.sleep(timeskip)

def main():
    start_system()
    # system_continue = True
    # while system_continue:
    #     system_continue = wait_for_people()
    fbr.upload_entry("D:/MON Stuff/Work Stuff/SmartDoor/smartdoor_alarmsystem/alarmsystem/resources/captures/3.jpg")
    deactivate_system()

if __name__ == '__main__':
    main()