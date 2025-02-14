#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(9600);

  while (!Serial)
    ;

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1)
      ;
  }
}

void loop() {

  if (IMU.temperatureAvailable()) {
    float temperature_deg = 0;
    IMU.readTemperature(temperature_deg);

    unsigned long milliseconds = millis();
    unsigned long seconds = milliseconds / 1000;  // Convert to seconds

    Serial.print(seconds);
    Serial.print(",");
    Serial.println(temperature_deg);
  }

  delay(1000);
}
