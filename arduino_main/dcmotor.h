#ifndef DCMOTOR_H
#define DCMOTOR_H

class DCMotor
{
    int mSpeed = 255, mPin1, mPin2;

public:
    void pinout(int in1, int in2);
    void speed(int in1);
    void forward();
    void backward();
    void stop();
};

#endif