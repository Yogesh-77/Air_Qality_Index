"""AirWatch Global: professional AQI forecasting dashboard."""

from datetime import datetime, timedelta

import streamlit as st

st.set_page_config(
    page_title="AirWatch Global | AQI Forecasting",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded",
)

AQI_CATEGORIES = [
    (0, 50, "Good", "#22c55e", "Air quality is healthy for outdoor activity."),
    (51, 100, "Moderate", "#eab308", "Acceptable air quality; sensitive people should watch symptoms."),
    (101, 150, "Unhealthy for Sensitive Groups", "#f97316", "Sensitive groups should reduce prolonged outdoor exertion."),
    (151, 200, "Unhealthy", "#ef4444", "Everyone should reduce prolonged or heavy outdoor exertion."),
    (201, 300, "Very Unhealthy", "#a855f7", "Avoid heavy outdoor exertion and keep windows closed."),
    (301, 500, "Hazardous", "#7f1d1d", "Stay indoors and use filtered air where possible."),
]

CITY_READINGS = [
    {
        "city": "Chennai",
        "country": "India",
        "aqi": 54,
        "predicted_aqi": 62,
        "temperature": 29.5,
        "humidity": 68,
        "wind": 11,
        "pm25": 23.5,
        "pm10": 54.2,
        "o3": 35.1,
        "no2": 16.4,
        "co": 0.54,
        "trend": "Improving",
    },
    {
        "city": "Mumbai",
        "country": "India",
        "aqi": 157,
        "predicted_aqi": 171,
        "temperature": 28.6,
        "humidity": 79,
        "wind": 7,
        "pm25": 68.2,
        "pm10": 122.8,
        "o3": 22.4,
        "no2": 44.3,
        "co": 0.91,
        "trend": "Rising",
    },
    {
        "city": "Delhi",
        "country": "India",
        "aqi": 188,
        "predicted_aqi": 204,
        "temperature": 34.7,
        "humidity": 41,
        "wind": 6,
        "pm25": 90.2,
        "pm10": 181.6,
        "o3": 58.4,
        "no2": 51.7,
        "co": 1.18,
        "trend": "Alert",
    },
    {
        "city": "Coimbatore",
        "country": "India",
        "aqi": 114,
        "predicted_aqi": 121,
        "temperature": 26.5,
        "humidity": 63,
        "wind": 9,
        "pm25": 44.8,
        "pm10": 87.3,
        "o3": 30.1,
        "no2": 29.5,
        "co": 0.63,
        "trend": "Stable",
    },
]

MODEL_SCORECARDS = [
    {"model": "Linear Regression", "mae": 13.8, "rmse": 18.5, "r2": 0.78, "best_for": "Fast baseline and interpretability"},
    {"model": "Random Forest", "mae": 8.6, "rmse": 12.1, "r2": 0.89, "best_for": "Robust tabular forecasting"},
    {"model": "LSTM", "mae": 6.9, "rmse": 10.4, "r2": 0.92, "best_for": "24-hour time-series windows"},
]

PIPELINE_STEPS = [
    "Ingest city_hour.csv and parse timestamp columns.",
    "Clean data, remove duplicates, align column names, and fill missing values.",
    "Engineer calendar, lag, rolling average, humidity, wind, and pollutant features.",
    "Train Linear Regression and Random Forest models for transparent baselines.",
    "Train LSTM on rolling 24-hour windows for sequence-aware forecasting.",
    "Save trained artifacts and load them in Streamlit for city-level predictions.",
    "Display current AQI, predicted AQI, pollutant drivers, and health alerts.",
]


def get_category(aqi: int) -> tuple[str, str, str]:
    """Return the label, color, and guidance text for an AQI value."""
    for low, high, label, color, guidance in AQI_CATEGORIES:
        if low <= aqi <= high:
            return label, color, guidance
    return AQI_CATEGORIES[-1][2], AQI_CATEGORIES[-1][3], AQI_CATEGORIES[-1][4]


