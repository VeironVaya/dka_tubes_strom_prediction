import pandas as pd
import sympy as sp
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt 
from skfuzzy import control as ctrl
from IPython.display import display
data = pd.read_csv("processed_weather.csv",sep = ';',low_memory=False)
data.head()
cols_to_convert = [
    'MinTemp', 'MaxTemp', 'Temp9am', 'Temp3pm',
    'Humidity9am', 'Humidity3pm',
    'WindSpeed9am', 'WindSpeed3pm', 'WindGustSpeed',
    'Pressure9am', 'Pressure3pm'
]

for col in cols_to_convert:
    data[col] = pd.to_numeric(data[col],errors = 'coerce')
data['temp_day_avg'] = data[['MinTemp', 'MaxTemp', 'Temp9am', 'Temp3pm']].mean(axis=1)
data['humidity_avg'] = data[['Humidity9am', 'Humidity3pm']].mean(axis=1)
data['wind_speed_avg'] = data[['WindSpeed9am', 'WindSpeed3pm', 'WindGustSpeed']].mean(axis=1)
data['pressure_avg'] = data[['Pressure9am', 'Pressure3pm']].mean(axis=1)
processed_data = data[['temp_day_avg', 'humidity_avg', 'wind_speed_avg', 'pressure_avg']]

processed_data.head()

# Data Slice
subProcData = processed_data.iloc[:500].copy()
# Fuzzy Variables
temp = ctrl.Antecedent(np.arange(0, 51, 1), 'Temp')
temp['Low']    = fuzz.trapmf(temp.universe,  [0,  0,  10,  20])
temp['Medium'] = fuzz.trimf(temp.universe,   [15, 25, 35])
temp['High']   = fuzz.trapmf(temp.universe,  [30, 40, 50, 50])

# Plotting
plt.plot(temp.universe, temp['Low'].mf, label='Low')
plt.plot(temp.universe, temp['Medium'].mf, label='Medium')
plt.plot(temp.universe, temp['High'].mf, label='High')
plt.title('Fungsi Keanggotaan Temperatur')
plt.xlabel('Temperatur (°C)')
plt.ylabel('Derajat Keanggotaan')
plt.legend()
plt.grid(True)
plt.show()

humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'Humidity')
humidity['Low']    = fuzz.trapmf(humidity.universe,  [0,   0,   30,  50])
humidity['Medium'] = fuzz.trimf(humidity.universe,   [40,  55,  70])
humidity['High']   = fuzz.trapmf(humidity.universe,  [60,  80,  100, 100])

plt.plot(humidity.universe, humidity['Low'].mf, label='Low')
plt.plot(humidity.universe, humidity['Medium'].mf, label='Medium')
plt.plot(humidity.universe, humidity['High'].mf, label='High')
plt.title('Fungsi Keanggotaan Kelembaban')
plt.xlabel('Kelembaban (%)')
plt.ylabel('Derajat Keanggotaan')
plt.legend()
plt.grid(True)
plt.show()

wind = ctrl.Antecedent(np.arange(0, 101, 1), 'WindSpeed')
wind['Low']    = fuzz.trapmf(wind.universe,  [0,   0,   10,  20])
wind['Medium'] = fuzz.trimf(wind.universe,   [15,  30,  45])
wind['High']   = fuzz.trapmf(wind.universe,  [40,  60,  100, 100])

plt.plot(wind.universe, wind['Low'].mf, label='Low')
plt.plot(wind.universe, wind['Medium'].mf, label='Medium')
plt.plot(wind.universe, wind['High'].mf, label='High')
plt.title('Fungsi Keanggotaan Kecepatan Angin')
plt.xlabel('Kecepatan Angin (km/jam)')
plt.ylabel('Derajat Keanggotaan')
plt.legend()
plt.grid(True)
plt.show()

pressure = ctrl.Antecedent(np.arange(980, 1041, 1), 'Pressure')
pressure['Low']    = fuzz.trapmf(pressure.universe,  [980,  980,  990, 1000])
pressure['Medium'] = fuzz.trimf(pressure.universe,   [995, 1008, 1020])
pressure['High']   = fuzz.trapmf(pressure.universe,  [1015, 1030, 1040, 1040])

