import numpy as np

def simulate_heater(P_heater_series, dt,
                    C_p, U, alpha, T_amb, tau,
                    T0=None, Ts0=None):
    """
    Simulates temperature dynamics given a series of heater powers.
    
    P_heater_series: numpy array of heater power values over time steps.
    dt: time step (сек).
    C_p: тепловая ёмкость.
    U: коэффициент теплопотерь.
    alpha: преобразователь мощности.
    T_amb: температура окружающей среды.
    tau: постоянная времени задержки.
    T0: начальная температура «комнаты». По умолчанию ambient.
    Ts0: начальная температура датчика. По умолчанию ambient.
    """
    n = len(P_heater_series)
    T = np.zeros(n)
    Ts = np.zeros(n)
    
    T[0] = T0 if T0 is not None else T_amb
    Ts[0] = Ts0 if Ts0 is not None else T_amb
    
    for i in range(1, n):
        P = P_heater_series[i-1]
        dT = ( -U * (T[i-1] - T_amb) + alpha * P ) / C_p
        T[i] = T[i-1] + dT * dt
        
        dTs = (T[i-1] - Ts[i-1]) / tau
        Ts[i] = Ts[i-1] + dTs * dt
    
    return T, Ts

# Пример использования:
if __name__ == "__main__":
    dt = 1.0  # 1 секунда
    time_steps = 600  # симуляция на 10 минут
    P_series = np.zeros(time_steps)
    P_series[10:310] = 1.0  # нагреватель включен на единицу мощности между 10 и 310 секундами

    # Параметры модели:
    C_p = 100.0      # условная тепловая ёмкость
    U = 0.01          # коэффициент теплоотдачи
    alpha = 20.0     # эффективность нагрева
    T_amb = 20.0     # температура окружающей среды
    tau = 150.0        # задержка передачи тепла

    T, Ts = simulate_heater(P_series, dt, C_p, U, alpha, T_amb, tau)

    # Можно визуализировать поведение:
    import matplotlib.pyplot as plt
    plt.plot(T, label="Комната (T)")
    plt.plot(Ts, label="Датчик (Ts)")
    plt.plot(P_series * 100 + T_amb, label="Мощность нагрева (P × 100)") 
    plt.legend()
    plt.xlabel("Шаг времени (сек)")
    plt.ylabel("Температура / условная шкала")
    plt.show()
