#define USE_HX711
//#define USE_MPU6050
//#define PRINT_MPU_TEMPERATURE

#define BAUD_RATE 115200
#define TIMEOUT_MS 30

#ifdef USE_HX711
#include "HX711.h"
#define DAT_PIN 2 //D2
#define CLK_PIN 3 //D3
#define SCALE 500.0
#define SAMPLING_INTERVAL_CALIBRATION 100
#define SAMPLING_INTERVAL 2
HX711 loadcell;
#endif

#ifdef USE_MPU6050
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
Adafruit_MPU6050 mpu;
#endif

void setup() {
	Serial.begin(BAUD_RATE);
#ifdef USE_HX711
	loadcell.begin(DAT_PIN, CLK_PIN);
	while (!loadcell.is_ready()) delay(100);
	loadcell.set_scale(SCALE);
	loadcell.tare(SAMPLING_INTERVAL_CALIBRATION);
#endif
#ifdef USE_MPU6050
	while (!mpu.begin()) delay(100);
	mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
	mpu.setGyroRange(MPU6050_RANGE_500_DEG);
	mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
#endif
}

void loop() {
#ifdef USE_HX711
	if (loadcell.wait_ready_timeout(TIMEOUT_MS)) {
		long reading = loadcell.get_units(SAMPLING_INTERVAL);
		Serial.print(reading);
#ifdef USE_MPU6050
		Serial.print(",");
#endif
#endif
#ifdef USE_MPU6050
		sensors_event_t a, g, temp;
		mpu.getEvent(&a, &g, &temp);
		Serial.print(a.acceleration.x);Serial.print(",");
		Serial.print(a.acceleration.y);Serial.print(",");
		Serial.print(a.acceleration.z);Serial.print(",");
		Serial.print(g.gyro.x);Serial.print(",");
		Serial.print(g.gyro.y);Serial.print(",");
		Serial.print(g.gyro.z);
#ifdef PRINT_MPU_TEMPERATURE
		Serial.print(",");
		Serial.print(temp.temperature);
#endif
#endif
		Serial.println("");
#ifdef USE_HX711
	}
#else
	delay(TIMEOUT_MS);
#endif
}
