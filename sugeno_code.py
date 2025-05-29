import pandas as pd
import numpy as np
from IPython.display import display

# Load and preprocess data
data = pd.read_csv("processed_weather.csv", sep=';', low_memory=False)

cols_to_convert = [
    'MinTemp', 'MaxTemp', 'Temp9am', 'Temp3pm',
    'Humidity9am', 'Humidity3pm',
    'WindSpeed9am', 'WindSpeed3pm', 'WindGustSpeed',
    'Pressure9am', 'Pressure3pm'
]
for col in cols_to_convert:
    data[col] = pd.to_numeric(data[col], errors='coerce')

data['temp_day_avg'] = data[['MinTemp', 'MaxTemp', 'Temp9am', 'Temp3pm']].mean(axis=1)
data['humidity_avg'] = data[['Humidity9am', 'Humidity3pm']].mean(axis=1)
data['wind_speed_avg'] = data[['WindSpeed9am', 'WindSpeed3pm', 'WindGustSpeed']].mean(axis=1)
data['pressure_avg'] = data[['Pressure9am', 'Pressure3pm']].mean(axis=1)

# Use only first 500 samples
subProcData = data[['temp_day_avg', 'humidity_avg', 'wind_speed_avg', 'pressure_avg']].iloc[:500].copy()

# Normalize input features to [0,1] for Sugeno inference
subProcData['temp_norm'] = (subProcData['temp_day_avg'] - 0) / (50 - 0)
subProcData['humidity_norm'] = subProcData['humidity_avg'] / 100
subProcData['wind_norm'] = subProcData['wind_speed_avg'] / 100
subProcData['pressure_norm'] = (subProcData['pressure_avg'] - 980) / (60)

# Define weights for Sugeno-style output (can be tuned based on domain knowledge)
w_temp = 0.6
w_hum = 0.4
w_wind = 0.2
w_pres = 0.2

# Sugeno risk score (weighted sum of normalized inputs)
subProcData['Storm Risk Score'] = (
    subProcData['temp_norm'] * w_temp +
    subProcData['humidity_norm'] * w_hum +
    subProcData['wind_norm'] * w_wind +
    (1 - subProcData['pressure_norm']) * w_pres 
) * 10 

# Categorize score
subProcData['Risk Category'] = subProcData['Storm Risk Score'].apply(
    lambda x: 'Low' if x < 4.8 else ('Medium' if x < 7 else 'High')
)

# Rename columns for display
pretty_df = subProcData.rename(columns={
    'temp_day_avg': 'Temp (°C)',
    'humidity_avg': 'Humidity (%)',
    'wind_speed_avg': 'Wind (km/h)',
    'pressure_avg': 'Pressure (hPa)'
})

pretty_df['Storm Risk Score'] = pretty_df['Storm Risk Score'].round(3)
pretty_df = pretty_df[[
    'Temp (°C)', 'Humidity (%)', 'Wind (km/h)', 'Pressure (hPa)',
    'Storm Risk Score', 'Risk Category']]

print("\n🌪️ Final Storm Risk Prediction (Sugeno):")
display(pretty_df.head(20))
