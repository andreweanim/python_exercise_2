import pandas as pd
import matplotlib.pyplot as plt

# Collect the data in a CSV file and submit it with the rest of your results
csv_file = "temperature_logging.csv" 

try:
    df = pd.read_csv(csv_file)  # Read the CSV into a DataFrame

    # Visualize the data with a line graph with two axes: time & temperature with criteria below
    df['Time (s)'] = df['Timesteps (ms)']

    plt.figure(figsize=(10, 6))
    plt.plot(df['Time (s)'], df['Temperature (°C)'], color='orange', label='Temperature')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature over Time')
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()

except FileNotFoundError:
    print(f"Error: CSV file '{csv_file}' not found.")
except KeyError as e:
    print(f"Error: Column '{e}' not found in CSV. Check your column names.")
except Exception as e:
    print(f"An error occurred: {e}")