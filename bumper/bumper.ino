#define BAUD_RATE 115200
#define TIMEOUT_MS 20

#include "HX711.h"
#define DAT_PIN_1 2 //D2
#define CLK_PIN_1 3 //D3
#define DAT_PIN_2 4 //D4
#define CLK_PIN_2 5 //D5
#define SCALE 100.0
#define CALIBRATION_INTERVAL 10
#define SAMPLING_INTERVAL 1

HX711 loadcell_1;
HX711 loadcell_2;

const size_t mem_size = CALIBRATION_INTERVAL;
double mem_1[mem_size];
double mem_2[mem_size];

bool filled = false;
int pos = 0;


double mean(double mem[]) {
	double res = 0;
	for (int i = 0; i < mem_size; i++) {
		res = res + mem[i];
	}
	return res / mem_size;
}


void setup() {
	Serial.begin(BAUD_RATE);
	loadcell_1.begin(DAT_PIN_1, CLK_PIN_1);
	loadcell_2.begin(DAT_PIN_2, CLK_PIN_2);
	while (!loadcell_1.is_ready() || !loadcell_2.is_ready()) {
		delay(TIMEOUT_MS);
	}
	loadcell_1.set_scale(SCALE);
	loadcell_2.set_scale(SCALE);
	loadcell_1.tare(CALIBRATION_INTERVAL);
	loadcell_2.tare(CALIBRATION_INTERVAL);
}

void loop() {

	if (loadcell_1.wait_ready_timeout(TIMEOUT_MS) &&
			loadcell_2.wait_ready_timeout(TIMEOUT_MS)) {

		mem_1[pos] = loadcell_1.get_units(SAMPLING_INTERVAL);
		mem_2[pos] = loadcell_2.get_units(SAMPLING_INTERVAL);

		if (filled) {
			Serial.print((long)(mem_1[pos] - mean(mem_1)));
			Serial.print(",");
			Serial.print((long)(mem_2[pos] - mean(mem_2)));
			Serial.println("");
		}

		if (++pos >= mem_size) {
			filled = true;
			pos = 0;
		}

	}

	delay(TIMEOUT_MS);
}
