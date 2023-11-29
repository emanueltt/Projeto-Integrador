bool handshakeComplete = false;
bool acknowledged = false;
float sensorValue = 123.45; // Replace with your actual sensor reading

void connect()
{
    while (!handshakeComplete)
    {
        // Perform the handshake
        if (Serial.available() > 0)
        {
            char command = Serial.read();
            if (command == 'H')
            {
                // Received handshake request from Python
                Serial.println("A");      // Send acknowledgment back to Python
                handshakeComplete = true; // Handshake is complete
                acknowledged = true;
                break;
            }
        }
    }
}

void idle()
{
    while (true)
    {
        // Lê comando do pc
        if (Serial.available() > 0)
        {
            char command = Serial.read();
            if (command == 'S')
            {
                break;
            }
        }
    }
}

void working()
{
    // Setup motor

    // Envio leitura
    while (true)
    {
        // Lê sensor e envia valor
        Serial.println(sensorValue, 2);

        // Lê comando do pc
        if (Serial.available() > 0)
        {
            char command = Serial.read();
            if (command == 'P')
            {
                break;
            }
        }
    }
}

void setup()
{
    Serial.begin(9600);
    connect();
}

void loop()
{
    idle();
    working();
}
