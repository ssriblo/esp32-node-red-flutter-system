# Real-time data plotting from ESP32 via serial using matplotlib
# This version has NOT issues with performance and overheating on some PCs


import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from time import perf_counter
import numpy as np

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE   = 115200
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
except serial.SerialException as e:
    print(f"Error opening serial port {SERIAL_PORT}: {e}")
    exit(1)

MAX_POINTS = 200
tbuf = deque(maxlen=MAX_POINTS)
ybufs = [deque(maxlen=MAX_POINTS) for _ in range(5)]

y5_min, y5_max = 1000, 0  

fig, ax = plt.subplots()
lines = [ax.plot([], [], label=lbl, clip_on=True)[0]
         for lbl in ('P','dT','T','dTs','Ts')]

ax.set_xlabel('Time, s')
ax.set_ylabel('Value')
ax.set_title('Real-time ESP32 Data')
ax.legend()

# Remove scientific notation and offset at Y
ax.ticklabel_format(axis='y', useOffset=False, style='plain')

t0 = perf_counter()

def init():
    ax.set_xlim(0, 1)     # (will be updated)
    ax.set_ylim(-1, 1)     # (will be updated)
    for ln in lines:
        ln.set_data([], [])
    return lines

def update(_frame):
    global y5_min, y5_max

    if ser.in_waiting:
        raw = ser.readline().decode('utf-8', errors='ignore').strip()
        parts = raw.split()
        if len(parts) >= 5:
            try:
                vals = list(map(float, parts[:5]))
                print(f"Received values: {vals}", vals[4])

                t = perf_counter() - t0

                y5 = vals[4]
                if (y5 < y5_min):
                    y5_min = y5
                if (y5 > y5_max):
                    y5_max = y5
                # print(f"New Ts range: {y5_min} .. {y5_max} y5_max - y5_min = {y5_max - y5_min}")
                # print(f"[seconds:{t:.0f}] New Ts range:[{y5_min:.1f} .. {y5_max:.1f}] (Ts_max - Ts_min) = {(y5_max - y5_min):.1f}")

                tbuf.append(t)
                for b, v in zip(ybufs, vals):
                    b.append(v)

                # Line data update
                t_arr = np.fromiter(tbuf, dtype=float)
                for ln, b in zip(lines, ybufs):
                    ln.set_data(t_arr, np.fromiter(b, dtype=float))

                # Х - from 0 to current time
                ax.set_xlim(0, t)

                # Y - auto scale with margin
                all_y = np.concatenate([np.fromiter(b, dtype=float) for b in ybufs]) if len(tbuf) else np.array([0.0])
                y_min = np.min(all_y)
                y_max = np.max(all_y)
                if np.isfinite(y_min) and np.isfinite(y_max):
                    span = y_max - y_min
                    margin = 0.1 * span if span > 0 else 1.0
                    ax.set_ylim(y_min - margin, y_max + margin)

            except ValueError:
                pass

    return lines

ani = animation.FuncAnimation(
    fig, update, init_func=init, interval=100, blit=False
)

plt.show()
