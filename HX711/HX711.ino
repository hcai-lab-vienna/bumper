#include "HX711.h"

#define BAUD_RATE 115200
#define DAT_PIN 2 //D2
#define CLK_PIN 3 //D3
#define SCALE 1000.0
#define SAMPLING_INTERVAL_CALIBRATION 100
#define SAMPLING_INTERVAL 2
#define TIMEOUT_MS 3

HX711 loadcell;

void setup() {
	Serial.begin(BAUD_RATE);
	Serial.println("");
	loadcell.begin(DAT_PIN, CLK_PIN);
	delay(100);
	while (!loadcell.is_ready()) {
		delay(100);
		Serial.println("HX711 NOT FOUND");
	}
	Serial.println("CALIBRATING...");
	loadcell.set_scale(SCALE);
	loadcell.tare(SAMPLING_INTERVAL_CALIBRATION);
}

void loop() {
	if (loadcell.wait_ready_timeout(TIMEOUT_MS)) { 
		long reading = loadcell.get_units(SAMPLING_INTERVAL);
		Serial.println(reading);
	}
}
