# 🌿 Air Quality Index Dashboard

A polished Streamlit dashboard for presenting Air Quality Index (AQI) conditions, pollutant details, forecast cards, and public health guidance.

## Features

- Professional responsive layout with a branded hero section
- Interactive AQI slider and location input
- Category-specific AQI messaging and recommended actions
- Pollutant metric cards for PM2.5, PM10, ozone, and nitrogen dioxide
- Four-day AQI outlook using clear color-coded cards

## Run locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the Streamlit app:

   ```bash
   streamlit run streamlit_app.py
   ```

## Deployment

This repository is ready for Streamlit Community Cloud. Point the app entry file to `streamlit_app.py` and deploy from your GitHub repository.

> The current dashboard uses sample values for presentation. Replace the demo constants in `streamlit_app.py` with a live air-quality API when you are ready for production data.
