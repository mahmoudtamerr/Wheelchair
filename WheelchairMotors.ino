#include <Wire.h>
#include <Math.h>

const int MPU_addr = 0x68; // I2C address of the MPU-6050
const float TILT_THRESHOLD = 30.0; // Tilt threshold in degrees

// Motor A connections
const int motorA1 = 2;
const int motorA2 = 3;
const int motorAspeed = 9; 

// Motor B connections
const int motorB1 = 4;
const int motorB2 = 5;
const int motorBspeed = 10; 

int currentSpeed = 0;

void setup() {
  pinMode(motorA1, OUTPUT);
  pinMode(motorA2, OUTPUT);
  pinMode(motorAspeed, OUTPUT);
  pinMode(motorB1, OUTPUT);
  pinMode(motorB2, OUTPUT);
  pinMode(motorBspeed, OUTPUT);
  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the command character

    if (command == 'f' || command == 'b' || command == 'l' || command == 'r') {
      int speed = Serial.parseInt(); // Read the speed value
      move(command);
    } else if (command == 's') {
      stopMotors();
    }
  }
  
  delay(1); // Delay for readability
}

void move(char direction) {
  switch (direction) {
    case 'f':
      moveForward();
      break;
    case 'b':
      moveBackward();
      break;
    case 'l':
      turnLeft();
      break;
    case 'r':
      turnRight();
      break;
  }
}

void moveForward() {
  analogWrite(motorAspeed, 150);
  analogWrite(motorBspeed, 150);
  digitalWrite(motorA1, HIGH);
  digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, HIGH);
  digitalWrite(motorB2, LOW);
}

void moveBackward() {
  analogWrite(motorAspeed, 150);
  analogWrite(motorBspeed, 150);
  digitalWrite(motorA1, LOW);
  digitalWrite(motorA2, HIGH);
  digitalWrite(motorB1, LOW);
  digitalWrite(motorB2, HIGH);
}

void turnLeft() {

  analogWrite(motorBspeed, 0); 
  analogWrite(motorAspeed, 100);
  digitalWrite(motorA1, HIGH);  // Left motor forwards
  digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, LOW);    // Right motor off
  digitalWrite(motorB2, LOW);
}

void turnRight() {
    analogWrite(motorAspeed, 0); 
  analogWrite(motorBspeed, 100);
  digitalWrite(motorA1, LOW);  // Left motor off
  digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, HIGH);  // Right motor forwards
  digitalWrite(motorB2, LOW);
}

void stopMotors() {
  digitalWrite(motorA1, LOW);
  digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, LOW);
  digitalWrite(motorB2, LOW);
  analogWrite(motorAspeed, 0);
  analogWrite(motorBspeed, 0);
}
