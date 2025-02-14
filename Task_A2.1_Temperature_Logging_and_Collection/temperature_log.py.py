import serial
import time
import pandas as pd
import matplotlib.pyplot as plt

arduino_port = "COM3"
baud_rate = 9600

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=5)
    print(f"Connected to Arduino at {arduino_port}")
except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# Collect the data in a CSV file and submit it with the rest of your results
csv_file = "temperature_logging.csv"

try:
    data = []
    readings_collected = 0
    target_readings = 900

    while readings_collected < target_readings:
        line = ser.readline().decode('utf-8').rstrip()
        if line:
            try:
                Timesteps, temperature = line.split(",")
                data.append([int(Timesteps), float(temperature)])
                readings_collected += 1
                print(f"Reading {readings_collected}/{target_readings}, Timesteps: {Timesteps}, Temperature: {temperature}")
            except ValueError:
                print(f"Invalid data format: {line}")
        time.sleep(0.1)  # delay

    df = pd.DataFrame(data, columns=['Timesteps (ms)', 'Temperature (°C)'])
    df.to_csv(csv_file, index=False)
    print(f"Data saved to {csv_file}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if ser:
        ser.close()

        # Visualize the data with a line graph with two axes: time & temperature with criteria below
df['Time (s)'] = df['Timesteps (ms)']

plt.figure(figsize =(10, 6))
plt.plot(df['Time (s)'], df['Temperature (°C)'], color='orange', label='Temperature')
plt.xlabel('Time (seconds)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature over Time')
plt.grid(True)
plt.legend(loc='upper right')
plt.show()
