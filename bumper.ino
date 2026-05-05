#include "HX711.h"
// #include <Adafruit_MPU6050.h>
// #include <Adafruit_Sensor.h>
// #include <Wire.h>

#define BAUD_RATE 115200
#define DAT_PIN 2 //D2
#define CLK_PIN 3 //D3
#define SCALE 500.0
#define SAMPLING_INTERVAL_CALIBRATION 100
#define SAMPLING_INTERVAL 2
#define TIMEOUT_MS 3

HX711 loadcell;
// Adafruit_MPU6050 mpu;

void setup() {
	Serial.begin(BAUD_RATE);
	loadcell.begin(DAT_PIN, CLK_PIN);
	while (!loadcell.is_ready()) delay(100);
	// while (!mpu.begin()) delay(100);
	// mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
	// mpu.setGyroRange(MPU6050_RANGE_500_DEG);
	// mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
	loadcell.set_scale(SCALE);
	loadcell.tare(SAMPLING_INTERVAL_CALIBRATION);
}

void loop() {
	if (loadcell.wait_ready_timeout(TIMEOUT_MS)) { 
		long reading = loadcell.get_units(SAMPLING_INTERVAL);
		// sensors_event_t a, g, temp;
		// mpu.getEvent(&a, &g, &temp);
		Serial.print(reading);//Serial.print(",");
		// Serial.print(a.acceleration.x);Serial.print(",");
		// Serial.print(a.acceleration.y);Serial.print(",");
		// Serial.print(a.acceleration.z);Serial.print(",");
		// Serial.print(g.gyro.x);Serial.print(",");
		// Serial.print(g.gyro.y);Serial.print(",");
		// Serial.print(g.gyro.z);//Serial.print(",");
		Serial.println("");//Serial.println(temp.temperature);
	}
}
