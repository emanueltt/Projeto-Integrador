bool handshakeComplete = false;
bool acknowledged = false;
float sensorValue = 123.45;  // Replace with your actual sensor reading

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (!handshakeComplete) {
    // Perform the handshake
    if (Serial.available() > 0) {
      char command = Serial.read();
      if (command == 'H') {
        // Received handshake request from Python
        Serial.println("A"); // Send acknowledgment back to Python
        handshakeComplete = true; // Handshake is complete
        acknowledged = true;
      }
    }
  } else {
    if (acknowledged == true) {
      acknowledged = false;
      // Send sensor data
      Serial.println(sensorValue, 2);
      delay(1000); // Adjust delay as needed
    }
    if (Serial.available() > 0) {
      char command = Serial.read();
      if (command == 'A') {
        acknowledged = true;
      }
    }
  }
}
