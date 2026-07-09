"""Professional Air Quality Index dashboard built with Streamlit."""

import streamlit as st

st.set_page_config(
    page_title="Air Quality Index Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

AQI_BREAKPOINTS = [
    {
        "category": "Good",
        "range": (0, 50),
        "color": "#00E400",
        "message": "Air quality is satisfactory and pollution poses little or no risk.",
        "advice": "Enjoy outdoor activities as usual.",
    },
    {
        "category": "Moderate",
        "range": (51, 100),
        "color": "#FFFF00",
        "message": "Air quality is acceptable for most people.",
        "advice": "Unusually sensitive people should consider reducing prolonged outdoor exertion.",
    },
    {
        "category": "Unhealthy for Sensitive Groups",
        "range": (101, 150),
        "color": "#FF7E00",
        "message": "Sensitive groups may experience health effects.",
        "advice": "People with heart or lung disease, older adults, children, and teens should limit prolonged outdoor exertion.",
    },
    {
        "category": "Unhealthy",
        "range": (151, 200),
        "color": "#FF0000",
        "message": "Some members of the general public may experience health effects.",
        "advice": "Reduce prolonged or heavy outdoor exertion and take more breaks indoors.",
    },
    {
        "category": "Very Unhealthy",
        "range": (201, 300),
        "color": "#8F3F97",
        "message": "Health alert: the risk of health effects is increased for everyone.",
        "advice": "Avoid prolonged or heavy outdoor exertion; consider moving activities indoors.",
    },
    {
        "category": "Hazardous",
        "range": (301, 500),
        "color": "#7E0023",
        "message": "Health warning of emergency conditions: everyone is more likely to be affected.",
        "advice": "Stay indoors, keep windows closed, and use filtered air if available.",
    },
]

POLLUTANTS = {
    "PM2.5": {
        "value": 18.4,
        "unit": "µg/m³",
        "trend": "+2.1 from yesterday",
        "description": "Fine particles from combustion, smoke, and secondary atmospheric reactions.",
    },
    "PM10": {
        "value": 42,
        "unit": "µg/m³",
        "trend": "-5 from yesterday",
        "description": "Inhalable particles from dust, construction, roadways, and natural sources.",
    },
    "Ozone": {
        "value": 58,
        "unit": "ppb",
        "trend": "+4 from yesterday",
        "description": "Ground-level ozone formed when sunlight reacts with nitrogen oxides and VOCs.",
    },
    "NO₂": {
        "value": 21,
        "unit": "ppb",
        "trend": "Stable",
        "description": "Traffic and combustion-related gas that can irritate the respiratory system.",
    },
}

FORECAST = [
    {"day": "Today", "aqi": 72, "condition": "Moderate"},
    {"day": "Tomorrow", "aqi": 89, "condition": "Moderate"},
    {"day": "Saturday", "aqi": 118, "condition": "Sensitive Groups"},
    {"day": "Sunday", "aqi": 64, "condition": "Moderate"},
]


def get_aqi_status(aqi_value: int) -> dict:
    """Return category metadata for an AQI value."""
    for breakpoint in AQI_BREAKPOINTS:
        low, high = breakpoint["range"]
        if low <= aqi_value <= high:
            return breakpoint
    return AQI_BREAKPOINTS[-1]


def render_aqi_scale(current_aqi: int) -> None:
    """Render a responsive AQI category scale."""
    st.markdown("### AQI Scale")
    columns = st.columns(len(AQI_BREAKPOINTS))
    for column, item in zip(columns, AQI_BREAKPOINTS):
        low, high = item["range"]
        active = low <= current_aqi <= high
        border = "3px solid #111827" if active else "1px solid rgba(17, 24, 39, 0.12)"
        column.markdown(
            f"""
            <div class="scale-card" style="border:{border}; border-top: 10px solid {item['color']};">
                <strong>{item['category']}</strong><br>
                <span>{low}–{high}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown(
    """
    <style>
        .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .hero {
            padding: 2.5rem;
            border-radius: 28px;
            background: linear-gradient(135deg, #0f766e 0%, #14b8a6 50%, #a7f3d0 100%);
            color: white;
            box-shadow: 0 24px 60px rgba(15, 118, 110, 0.28);
            margin-bottom: 1.5rem;
        }
        .hero h1 { font-size: 3rem; margin-bottom: 0.4rem; }
        .hero p { font-size: 1.15rem; max-width: 760px; }
        .status-card, .recommendation-card, .scale-card {
            background: white;
            border-radius: 18px;
            padding: 1.1rem;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
            min-height: 130px;
        }
        .scale-card { text-align: center; min-height: 96px; }
        .pill {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.22);
            color: white;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .section-muted { color: #64748b; }
        [data-testid="stMetricValue"] { font-size: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Dashboard Controls")
    city = st.text_input("Location", value="Your City")
    current_aqi = st.slider("Current AQI", min_value=0, max_value=500, value=72)
    show_details = st.toggle("Show pollutant details", value=True)
    st.caption("Adjust the AQI value to preview category-specific messaging and guidance.")

status = get_aqi_status(current_aqi)

st.markdown(
    f"""
    <section class="hero">
        <span class="pill">Live Air Quality Snapshot</span>
        <h1>{city} Air Quality Index</h1>
        <p>Track current conditions, understand pollutant drivers, and get clear health guidance from a clean, professional dashboard.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

metric_col, status_col, action_col = st.columns([1, 1.2, 1.4])
with metric_col:
    st.metric("Current AQI", current_aqi, delta="Updated now")
with status_col:
    st.markdown(
        f"""
        <div class="status-card" style="border-left: 12px solid {status['color']};">
            <h3>{status['category']}</h3>
            <p>{status['message']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with action_col:
    st.markdown(
        f"""
        <div class="recommendation-card">
            <h3>Recommended Action</h3>
            <p>{status['advice']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

render_aqi_scale(current_aqi)

st.divider()

st.subheader("Key Pollutants")
st.caption("Representative readings for a polished demo experience. Connect a live API later for production data.")
pollutant_columns = st.columns(4)
for column, (name, data) in zip(pollutant_columns, POLLUTANTS.items()):
    with column:
        st.metric(name, f"{data['value']} {data['unit']}", data["trend"])
        if show_details:
            st.caption(data["description"])

st.subheader("Four-Day Outlook")
forecast_columns = st.columns(len(FORECAST))
for column, item in zip(forecast_columns, FORECAST):
    forecast_status = get_aqi_status(item["aqi"])
    column.markdown(
        f"""
        <div class="status-card" style="border-top: 8px solid {forecast_status['color']};">
            <h4>{item['day']}</h4>
            <h2>{item['aqi']}</h2>
            <p>{item['condition']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.info(
    "Tip: For a production deployment, replace the sample readings with an API such as AirNow, OpenAQ, or your local environmental authority."
)
