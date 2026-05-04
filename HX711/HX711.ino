#include "HX711.h"

#define BAUD_RATE 115200
#define LOADCELL_DT_PIN 2
#define LOADCELL_SCK_PIN 3
#define CHANNEL_A 128
#define CHANNEL_B 32
#define SAMPLING_INTERVAL_CALIBRATION 100
#define SAMPLING_INTERVAL 5
#define TIMEOUT_MS 10

HX711 loadcell;

// long offset_a = 0;
// long offset_b = 0;
// long reading_a = 0;
// long reading_b = 0;
// bool channel_a = true;
long offset = 0;
long reading = 0;

void setup() {
	Serial.begin(BAUD_RATE);
	loadcell.begin(LOADCELL_DT_PIN, LOADCELL_SCK_PIN);
	// loadcell.set_gain(CHANNEL_B);
	// offset_b = loadcell.get_units(SAMPLING_INTERVAL_CALIBRATION);
	// loadcell.set_gain(CHANNEL_A);
	// offset_a = loadcell.get_units(SAMPLING_INTERVAL_CALIBRATION);
	loadcell.set_gain(CHANNEL_A);
	offset = loadcell.get_units(SAMPLING_INTERVAL_CALIBRATION);
}

void loop() {
	if (loadcell.wait_ready_timeout(TIMEOUT_MS)) {
		// if (channel_a) {
		// 	channel_a = false;
		// 	loadcell.set_gain(CHANNEL_A);
		// 	reading_a = (long)loadcell.get_units(SAMPLING_INTERVAL) - offset_a;

		// } else {
		// 	channel_a = true;
		// 	loadcell.set_gain(CHANNEL_B);
		// 	reading_b = (long)loadcell.get_units(SAMPLING_INTERVAL) - offset_b;

		// }
		// Serial.print(reading_a);
		// Serial.print(',');
		// Serial.println(reading_b);
		reading = (long)loadcell.get_units(SAMPLING_INTERVAL) - offset;
		Serial.println(reading);
	}
}
