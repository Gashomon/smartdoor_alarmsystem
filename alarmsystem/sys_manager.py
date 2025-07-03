import os
import platform

# import RPi.GPIO as GPIO

def get_os_type() -> str:
    if platform.system() == 'Windows':
        return 'windows'
    else:
        if "arm" in platform.machine().lower():
            return 'raspi'
        else:
            return 'linux'

def get_dir() -> str:
    return os.getcwd

def attach_sleeper() -> None:
    # set gpio to listen and sleep / wake
    pass

def dettach_sleeper() -> None:
    # remove gpio
    pass

def set_oneddn() -> None:
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = 0

def unset_oneddn() -> None:
    del os.environ['TF_ENABLE_ONEDNN_OPTS']