def make_hourly_forecast(base_aqi: int) -> list[dict[str, int | str]]:
    """Create a deterministic 24-hour demo forecast for the selected city."""
    start_time = datetime(2026, 7, 9, 0, 0)
    forecast = []
    for hour in range(24):
        daily_cycle = [0, 4, 8, 10, 6, 2, -3, -7][hour % 8]
        commute_effect = 14 if hour in (8, 9, 17, 18, 19) else 0
        value = max(0, min(500, base_aqi + daily_cycle + commute_effect - hour // 6))
        forecast.append({"time": (start_time + timedelta(hours=hour)).strftime("%H:%M"), "aqi": value})
    return forecast


def render_city_card(reading: dict[str, int | float | str]) -> None:
    """Render one city reading card with current and predicted AQI."""
    label, color, guidance = get_category(int(reading["aqi"]))
    predicted_label, predicted_color, _ = get_category(int(reading["predicted_aqi"]))
    card_class = "city-card alert-card" if int(reading["predicted_aqi"]) >= 151 else "city-card"
    st.markdown(
        f"""
        <article class="{card_class}" style="--accent:{color}; --prediction:{predicted_color};">
            <div class="card-topline"></div>
            <div class="city-header">
                <div>
                    <p class="eyebrow">{reading['country']} · {reading['trend']}</p>
                    <h3>{reading['city']}</h3>
                </div>
                <span class="status-pill">{label}</span>
            </div>
            <div class="metric-grid">
                <div><span>Current AQI</span><strong>{reading['aqi']}</strong></div>
                <div><span>Predicted AQI</span><strong>{reading['predicted_aqi']}</strong></div>
                <div><span>PM2.5</span><strong>{reading['pm25']} µg/m³</strong></div>
                <div><span>PM10</span><strong>{reading['pm10']} µg/m³</strong></div>
                <div><span>O₃</span><strong>{reading['o3']} ppb</strong></div>
                <div><span>NO₂</span><strong>{reading['no2']} ppb</strong></div>
            </div>
            <p class="guidance"><strong>Forecast:</strong> {predicted_label}. {guidance}</p>
        </article>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
        :root { color-scheme: dark; }
        .stApp { background: #0f1117; color: #f8fafc; }
        .block-container { padding-top: 1.6rem; padding-bottom: 3rem; }
        section.hero {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.20);
            border-radius: 28px;
            padding: 2.2rem;
            background:
                radial-gradient(circle at 18% 18%, rgba(96, 165, 250, 0.38), transparent 28%),
                linear-gradient(135deg, #0b1220 0%, #172554 46%, #2563eb 100%);
            box-shadow: 0 26px 70px rgba(0, 0, 0, 0.32);
        }
        .hero h1 { font-size: clamp(2.3rem, 6vw, 4.8rem); margin: 0.2rem 0; letter-spacing: -0.05em; }
        .hero p { color: #dbeafe; font-size: 1.1rem; max-width: 850px; }
        .badge-row { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 1.2rem; }
        .badge {
            border: 1px solid rgba(255,255,255,0.24);
            background: rgba(255,255,255,0.12);
            border-radius: 999px;
            padding: 0.45rem 0.78rem;
            font-size: 0.82rem;
            font-weight: 700;
        }
        .kpi-card, .city-card, .model-card, .timeline-card {
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 22px;
            background: linear-gradient(180deg, #1f2430 0%, #171b24 100%);
            box-shadow: 0 18px 42px rgba(0, 0, 0, 0.25);
        }
        .kpi-card { padding: 1.2rem; min-height: 136px; }
        .kpi-card span, .metric-grid span, .eyebrow { color: #94a3b8; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.09em; }
        .kpi-card strong { display: block; font-size: 2.1rem; margin-top: 0.3rem; }
        .city-card { position: relative; overflow: hidden; padding: 1.2rem; min-height: 338px; }
        .alert-card { background: linear-gradient(180deg, #fee2e2 0%, #fecaca 100%); color: #7f1d1d; }
        .card-topline { height: 5px; width: 100%; background: var(--accent); position: absolute; top: 0; left: 0; }
        .city-header { display: flex; justify-content: space-between; gap: 1rem; align-items: flex-start; }
        .city-header h3 { margin: 0.2rem 0 0; font-size: 1.55rem; }
        .status-pill { background: var(--accent); color: #020617; font-weight: 800; padding: 0.35rem 0.65rem; border-radius: 999px; font-size: 0.72rem; }
        .metric-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.75rem; margin: 1.1rem 0; }
        .metric-grid div { border-radius: 14px; background: rgba(15, 23, 42, 0.42); padding: 0.78rem; }
        .metric-grid strong { display: block; margin-top: 0.18rem; }
        .guidance { color: inherit; opacity: 0.9; font-size: 0.9rem; }
        .model-card, .timeline-card { padding: 1rem; min-height: 168px; }
        .timeline-card { border-left: 4px solid #60a5fa; }
        div[data-testid="stSidebar"] { background: #20242e; }
        div[data-testid="stSidebar"] * { color: #f8fafc; }
        [data-testid="stMetricValue"] { color: #f8fafc; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Settings")
    selected_city = st.selectbox("Focus city", [city["city"] for city in CITY_READINGS])
    city_limit = st.slider("Cities shown", 1, len(CITY_READINGS), len(CITY_READINGS))
    forecast_hours = st.slider("Forecast horizon", 6, 24, 24, step=6)
    alert_threshold = st.slider("Alert threshold", 50, 300, 151, step=10)
    st.caption("Demo data mirrors the final project workflow. Replace constants with saved model outputs when artifacts are available.")

selected_reading = next(reading for reading in CITY_READINGS if reading["city"] == selected_city)
visible_cities = CITY_READINGS[:city_limit]
high_risk_count = sum(1 for reading in visible_cities if int(reading["predicted_aqi"]) >= alert_threshold)
average_aqi = round(sum(int(reading["aqi"]) for reading in visible_cities) / len(visible_cities))
best_model = min(MODEL_SCORECARDS, key=lambda item: item["mae"])

st.markdown(
    """
    <section class="hero">
        <span class="badge">🌎 AirWatch Global</span>
        <h1>Live + Predicted AQI, Realtime Alerts & Health Risk</h1>
        <p>
            A complete Streamlit front end for an air-quality forecasting project: clean data, engineer
            time-aware features, train classical and LSTM models, and present city-level AQI alerts in one professional dashboard.
        </p>
        <div class="badge-row">
            <span class="badge">city_hour.csv ready</span>
            <span class="badge">Linear Regression</span>
            <span class="badge">Random Forest</span>
            <span class="badge">LSTM 24-hour windows</span>
            <span class="badge">AQI health guidance</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.write("")
kpi_cols = st.columns(4)
kpi_values = [
    ("Average AQI", average_aqi, "Across visible cities"),
    ("High-risk alerts", high_risk_count, f"Predicted AQI ≥ {alert_threshold}"),
    ("Best model", best_model["model"], f"MAE {best_model['mae']}"),
    ("Forecast horizon", f"{forecast_hours}h", "Hourly windows"),
]
for column, (label, value, helper) in zip(kpi_cols, kpi_values):
    column.markdown(f"<div class='kpi-card'><span>{label}</span><strong>{value}</strong><p>{helper}</p></div>", unsafe_allow_html=True)

dashboard_tab, forecast_tab, models_tab, workflow_tab = st.tabs(["Dashboard", "24-hour forecast", "Models", "Project workflow"])

with dashboard_tab:
    st.subheader("City monitoring board")
    city_columns = st.columns(2)
    for index, reading in enumerate(visible_cities):
        with city_columns[index % 2]:
            render_city_card(reading)

with forecast_tab:
    st.subheader(f"{selected_city} hourly AQI forecast")
    hourly_forecast = make_hourly_forecast(int(selected_reading["predicted_aqi"]))[:forecast_hours]
    chart_data = {"time": [item["time"] for item in hourly_forecast], "aqi": [item["aqi"] for item in hourly_forecast]}
    st.line_chart(chart_data, x="time", y="aqi", height=330)
    forecast_category, forecast_color, forecast_guidance = get_category(max(item["aqi"] for item in hourly_forecast))
    st.markdown(
        f"<div class='timeline-card' style='border-left-color:{forecast_color};'><h3>Peak risk: {forecast_category}</h3><p>{forecast_guidance}</p></div>",
        unsafe_allow_html=True,
    )

with models_tab:
    st.subheader("Model comparison")
    model_columns = st.columns(3)
    for column, card in zip(model_columns, MODEL_SCORECARDS):
        column.markdown(
            f"""
            <div class="model-card">
                <h3>{card['model']}</h3>
                <p><strong>MAE:</strong> {card['mae']} &nbsp; <strong>RMSE:</strong> {card['rmse']}</p>
                <p><strong>R²:</strong> {card['r2']}</p>
                <p>{card['best_for']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.success("Recommended production path: train Random Forest as a dependable baseline, then deploy LSTM when 24-hour sequence artifacts are available.")

with workflow_tab:
    st.subheader("End-to-end project plan")
    for step_number, step in enumerate(PIPELINE_STEPS, start=1):
        st.markdown(f"<div class='timeline-card'><h4>{step_number}. {step}</h4></div>", unsafe_allow_html=True)
    st.info("This page is structured so future files such as notebooks, model artifacts, and datasets can plug into the same dashboard without redesigning the UI.")
