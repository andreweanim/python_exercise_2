#include <Arduino_LSM6DSOX.h>

float Ax, Ay, Az;
float Gx, Gy, Gz;

// Start date and time
String startDate = "2024-10-27";
String startTime = "14:00:00";
unsigned long startTimeMillis;

const int sampleRate = 500;   // 2Hz (1000ms/2 = 500ms)
const int duration = 600000;  // 10 minutes in milliseconds

void setup() {
  Serial.begin(9600);

  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1)
      ;
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println("Hz");
  Serial.println();

  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println("Hz");
  Serial.println();

  // header
  Serial.println("Date,Time,Ax,Ay,Az,Gx,Gy,Gz");

  startTimeMillis = millis();  // Record the start time
}

void loop() {
  if (millis() - startTimeMillis < duration) {
    if (millis() % sampleRate == 0) {

      unsigned long elapsedTime = millis() - startTimeMillis;
      int seconds = elapsedTime / 1000;
      int minutes = seconds / 60;
      int hours = minutes / 60;

      seconds %= 60;
      minutes %= 60;

      String currentTime = String(hours) + ":" + String(minutes) + ":" + String(seconds);

      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(Ax, Ay, Az);
        Serial.print(startDate);
        Serial.print(",");
        Serial.print(currentTime);
        Serial.print(",");
        Serial.print(Ax);
        Serial.print(",");
        Serial.print(Ay);
        Serial.print(",");
        Serial.print(Az);
        Serial.print(",");
      }

      if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(Gx, Gy, Gz);

        Serial.print(Gx);
        Serial.print(",");
        Serial.print(Gy);
        Serial.print(",");
        Serial.println(Gz);
      }

      delay(10);
    }
  } else {
    Serial.println("Data collection complete!");
    while (1) {
      delay(10);
    }
  }
}