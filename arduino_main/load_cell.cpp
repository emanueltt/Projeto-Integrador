#include "load_cell.h"

LoadCell::LoadCell(){
    /*
        How to calibrate loadcell:
        1. Call set_scale() with no parameter.
        2. Call tare() with no parameter.
        3. Place a known weight on the scale and call get_units(10).
        4. Divide the result in step 3 to your known weight. You should get about the parameter you need to pass to set_scale().
        5. Adjust the parameter in step 4 until you get an accurate reading.
    */
    loadCellSensor.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    loadCellSensor.set_scale(mScale);
}

long LoadCell::read(int sampleQuantity){
    loadCellSensor.power_up();
    long reading = loadCellSensor.get_units(sampleQuantity);
    loadCellSensor.power_down();
    return reading;
}

void LoadCell::set_scale(float scale){
    loadCellSensor.set_scale(scale);
}

void LoadCell::tare(){
    loadCellSensor.tare();
}