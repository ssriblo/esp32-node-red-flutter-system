#ifndef TEMP_FILTER_H
#define TEMP_FILTER_H


#include <stdio.h>
#include <stdlib.h>
#include <Arduino.h>

typedef struct {
    float Cp;      // heat capacity
    float U;       // heat loss coefficient
    float alpha;   // conversion of power to heat energy
    float Tamb;    // ambient temperature
    float tau;     // delay time constant (sensor)
    float dt;      // integration step
    float T;       // “room” temperature
    float Ts;      // measured temperature (sensor)
} HeaterModel;

void init_model(HeaterModel *m, float Cp, float U, float alpha,
                float Tamb, float tau, float dt, float T0, float Ts0);

void step_model(HeaterModel *m, float P_heater);

void heater_model_unit_test(void);


#endif // TEMP_FILTER_H