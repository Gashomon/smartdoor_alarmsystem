/*
  Use Analog Pin to receive sleep mode or trigger alarm
  Use wakePin to send wake up signal to raspi, if needed, request Serial to run detection script
  Activate buzzer at highest volume, with different intervals. While face is detected, keep on buzzing (consider distance if needed)
*/
#include "LowPower.h"

const int buzzerPin = 6;      // speaker (PWM pins D3, D5, D6, D9, D10, D11)
const int sensorPin = 3;      // force sensor (D2 or D3) 
const int wakePin = 8;        // raspi hardware force wake pin (Digital pins D2 to D12)
const int alrmOnPin = 4;      // raspi alarm on pin (Digital pins)
const int alrmOffPin = 5;     // raspi alarm off pin (Digital pins)
const int sleepPin =  7;      // raspi trigger sleep arduino (Digital pins)

// above this is considered activated if sensor is in analog
// const int sensor_threshold = 100;

// cmd Pin outputs if sensor is in analog
// const int cmd_max = 255;
// const int cmd_min = 0;

// cmd variables
bool alarm_on = false;
bool sleep_on = false;

// alarm variables
int sound_steps[] = {1000, 500, 1000, 500, 1000, 1000, 500, 1000, 500, 100, 500, 100, 500, 100, 500, 100, 500, 100, 500, 100, 500, 1000};
int sounds_len = sizeof(sound_steps) /sizeof(sound_steps[0]);
int sound_curr = 0;
int sound_out = HIGH;
int sound_timer = millis();
int sound_time_maxout = 3000; // should be greater than any value in sound_steps

void setup() {
  pinMode(buzzerPin, OUTPUT);
  pinMode(sensorPin, INPUT);
  pinMode(wakePin, OUTPUT);  
  pinMode(alrmOnPin, INPUT);
  pinMode(alrmOffPin, INPUT);
  pinMode(sleepPin, INPUT);
  
  attachInterrupt(digitalPinToInterrupt(sensorPin), wakePi, RISING);
  alarm_on = false;
  sleep_on = false;

  resetAlarm();

  // auto sleep at startup
  // setupSleep();
}

void loop() {
  if(digitalRead(alrmOnPin) == HIGH){
    alarm_on = true;
  }
  else if(digitalRead(alrmOffPin) == HIGH){
    alarm_on = false;
  }
  else if(digitalRead(sleepPin) == HIGH){
    setupSleep();
  }

  if (alarm_on){
    runAlarm();
  }
}

void setupSleep(){
  // sounds
  analogWrite(buzzerPin, 150);
  delay(250);
  analogWrite(buzzerPin, 100);
  delay(250);
  analogWrite(buzzerPin, 0);

  // main func
  sleep_on = true;
  LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF); 
}

void wakePi(){
  if (sleep_on){
    // sounds
    analogWrite(buzzerPin, 100);
    delay(250);
    analogWrite(buzzerPin, 150);
    delay(250);
    analogWrite(buzzerPin, 0);

    // main func
    digitalWrite(wakePin, HIGH);
    resetAlarm();
    sleep_on = false;
  }
}

void runAlarm(){
  if (sound_curr >= sounds_len-1 || millis() - sound_timer >= sound_time_maxout){
    resetAlarm();
  }

  if (millis() - sound_timer >= sound_steps[sound_curr]){
    digitalWrite(buzzerPin, sound_out);
    sound_out = !sound_out;
    sound_timer = millis();
    sound_curr++;
  }
}

void resetAlarm(){
  sound_curr = 0;
  sound_timer = millis();
  sound_out = HIGH;
}