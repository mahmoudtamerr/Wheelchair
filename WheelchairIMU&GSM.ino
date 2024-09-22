#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
float gyroThreshold = .3;
int currentSpeed = 0;
int st =0;
// MPU6050 object
Adafruit_MPU6050 mpu;
// Function prototypes
void testATCommand();
void sendSMS(const char *number, const char *message);
SoftwareSerial GSM(7, 8);  // RX, TX for GSM module
void setup() {
  Serial.begin(19200);  // Communication with Serial Monitor
  while (!Serial) delay(10); // Wait for Serial console to open
  // Initialize the MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  GSM.begin(19200);     // Communication with GSM module
  // Give some time for GSM to initialize
  delay(1000);
  // Test AT command to check GSM response
  testATCommand();
  // Send SMS  // Replace with your phone number and message
}
void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  if (GSM.available()) {
    String response = GSM.readString();  // Read the response from GSM
    Serial.println("GSM Response: " + response);
  }
  /*// Continuously check for input from Serial Monitor to send to GSM
  if (Serial.available()) {
    String command = Serial.readString();
    GSM.println(command);  // Send the command from Serial Monitor to GSM
  }
  */
  if (abs(g.gyro.x) > gyroThreshold || abs(g.gyro.y) > gyroThreshold & st == 1) {
    Serial.println("Warning: Chair is turning or turned over!");
    sendSMS("+201156033966", "warnning");
    st=0;
    delay(100); 
  }
  else if (st == 0){
    Serial.println("the chair is stable ");
    st =1;
    delay(3000);
  }
}
void testATCommand() {
    // Send AT command
  
  delay(1000);  // Wait for response
    Serial.println("Sending AT command to GSM...");
    GSM.println("AT");
    delay(100);
    if (GSM.available()) {
      String response = GSM.readString();
      Serial.println("GSM Response: " + response);
    } else {
      Serial.println("No response from GSM module.");
    }
}
void sendSMS(const char *number, const char *message) {
  Serial.print("Sending SMS to ");
  Serial.println(number);
  GSM.println("AT+CMGF=1");  // Set SMS mode to text
  delay(1000);
  GSM.print("AT+CMGS=\"");
  GSM.print(number);
  GSM.println("\"");  // Specify recipient number
  delay(1000);
  GSM.println(message);  // Send the SMS message
  delay(1000);
  GSM.write(26);  // ASCII code for CTRL+Z to send SMS
  delay(2000);
  Serial.println("SMS sent.");
}