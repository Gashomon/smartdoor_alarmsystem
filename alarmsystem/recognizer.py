from deepface import DeepFace
import time
from picamera2 import Picamera2

camera = Picamera2

still_config = camera.create_still_configuration(

)
video_config = camera.create_video_configuration()

def capture_at_door(location: str = '.') -> str:
    # take pic
    camera.start_and_capture_file(location+'\\temp.jpg')

    # ensure person is in pic
    
    # return pic path
    return location+'\\temp.jpg'

def find_match(img1_path: str, db_folder: str, model: str = 'VGG-Face', detector: str = 'openCV', sure_detect: bool = False, spoofing: bool = True) -> bool:
    df_find = DeepFace.find(img1_path, db_folder,model_name=model, detector_backend=detector, enforce_detection=sure_detect, anti_spoofing=spoofing)[0]
    matches = len(df_find.index)

    has_match = True if matches > 0 else False
    return has_match

