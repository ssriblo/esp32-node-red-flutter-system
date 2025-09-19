#include "tempFilter.h" 

// #define DEBUG_PRINT

void init_model(HeaterModel *m, float Cp, float U, float alpha,
                float Tamb, float tau, float dt, float T0, float Ts0) {
    m->Cp = Cp;
    m->U = U;
    m->alpha = alpha;
    m->Tamb = Tamb;
    m->tau = tau;
    m->dt = dt;
    m->T = T0;
    m->Ts = Ts0;
}

void step_model(HeaterModel *m, float P_heater) {


    float dT = ( -m->U * (m->T - m->Tamb) + m->alpha * P_heater ) / m->Cp;

    // Serial.printf("[step_model] %f %f\n",  -m->U * (m->T - m->Tamb),  m->alpha * P_heater );

    m->T += dT * m->dt;

    float dTs = (m->T - m->Ts) / m->tau;
    m->Ts += dTs * m->dt;

#ifdef DEBUG_PRINT    
    Serial.printf("\n[step_model-1] P_heater: %2.1f\n", P_heater);
    Serial.printf("[step_model-2] dT=%2.1f T=%2.1f dTs=%2.1f Ts=%2.1f\n\n", m->T, dTs, m->Ts);
#endif
    Serial.printf("%2.1f %f %f %f %f\n", P_heater, dT, m->T, dTs, m->Ts);

}

void heater_model_unit_test(void) {
    delay(1000);
    const int STEPS = 600;
    float dt = 1.0;
    HeaterModel model;
    init_model(&model,
               100.0,   // Cp
               0.01,     // U
               20.0,    // alpha
               20.0,    // Tamb
               150.0,     // tau
               dt,
               20.0,    // initail room temperature
               20.0);   // initial sensor temperature

    // float *P = malloc(sizeof(float) * STEPS);
    // float *T = malloc(sizeof(float) * STEPS);
    // float *Ts = malloc(sizeof(float) * STEPS);
    float *P = static_cast<float*>(malloc(sizeof(float) * STEPS));
    float *T = static_cast<float*>(malloc(sizeof(float) * STEPS));
    float *Ts = static_cast<float*>(malloc(sizeof(float) * STEPS));

    if (!P || !T || !Ts) {
        fprintf(stderr, "maloc error\n");
        // return 1;
    }
    for (int i = 0; i < STEPS; i++) {
        P[i] = (i >= 10 && i < 310) ? 1.0 : 0.0;
    }

    for (int i = 0; i < STEPS; i++) {
        P[i] = P[i];
        T[i] = model.T;
        Ts[i] = model.Ts;
        step_model(&model, P[i]);
    }

    printf("step,heater_power,T_room,T_sensor\n");
    for (int i = 0; i < STEPS; i++) {
        printf("%d,%.3f,%.3f,%.3f\n", i, P[i], T[i], Ts[i]);
    }

    free(P);
    free(T);
    free(Ts);
}
