import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Load & process data
data = pd.read_csv("processed_weather.csv", sep=';', low_memory=False)
cols_to_convert = [
    'MinTemp', 'MaxTemp', 'Temp9am', 'Temp3pm',
    'Humidity9am', 'Humidity3pm',
    'WindSpeed9am', 'WindSpeed3pm', 'WindGustSpeed',
    'Pressure9am', 'Pressure3pm'
]
for col in cols_to_convert:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Feature engineering
data['temp_day_avg'] = data[['MinTemp', 'MaxTemp', 'Temp9am', 'Temp3pm']].mean(axis=1)
data['humidity_avg'] = data[['Humidity9am', 'Humidity3pm']].mean(axis=1)
data['wind_speed_avg'] = data[['WindSpeed9am', 'WindSpeed3pm', 'WindGustSpeed']].mean(axis=1)
data['pressure_avg'] = data[['Pressure9am', 'Pressure3pm']].mean(axis=1)
processed_data = data[['temp_day_avg', 'humidity_avg', 'wind_speed_avg', 'pressure_avg']].iloc[:500].copy()

# Drop rows with NaN values to avoid fuzzy logic errors
processed_data.dropna(inplace=True)

# Define fuzzy variables
temp = ctrl.Antecedent(np.arange(0, 51, 1), 'Temp')
temp['Low'] = fuzz.trapmf(temp.universe, [0, 0, 10, 20])
temp['Medium'] = fuzz.trimf(temp.universe, [15, 25, 35])
temp['High'] = fuzz.trapmf(temp.universe, [30, 40, 50, 50])

humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'Humidity')
humidity['Low'] = fuzz.trapmf(humidity.universe, [0, 0, 30, 50])
humidity['Medium'] = fuzz.trimf(humidity.universe, [40, 55, 70])
humidity['High'] = fuzz.trapmf(humidity.universe, [60, 80, 100, 100])

wind = ctrl.Antecedent(np.arange(0, 101, 1), 'WindSpeed')
wind['Low'] = fuzz.trapmf(wind.universe, [0, 0, 10, 20])
wind['Medium'] = fuzz.trimf(wind.universe, [15, 30, 45])
wind['High'] = fuzz.trapmf(wind.universe, [40, 60, 100, 100])

pressure = ctrl.Antecedent(np.arange(980, 1041, 1), 'Pressure')
pressure['Low'] = fuzz.trapmf(pressure.universe, [980, 980, 990, 1000])
pressure['Medium'] = fuzz.trimf(pressure.universe, [995, 1008, 1020])
pressure['High'] = fuzz.trapmf(pressure.universe, [1015, 1030, 1040, 1040])

storm_risk = ctrl.Consequent(np.arange(0, 11, 1), 'StormRisk')
storm_risk['Low'] = fuzz.trapmf(storm_risk.universe, [0, 0, 2, 4])
storm_risk['Medium'] = fuzz.trimf(storm_risk.universe, [3, 5, 7])
storm_risk['High'] = fuzz.trapmf(storm_risk.universe, [6, 8, 10, 10])

# Define fuzzy rules
rule1 = ctrl.Rule(pressure['Low'] | wind['High'], storm_risk['High'])
rule2 = ctrl.Rule((humidity['High'] & (wind['Medium'] | temp['High'])), storm_risk['High'])
rule3 = ctrl.Rule((humidity['Medium'] & temp['Medium'] & wind['Medium']), storm_risk['Medium'])
rule4 = ctrl.Rule((pressure['Medium'] & humidity['Low']), storm_risk['Low'])
rule5 = ctrl.Rule((wind['Low'] & pressure['High']), storm_risk['Low'])
rule6 = ctrl.Rule((temp['Low'] | temp['Medium'] | temp['High']), storm_risk['Medium'])

storm_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])

def compute_storm_risk(temp_val, hum_val, wind_val, pres_val):
    sim = ctrl.ControlSystemSimulation(storm_ctrl)
    sim.input['Temp'] = temp_val
    sim.input['Humidity'] = hum_val
    sim.input['WindSpeed'] = wind_val
    sim.input['Pressure'] = pres_val
    sim.compute()
    val = sim.output['StormRisk']

    if val < 3:
        return 'Low'
    elif val < 7:
        return 'Medium'
    else:
        return 'High'

def row_to_label(row):
    return compute_storm_risk(
        row['temp_day_avg'],
        row['humidity_avg'],
        row['wind_speed_avg'],
        row['pressure_avg']
    )

# Generate target labels using fuzzy logic
processed_data['StormRiskLabel'] = processed_data.apply(row_to_label, axis=1)

# Prepare for training
X = processed_data[['temp_day_avg', 'humidity_avg', 'wind_speed_avg', 'pressure_avg']]
y = processed_data['StormRiskLabel']

le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Stratified split to include all classes
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, 
    test_size=0.2, 
    random_state=42,
    stratify=y_encoded
)

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# Evaluation
all_labels = list(range(len(le.classes_)))
print("\nRandom Forest Classification Report:")
print(classification_report(
    y_test, 
    y_pred, 
    labels=all_labels,
    target_names=le.classes_,
    zero_division=0
))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=all_labels))