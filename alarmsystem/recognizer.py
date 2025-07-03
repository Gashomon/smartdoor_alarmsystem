from deepface import DeepFace

def capture_at_door() -> str:
    # take pic
    # save pic
    # return pic path
    pass

def find_match(img1_path: str, db_folder: str, model: str = 'VGG-Face', detector: str = 'openCV', spoofing: bool = True) -> bool:
    if len(DeepFace.find(img1_path, db_folder,model_name=model, detector_backend=detector, anti_spoofing=spoofing)):
        # show how many matches and names
        return True
    else:
        # prompt unknown
        return False

    
    
    pass
