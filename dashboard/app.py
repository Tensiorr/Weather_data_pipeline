import plotly.express as px
import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Create database connection."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def get_latest_measurements():
    """Get latest measurement for each city."""
    dbconnect = get_db_connection()

    query = """
    SELECT DISTINCT ON (city) 
        city, temperature_celsius, measurement_time, humidity, pressure, wind_speed
    FROM weather_measurements
    ORDER BY city, measurement_time DESC;
    """

    df = pd.read_sql(query, dbconnect)
    dbconnect.close()
    return df


def get_all_measurements():
    """Get all measurements for time series chart."""
    dbconnect = get_db_connection()

    # SQL: Pobierz wszystkie dane, posortowane po czasie
    query = """
    SELECT city, temperature_celsius, measurement_time, humidity, pressure, wind_speed
    FROM weather_measurements
    ORDER BY measurement_time DESC;
    """

    df = pd.read_sql(query, dbconnect)
    dbconnect.close()
    return df


st.set_page_config(page_title="Weather Dashboard", page_icon="☁️", layout="wide")

st.title("Weather Data Dashboard")


st.header("Current Weather")
latest_df = get_latest_measurements()


col1, col2, col3 = st.columns(3)
with col1:
    avg_temp = latest_df["temperature_celsius"].mean()
    st.metric("Average Temperature (All Cities)", f"{avg_temp:.2f}°C")
with col2:
    hottest = latest_df.loc[latest_df["temperature_celsius"].idxmax(), "city"]
    st.metric("Hottest City", hottest)
with col3:
    st.metric("Cities Tracked", len(latest_df))

st.dataframe(latest_df, use_container_width=True)

st.header("Temperature Trends")

all_data = get_all_measurements()

all_cities = all_data["city"].unique().tolist()
selected_cities = st.multiselect(
    "Select cities to display", options=all_cities, default=all_cities
)

if selected_cities:
    filtered_data = all_data[all_data["city"].isin(selected_cities)]
else:
    filtered_data = all_data


fig_temp = px.line(
    filtered_data,
    x="measurement_time",
    y="temperature_celsius",
    color="city",
    title="Temperature Over Time",
)
st.plotly_chart(fig_temp, use_container_width=True)


st.header("City Comparison")

col1, col2 = st.columns(2)

with col1:
    fig_temp_bar = px.bar(
        latest_df,
        x="city",
        y="temperature_celsius",
        title="Current Temperature by City",
        color="temperature_celsius",
        color_continuous_scale="RdYlBu_r",
    )
    st.plotly_chart(fig_temp_bar, use_container_width=True)

with col2:
    fig_humidity = px.bar(
        latest_df,
        x="city",
        y="humidity",
        title="Humidity by City",
        color="humidity",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig_humidity, use_container_width=True)
