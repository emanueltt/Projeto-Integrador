#define LED_PIN 11
#define BAUDRATE 9600
int brightness = 0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(BAUDRATE);
}

void loop() {
    if(Serial.available() > 0) {
        brightness = Serial.parseInt();
        Serial.println(brightness);

        brightness = constrain(brightness, 0, 255);

        if(brightness != 0) analogWrite(LED_PIN, brightness);

        delay(500);
    }
}