plt.plot(pressure.universe, pressure['Low'].mf, label='Low')
plt.plot(pressure.universe, pressure['Medium'].mf, label='Medium')
plt.plot(pressure.universe, pressure['High'].mf, label='High')
plt.title('Fungsi Keanggotaan Tekanan')
plt.xlabel('Tekanan (hPa)')
plt.ylabel('Derajat Keanggotaan')
plt.legend()
plt.grid(True)
plt.show()

storm_risk = ctrl.Consequent(np.arange(0, 11, 1), 'StormRisk')
storm_risk['Low']    = fuzz.trapmf(storm_risk.universe,  [0,   0,   2,   4])
storm_risk['Medium'] = fuzz.trimf(storm_risk.universe,   [3,   5,   7])
storm_risk['High']   = fuzz.trapmf(storm_risk.universe,  [6,   8,   10,  10])


plt.plot(storm_risk.universe, storm_risk['Low'].mf, label='Low')
plt.plot(storm_risk.universe, storm_risk['Medium'].mf, label='Medium')
plt.plot(storm_risk.universe, storm_risk['High'].mf, label='High')
plt.title('Fungsi Keanggotaan Risiko Badai')
plt.xlabel('Risiko Badai')
plt.ylabel('Derajat Keanggotaan')
plt.legend()
plt.grid(True)
plt.show()

# (1) High Risk if (Pressure is Low) OR (Wind is High)
rule1 = ctrl.Rule(
    pressure['Low'] | wind['High'],
    storm_risk['High']
)

# (2) High Risk if (Humidity is High) AND (Wind is Medium OR Temp is High)
rule2 = ctrl.Rule(
    (humidity['High'] & (wind['Medium'] | temp['High'])),
    storm_risk['High']
)

# (3) Medium Risk if (Humidity, Temp, and Wind are all Medium)
rule3 = ctrl.Rule(
    (humidity['Medium'] & temp['Medium'] & wind['Medium']),
    storm_risk['Medium']
)

# (4) Low Risk if (Pressure is Medium) AND (Humidity is Low)
rule4 = ctrl.Rule(
    (pressure['Medium'] & humidity['Low']),
    storm_risk['Low']
)

# (5) Low Risk if (Wind is Low) AND (Pressure is High)
rule5 = ctrl.Rule(
    (wind['Low'] & pressure['High']),
    storm_risk['Low']
)

# (6) Default: catch‐all → Medium Risk
# Since for any numeric Temp, at least one of temp['Low'], temp['Medium'], temp['High'] is nonzero,
# this rule will always fire to some degree. 
rule6 = ctrl.Rule(
    (temp['Low'] | temp['Medium'] | temp['High']),
    storm_risk['Medium']
)

# Build the control system with all six rules:
storm_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
# For Row Function
def compute_storm_risk(temp_val, hum_val, wind_val, pres_val):
    # Create a fresh simulator each time
    sim = ctrl.ControlSystemSimulation(storm_ctrl)
    sim.input['Temp']      = temp_val
    sim.input['Humidity']  = hum_val
    sim.input['WindSpeed'] = wind_val
    sim.input['Pressure']  = pres_val

    
    sim.compute()
    val = sim.output['StormRisk']  # should exist if everything is defined above


    # Turn numeric 0..10 back into a category
    if val < 3:
        cat = 'Low'
    elif val < 7:
        cat = 'Medium'
    else:
        cat = 'High'
  
    return val, cat

def row_to_risk(row):
    v, c = compute_storm_risk(
        row['temp_day_avg'],
        row['humidity_avg'],
        row['wind_speed_avg'],
        row['pressure_avg']
    )
    return pd.Series({'StormRiskValue': v, 'StormRiskCategory': c})

#Implementation
risk_df = subProcData.apply(row_to_risk, axis=1)
subProcData[['StormRiskValue','StormRiskCategory']] = risk_df

# Format float and rename columns
pretty_df = subProcData.copy()
pretty_df['StormRiskValue'] = pretty_df['StormRiskValue'].round(3)
pretty_df = pretty_df.rename(columns={
    'temp_day_avg': 'Temp (°C)',
    'humidity_avg': 'Humidity (%)',
    'wind_speed_avg': 'Wind (km/h)',
    'pressure_avg': 'Pressure (hPa)',
    'StormRiskValue': 'Storm Risk Score',
    'StormRiskCategory': 'Risk Category'
})

print("\n🌪️ Final Storm Risk Prediction:")
display(pretty_df)