#define LED_PIN 11
#define SENSOR A5
#define BAUDRATE 9600
int brightness = 0;
float light = 0.0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(SENSOR, INPUT);
  Serial.begin(BAUDRATE);
}

void loop() {
    light = analogRead(SENSOR);
    light = map(light, 0, 1023, 255, 0);

    /* Serial.print("light [%]: "); */
    Serial.println(light / 255 * 100);

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