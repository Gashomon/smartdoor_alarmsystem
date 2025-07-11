import os
import platform

# import RPi.GPIO as GPIO # not used because easier to apply gpiozero
from gpiozero import LED as digiOutPin
from gpiozero import Button as digiInPin
from time import sleep

PIWAKEPIN = 8 # MUST BE GPIO3
ALARMONPIN = 4
ALARMOFFPIN = 5
ARDUINOOFFPIN =  7
POWERPIN = 1

doorTouch = None
alarmOn = None
alarmOff = None
arduinoOff = None
piPower = None

# System Stuff
def get_os_type() -> str:
    if platform.system() == 'Windows':
        return 'windows'
    else:
        if "arm" in platform.machine().lower():
            return 'raspi'
        else:
            return 'linux'

def get_dir() -> str:
    return os.getcwd()

def set_oneddn() -> None:
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = 0

def unset_oneddn() -> None:
    del os.environ['TF_ENABLE_ONEDNN_OPTS']

def sleep_pi() -> None:
    sleep_arduino()
    os.system('sudo halt')
    pass

def check_net() -> bool:
    # irrelevant stuff if needed to catch no internet issues
    pass


# GPIO stuff
def set_pins() -> None:
    # set gpio to listen and sleep / wake
    global doorTouch
    global alarmOn
    global alarmOff
    global arduinoOff
    global piPower

    doorTouch = digiInPin(PIWAKEPIN)
    alarmOn = digiOutPin(ALARMONPIN)
    alarmOff = digiOutPin(ALARMOFFPIN)
    arduinoOff = digiOutPin(ARDUINOOFFPIN)
    piPower = digiInPin(POWERPIN)
    pass

def close_pins() -> None:
    # remove gpio
    global doorTouch
    global alarmOn
    global alarmOff
    global arduinoOff
    global piPower

    doorTouch.close()
    alarmOn.close()
    alarmOff .close()
    arduinoOff.close()
    piPower .close()

def activate_alarm() -> None:
    global alarmOn
    alarmOn.blink(n=1)

def deact_alarm() -> None:
    global alarmOff
    alarmOff.blink(n=1)

def sleep_arduino() -> None:
    global arduinoOff

    deact_alarm()
    arduinoOff.blink(n=1)

def got_touched() -> bool:
    global doorTouch
    if doorTouch.isPressed:
        return True
    else:
        return False
    
def pi_power_off() -> None:
    global piPower
    if piPower.isPressed:
        close_pins()
        unset_oneddn()
        os.system('sudo shutdown')