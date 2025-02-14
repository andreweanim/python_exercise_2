import serial
import time
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# I- Collect the data in a CSV file and submit it with the rest of your results

arduino_port = "COM3"  
baud_rate = 9600
csv_file = "motion_logging.csv"
num_readings = 1350

ser = None

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=5)
    print(f"Connected to Arduino at {arduino_port}")

    # Open the file to save the data
    with open(csv_file, "w") as file:
        file.write("Date,Time,Ax,Ay,Az,Gx,Gy,Gz\n")

        readings_count = 0
        while readings_count < num_readings:
            line = ser.readline().decode('utf-8').rstrip()
            if line:
                try:
                    file.write(line + "\n")
                    readings_count += 1
                    print(f"Reading {readings_count}/{num_readings}")

                except Exception as e:
                    print(f"Error processing line: {line}. Error: {e}")

            time.sleep(0.1)

    print(f"Data saved to {csv_file}")


    # II- Visualize the data with a line graph with two axes with criteria below

    df = pd.read_csv(csv_file)

    def time_to_seconds(time_str):
        try:
           
            time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S")
            
            total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
            return total_seconds
        except ValueError:
            return None

    df['Time'] = df['Time'].apply(time_to_seconds)
    df.dropna(subset=['Time'], inplace=True)

    plt.figure(figsize=(12, 8))

    # Plot the data
    plt.plot(df['Time'], df['Ax'], label='Ax')
    plt.plot(df['Time'], df['Ay'], label='Ay')
    plt.plot(df['Time'], df['Az'], label='Az')
    plt.plot(df['Time'], df['Gx'], label='Gx')
    plt.plot(df['Time'], df['Gy'], label='Gy')
    plt.plot(df['Time'], df['Gz'], label='Gz')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Acceleration (m.sq/s.sq)')

    plt.title('Motion Logging')
    plt.grid(True)
    plt.legend(loc='upper right')

    plt.show()


    # III- (Manipulate the data)

    threshold = 0.1 

    df_compress = df[
        (np.abs(df['Ax']) > threshold) | (np.abs(df['Ay']) > threshold) | (np.abs(df['Az']) > threshold)
    ]

    plt.figure(figsize=(12, 8)) 

    # Plot compressed
    plt.plot(df_compress['Time'], df_compress['Ax'], label='Ax')
    plt.plot(df_compress['Time'], df_compress['Ay'], label='Ay')
    plt.plot(df_compress['Time'], df_compress['Az'], label='Az')
    plt.plot(df_compress['Time'], df_compress['Gx'], label='Gx')
    plt.plot(df_compress['Time'], df_compress['Gy'], label='Gy')
    plt.plot(df_compress['Time'], df_compress['Gz'], label='Gz')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Acceleration (m/s^2) / Angular Velocity (deg/s)')

    plt.title('Motion Data (Compressed)')
    plt.grid(True)
    plt.legend(loc='upper right')

    plt.show()


except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if ser:
        ser.close()