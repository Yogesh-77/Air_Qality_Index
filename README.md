# 🌎 AirWatch Global — Air Quality Index Forecasting Dashboard

AirWatch Global is a professional Streamlit dashboard for an Air Quality Index (AQI) forecasting project. It is designed around the complete workflow shown in the project brief: clean `city_hour.csv`, engineer time and pollutant features, train forecasting models, save artifacts, and display current plus predicted AQI with health alerts.

## Project goals

1. Clean and prepare air-quality data with consistent timestamps, aligned feature names, duplicate removal, and missing-value handling.
2. Engineer time-series and weather/pollutant features such as month, day, hour, rolling averages, lag values, PM2.5, PM10, O₃, NO₂, CO, temperature, humidity, and wind speed.
3. Train and compare classical machine-learning models such as Linear Regression and Random Forest.
4. Train an LSTM model using rolling 24-hour windows for sequence-aware AQI forecasting.
5. Save trained models and use them in Streamlit to show current AQI, predicted AQI, city-level risk, and health alerts.

## What the app includes today

- Dark, professional **AirWatch Global** dashboard design
- Sidebar controls for focus city, visible city count, forecast horizon, and alert threshold
- City cards for Chennai, Mumbai, Delhi, and Coimbatore
- Current AQI, predicted AQI, pollutant drivers, forecast category, and health guidance
- 24-hour forecast tab with a focus-city line chart
- Model comparison cards for Linear Regression, Random Forest, and LSTM
- Workflow tab documenting the full data-cleaning, training, saving, and deployment path

## Repository structure

```text
.
├── README.md
├── LICENSE
├── requirements.txt
└── streamlit_app.py
```

## Run locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the dashboard:

   ```bash
   streamlit run streamlit_app.py
   ```

## Deployment note

This is a Streamlit application, so it will not run as a normal static GitHub Pages site. For a proper live display, deploy it with **Streamlit Community Cloud** and set the main file to `streamlit_app.py`.

## Next professional upgrade

When the dataset and trained artifacts are added, replace the demo constants in `streamlit_app.py` with:

- A data loader for `city_hour.csv`
- Saved model files for Linear Regression, Random Forest, and LSTM
- A scaler/encoder pipeline for the same preprocessing used during training
- Real predictions generated from the latest 24 hourly records per city
