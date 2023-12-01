#include "dcmotor.h"


void running_loop()
{
    // Setup motor
    DCMotor motor;
    motor.Pinout(5, 6);
    motor.Forward();

    // Envio leitura
    float sensorValue = 123.45;
    while (true)
    {
        motor.Forward();
        // Lê sensor e envia valor
        Serial.println(sensorValue, 2);
        delay(50)
        
        // Lê comando do pc
        if (Serial.available() > 0)
        {
            char command = Serial.read();
            if (command == 'P')
            {
                motor.Stop();
                delay(200);

                motor.Backward();
                delay(1000);

                motor.Stop();
                break;
            }
        }
    }
}

void idle_loop()
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

void connection_loop()
{
    while (true)
    {
        // Perform the handshake
        if (Serial.available() > 0)
        {
            char command = Serial.read();
            if (command == 'H')
            {
                // Received handshake request from Python
                Serial.println("A");  // Send acknowledgment back to Python
                break;
            }
        }
    }
}

void setup()
{
    Serial.begin(9600);
    connection_loop();
}

void loop()
{
    idle_loop();
    running_loop();
}
