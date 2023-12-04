#include "dcmotor.h"
#include "load_cell.h"


void running_loop()
{
    // Setup motor
    DCMotor motor;
    motor.pinout(5, 6);
    motor.forward();
    
    LoadCell loadCell;
    
    // Envio leitura
    while (true)
    {
        // Lê sensor e envia valor
        Serial.println(loadCell.read(5), 1);
        delay(50);
        
        // Lê comando do pc
        if (Serial.available() > 0)
        {
            char command = Serial.read();
            if (command == 'P')
            {
                motor.stop();
                delay(200);

                motor.backward();
                delay(1000);

                motor.stop();
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
    Serial.setTimeout(10);
    connection_loop();
}

void loop()
{
    idle_loop();
    running_loop();
}
