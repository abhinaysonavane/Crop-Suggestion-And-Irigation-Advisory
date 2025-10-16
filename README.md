# Crop Suggestion and Irrigation Advisory

A Flask-based IoT web app that uses Arduino sensor data and Machine Learning to recommend suitable crops and irrigation schedules in real time. The system integrates live temperature, humidity, and soil moisture readings with a Random Forest model to deliver smart-farming insights.

## Features
- Real-time data ingestion from Arduino sensors (temp, humidity, soil moisture)
- Dashboard to view live sensor readings and model predictions
- Crop suitability recommendations based on sensor data and historical dataset
- Irrigation advisory (when to water and approximate amount)
- Scripts for training and exporting Random Forest models
- Simple REST endpoints for sensor integration and mobile/web clients

## Tech stack
- Backend: Flask (Python)
- ML: scikit-learn (Random Forest)
- IoT: Arduino (serial data)
- Data: pandas for ingestion and preprocessing
- Frontend: HTML/CSS/JS (Bootstrap optional)

## Quick start (development)
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Crop-Suggestion-And-Irrigation-Advisory.git
   cd Crop-Suggestion-And-Irrigation-Advisory
2. Create virtual environment and install dependencies:

    python -m venv venv
    source venv/bin/activate   # macOS / Linux
    venv\Scripts\activate      # Windows
    pip install -r requirements.txt


3. Configure serial port in app.py or config.py (e.g. COM6 on Windows, /dev/ttyUSB0 on Linux).

Run the Flask app:

flask run


Open http://127.0.0.1:5000 to view the dashboard.

Model training

A sample script train_model.py prepares data, trains a Random Forest, and saves the model (model.pkl).

Provide a data/ folder with CSV(s) for training and testing. Example columns: temperature, humidity, soil_moisture, soil_type, crop_label.

File structure (suggested)
/
├─ app.py
├─ requirements.txt

├─ templates/index.html
├─ data/realistic_crop_iriigation_dataset.csv
├─ README.md
└─ .gitignore


