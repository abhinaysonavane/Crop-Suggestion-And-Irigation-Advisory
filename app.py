from flask import Flask, render_template, jsonify
import serial
import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import threading

app = Flask(__name__)

# ======== SERIAL COMMUNICATION ========
# Adjust COM port for your system (Windows: COM3, Linux/Mac: /dev/ttyUSB0)
try:
    arduino = serial.Serial('COM6', 9600, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"Error connecting to Arduino on COM6: {e}. Check if the port is correct and available.")
    # Set arduino to None or exit if communication is mandatory
    arduino = None


# ======== ML MODEL TRAINING ========
# Variables to hold models, initialized to None
crop_model = None
irrigation_model = None

try:
    data = pd.read_csv('realistic_crop_irrigation_dataset.csv')

    # CRITICAL FIX: Clean column names to remove any leading/trailing whitespace
    data.columns = data.columns.str.strip()

    # Assuming CSV columns: Temperature, Humidity, SoilMoisture, Crop, Irrigation_Needed
    X = data[['Temperature', 'Humidity', 'SoilMoisture']]
    y_crop = data['Crop']
    y_irrigation = data['Irrigation_Needed'] 

    crop_model = RandomForestClassifier()
    crop_model.fit(X, y_crop)

    irrigation_model = RandomForestClassifier()
    irrigation_model.fit(X, y_irrigation)

except FileNotFoundError:
    print("Error: 'synthetic_crop_irrigation_dataset.csv' not found. Please ensure it is in the same directory.")
    # Exit or continue without ML functionality
    exit()
except KeyError as e:
    print(f"KeyError: {e}. Column name mismatch in CSV. Check if 'Temperature', 'Humidity', 'SoilMoisture', 'Crop', and 'Irrigation_Needed' are spelled exactly right (case-sensitive) and have no extra spaces.")
    # Exit or continue without ML functionality
    exit()


# ======== SENSOR DATA STORAGE ========
sensor_data = {'temp': 0, 'hum': 0, 'soil': 0, 'crop': 'N/A', 'advice': 'N/A'}

# ======== READ ARDUINO DATA IN BACKGROUND ========
def read_arduino():
    if arduino is None:
        print("Arduino connection failed, background thread not running.")
        return

    while True:
        try:
            line = arduino.readline().decode('utf-8').strip()
            if line:
                # Ensure the line has the expected number of values (3: temp, hum, soil)
                values = line.split(',')
                if len(values) == 3:
                    temp, hum, soil = map(float, values)
                    
                    sensor_data['temp'] = temp
                    sensor_data['hum'] = hum
                    sensor_data['soil'] = soil

                    # --- IMPROVED PREDICTION LOGIC: Using a DataFrame for robustness ---
                    if crop_model and irrigation_model:
                        input_data_df = pd.DataFrame([[temp, hum, soil]], 
                                                     columns=['Temperature', 'Humidity', 'SoilMoisture'])
                        
                        # Predict the crop and irrigation advice using the trained models
                        sensor_data['crop'] = crop_model.predict(input_data_df)[0]
                        sensor_data['advice'] = irrigation_model.predict(input_data_df)[0]
                    # --- END IMPROVEMENT ---

                # time.sleep(0.5) # Add a small delay if the Arduino sends data too fast
                
        except ValueError:
            # Occurs if map(float, ...) fails (non-numeric data received)
            print(f"Non-numeric data received: {line}")
            continue
        except Exception as e:
            # General error handling for reading/decoding
            print(f"Error reading from Arduino: {e}")
            time.sleep(1) # Wait before trying again
            continue

# Start the Arduino reading thread only if connected
if arduino:
    thread = threading.Thread(target=read_arduino)
    thread.daemon = True
    thread.start()

# ======== FLASK ROUTES ========
@app.route('/')
def index():
    # Renders the index.html dashboard
    return render_template('index.html')

@app.route('/data')
def data():
    # Returns the live sensor data and ML advice as JSON
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) # use_reloader=False prevents thread from running twice
