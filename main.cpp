#include <Arduino.h>
#include <Servo.h>

Servo myServo;

void setup() {
  pinMode(2, OUTPUT);
  Serial.begin(9600);
  pinMode(12, OUTPUT);
}

void loop() {

  if(Serial.available() > 0){
    String value = Serial.readStringUntil('\n');
    value.trim();
    
    if(value == "ZERO"){
      digitalWrite(12, HIGH);
    }else if(value == "UM"){
      digitalWrite(12, LOW);
    }
  }

}