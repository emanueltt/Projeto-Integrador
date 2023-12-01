#ifndef DCMOTOR_H
#define DCMOTOR_H

class DCMotor
{
    int mSpeed = 255, mPin1, mPin2;

public:
    void Pinout(int in1, int in2);
    void Speed(int in1);
    void Forward();
    void Backward();
    void Stop();
};

#endif