#ifndef LOAD_CELL_H
#define LOAD_CELL_H

#include "HX711.h"

class LoadCell
{
    const int LOADCELL_DOUT_PIN = 12;
    const int LOADCELL_SCK_PIN = 11;

    float mScale = -103.595;
    HX711 loadCellSensor;

public:
    LoadCell();
    long read(int sampleQuantity);
    void set_scale(float scale);
    void tare();
};

#endif