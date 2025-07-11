from deepface import DeepFace
import time
import os
from picamera2 import Picamera2

camera = Picamera2
currdir = os.getcwd()
still_config = camera.create_still_configuration()
# video_config = camera.create_video_configuration()

def capture_at_door(location: str = currdir+"\\resources") -> str:
    filename = location+'\\temp.jpg'
    # take pic
    camera.start_and_capture_file(filename)

    # return pic path
    return filename

def find_match(img1_path: str, db_folder: str = currdir+"\\resources\\face_database", model: str = 'VGG-Face', detector: str = 'openCV', sure_detect: bool = False, spoofing: bool = True) -> bool:
    has_match = None
    try:
        df_find = DeepFace.find(img1_path, db_folder,model_name=model, detector_backend=detector, enforce_detection=sure_detect, anti_spoofing=spoofing)[0]
        matches = len(df_find.index)

        has_match = True if matches > 0 else False
    except Exception as e:
        has_match = True
        
    return has_match

def find_face() -> bool:
    # check if faces still exist in front
    
    # return true if yes, otherwise false
    pass