import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split

# Load your data
df = pd.read_csv('aw_fb_data.csv')

# I. Calories Transformation (Visualizing and choosing the best)

# 1. Original Distribution & Transformations
plt.figure(figsize=(15, 4))
plt.subplot(1, 4, 1)
df['calories'].hist(bins=30, color='blue')
plt.title('Original Calories Distribution')

df['calories_log'] = np.log1p(df['calories'])
plt.subplot(1, 4, 2)
df['calories_log'].hist(bins=30, color='green')
plt.title('Log Transformed Calories')

df['calories_sqrt'] = np.sqrt(df['calories'])
plt.subplot(1, 4, 3)
df['calories_sqrt'].hist(bins=30, color='red')
plt.title('Square Root Transformed Calories')

df['calories_cbrt'] = np.cbrt(df['calories'])
plt.subplot(1, 4, 4)
df['calories_cbrt'].hist(bins=30, color='orange')
plt.title('Cube Root Transformed Calories')

plt.tight_layout()
plt.show()

# QQ Plots for Normality Assessment
plt.figure(figsize=(15, 4))
plt.subplot(1, 4, 1)
stats.probplot(df['calories'], dist="norm", plot=plt)
plt.title('QQ Plot - Original')

plt.subplot(1, 4, 2)
stats.probplot(df['calories_log'], dist="norm", plot=plt)
plt.title('QQ Plot - Log')

plt.subplot(1, 4, 3)
stats.probplot(df['calories_sqrt'], dist="norm", plot=plt)
plt.title('QQ Plot - Sqrt')

plt.subplot(1, 4, 4)
stats.probplot(df['calories_cbrt'], dist="norm", plot=plt)
plt.title('QQ Plot - Cbrt')

plt.tight_layout()
plt.show()

# Choose the best transformation and apply it (e.g., log)
df['calories_transformed'] = df['calories_log']  # Or df['calories_sqrt'], df['calories_cbrt']


# II. Sampling and Visualization (age, height, weight)
df_sampled = df.drop_duplicates(subset='X1', keep='first').copy()

fig, axes = plt.subplots(3, 1, figsize=(8, 10))
colors = ['blue', 'green', 'red']

for i, col in enumerate(['age', 'height', 'weight']):
    axes[i].plot(df_sampled['X1'], df_sampled[col], color=colors[i], label=col.capitalize())
    axes[i].set_title(f'{col.capitalize()} Distribution')
    axes[i].set_xlabel('Participant ID')
    axes[i].set_ylabel(col.capitalize())
    axes[i].grid(True)
    axes[i].legend(loc='upper center')

plt.tight_layout()
plt.show()

# III Visualize "steps", "heart_rate", and "calories" of the first three participants in three plots with subplots (stacked plot)
fig, axes = plt.subplots(3, 1, figsize=(8, 10))
colors = ['blue', 'green', 'red']

for i, col in enumerate(['steps', 'hear_rate', 'calories_transformed']): #Using the transformed calories
    for j in range(1, 4):
        participant_data = df[df['X1'] == j]
        axes[i].plot(participant_data.index, participant_data[col], color=colors[j-1], label=f'Participant #{j}')
    axes[i].set_title(f'{col.capitalize()} for First 3 Participants')
    axes[i].set_xlabel('Data Point Index')
    axes[i].set_ylabel(col.capitalize())
    axes[i].grid(True)
    axes[i].legend(loc='upper left')

plt.tight_layout()
plt.show()

# IV Normalize the "age", "height", and "weight", and Standardize "steps" and "heart rate"
scaler_norm = MinMaxScaler()
df[['age_norm', 'height_norm', 'weight_norm']] = scaler_norm.fit_transform(df[['age', 'height', 'weight']])

scaler_std = StandardScaler()
df[['steps_std', 'heart_rate_std']] = scaler_std.fit_transform(df[['steps', 'hear_rate']])

# V Split the dataset into three categories with the following distribution: Train (70%), Validation (15%), and Test (15%) 
train_val_df, test_df = train_test_split(df, test_size=0.15, random_state=42)
train_df, val_df = train_test_split(train_val_df, test_size=(0.15/0.85), random_state=42)

print(f"Train set size: {len(train_df)}")
print(f"Validation set size: {len(val_df)}")
print(f"Test set size: {len(test_df)}")
