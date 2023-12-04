#include "dcmotor.h"
#include "Arduino.h"


void DCMotor::pinout(int in1, int in2)
{ // pinout é o método para a declaração dos pinos que vão controlar o objeto motor
    mPin1 = in1;
    mPin2 = in2;
    pinMode(mPin1, OUTPUT);
    pinMode(mPin2, OUTPUT);
}

void DCMotor::speed(int in1)
{ // speed é o método que irá ser responsável por salvar a velocidade de atuação do motor
    mSpeed = in1;
}

void DCMotor::forward()
{ // forward é o método para fazer o motor girar para frente
    analogWrite(mPin1, mSpeed);
    digitalWrite(mPin2, LOW);
}

void DCMotor::backward()
{ // backward é o método para fazer o motor girar para trás
    digitalWrite(mPin1, LOW);
    analogWrite(mPin2, mSpeed);
}

void DCMotor::stop()
{ // stop é o metodo para fazer o motor ficar parado.
    digitalWrite(mPin1, LOW);
    digitalWrite(mPin2, LOW);
}