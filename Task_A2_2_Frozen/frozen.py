import pandas as pd
import matplotlib.pyplot as plt

# Reading csv data
try:
    df = pd.read_csv('IOT-temp.csv')
except FileNotFoundError:
    print("Error: 'csv' not found.")
    exit()

# Conversion of 'noted_date' to datetime 
try:
    df['noted_date'] = pd.to_datetime(df['noted_date'], format='%d-%m-%Y %H:%M', errors='coerce', dayfirst=True)
except (ValueError, TypeError) as e:
    print(f"Error parsing dates: {e}. Check the 'noted_date' column for inconsistencies.")
    exit()

# Change the "In" and "Out" text of the "Out\In" column to 1 and 0 respectively
df['out/in'] = df['out/in'].replace({'In': 1, 'Out': 0})

# Set index and sort (using the original 'noted_date' as index)
df.set_index('noted_date', inplace=True)
df.sort_index(inplace=True)

# last week filter 
start_date = pd.to_datetime('2018-12-02') 
end_date = pd.to_datetime('2018-12-08')

df_last_week = df[(df.index >= start_date) & (df.index <= end_date)] 

# Data plot (using df_last_week and plotting based on 'out/in' values)
plt.figure(figsize=(12, 6)) # Same figure size as the correct code

plt.plot(
    df_last_week[df_last_week["out/in"] == 0].index, # Filtered for "Out" (now 0)
    df_last_week[df_last_week["out/in"] == 0]["temp"],
    label="Outdoor Temperature",
)
plt.plot(
    df_last_week[df_last_week["out/in"] == 1].index, # Filtered for "In" (now 1)
    df_last_week[df_last_week["out/in"] == 1]["temp"],
    label="Indoor Temperature",
)

plt.xlabel("Date")
plt.ylabel("Temperature")
plt.title("Indoor and Outdoor Temperature")
plt.grid(True)
plt.legend(loc="upper right")
plt.show()