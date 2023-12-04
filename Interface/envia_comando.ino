#include "HX711.h"

#define LED_PIN 11
#define LOADCELL_SCK_PIN A0
#define LOADCELL_DOUT_PIN A1
#define SENSOR A5
#define BAUDRATE 9600
int brightness = 0;
float light = 0.0;
const long LOADCELL_OFFSET = 50682624;
const long LOADCELL_DIVIDER = 5895655;

HX711 loadcell;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(SENSOR, INPUT);
  loadcell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  Serial.begin(BAUDRATE);
  // Serial.print("Tara: ");
  // Serial.println(loadcell.read());
  // Serial.println("Initializing load cell...");
  // loadcell.set_scale();
  // loadcell.tare(20);
  // loadcell.set_scale(LOADCELL_DIVIDER);
  // loadcell.set_offset(LOADCELL_OFFSET);
}

void loop() {
  light = analogRead(SENSOR);
  light = map(light, 0, 1023, 255, 0);
  Serial.println(light / 255 * 100);

  // Serial.print("Weight: ");
  // Serial.println(loadcell.get_value(10),0);

  // if(light > 200) analogWrite(LED_PIN, HIGH);
  // else analogWrite(LED_PIN, LOW);

  // if(Serial.available() > 0) {
  //     brightness = Serial.parseInt();
  //     Serial.println(brightness);

  //     brightness = constrain(brightness, 0, 255);

  //     if(brightness != 0) analogWrite(LED_PIN, brightness);

  //     delay(500);
  // }

  delay(1000);
}