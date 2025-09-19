# Real-time data plotting from ESP32 via serial using matplotlib
# This version has issues with performance and overheating on some PCs

import serial
import matplotlib.pyplot as plt
from collections import deque
import time

# Serial port configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Replace with your ESP32's serial port (e.g., '/dev/ttyUSB0' on Linux)
BAUD_RATE = 115200

# Plotting parameters
MAX_POINTS = 200  # Number of data points to display on the plot
x_data = deque(maxlen=MAX_POINTS)
y1_data = deque(maxlen=MAX_POINTS)
y2_data = deque(maxlen=MAX_POINTS) # For the second data series
y3_data = deque(maxlen=MAX_POINTS)
y4_data = deque(maxlen=MAX_POINTS)
y5_data = deque(maxlen=MAX_POINTS)

# Setup the plot
fig, ax = plt.subplots()

    # Serial.printf("%2.1f %2.1f %2.1f %2.1f\n", P_heater,dT, m->T, dTs, m->Ts);
line1, = ax.plot(x_data, y1_data, label='P')
line2, = ax.plot(x_data, y2_data, label='dT') 
line3, = ax.plot(x_data, y3_data, label='T') 
line4, = ax.plot(x_data, y4_data, label='dTs') 
line5, = ax.plot(x_data, y5_data, label='Ts') 

ax.set_xlabel('Time')
ax.set_ylabel('Values')
ax.set_title('Real-time ESP32 Data')
ax.legend()
plt.ion() # Turn on interactive mode for live plotting

try:
    # ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

    start_time = time.time()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            try:
                # Parse the comma-separated values
                values = [float(val) for val in line.split(' ')]

                print(f"Received values: {values}")

                if len(values) == 5: 
                    sensor1_val, sensor2_val, sensor3_val, sensor4_val, sensor5_val = values

                    current_time = time.time() - start_time
                    x_data.append(current_time)
                    y1_data.append(sensor1_val)
                    y2_data.append(sensor2_val)
                    y3_data.append(sensor3_val)
                    y4_data.append(sensor4_val)
                    y5_data.append(sensor5_val)

                    # Update plot data
                    line1.set_data(x_data, y1_data)
                    line2.set_data(x_data, y2_data)
                    line3.set_data(x_data, y3_data)
                    line4.set_data(x_data, y4_data)
                    line5.set_data(x_data, y5_data)

                    # Adjust plot limits dynamically
                    ax.set_xlim(x_data[0], x_data[-1] if len(x_data) > 1 else x_data[0] + 1)
                    ax.set_ylim(min(min(y1_data), min(y2_data), min(y3_data), min(y4_data), min(y5_data)) * 0.9, max(max(y1_data), max(y2_data), max(y3_data), max(y4_data), max(y5_data)) * 1.1)

                    fig.canvas.draw_idle()
                    fig.canvas.flush_events()

                    plt.show()
                    
                    time.sleep(0.5) # very helpful to avoid PC overheat !!

            except ValueError:
                print(f"Could not parse line: {line}")
            except IndexError:
                print(f"Incomplete data received: {line}")

except serial.SerialException as e:
    print(f"Serial port error: {e}")
except KeyboardInterrupt:
    print("Plotting stopped by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
    plt.ioff()
    plt.show() # Keep the plot window open after stopping interactive mode