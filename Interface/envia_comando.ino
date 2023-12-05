#define SENSOR A5
#define BAUDRATE 9600
float light = 0.0;

void setup() {
  pinMode(SENSOR, INPUT);
  Serial.begin(BAUDRATE);
}

void loop() {
  light = analogRead(SENSOR);
  light = map(light, 0, 1023, 255, 0);
  Serial.println(light / 255 * 100);
  delay(1000);
}