import streamlit as st
import requests

st.title("Vedic Astrology Chart Generator")

year = st.number_input("Year", min_value=1900, max_value=2100)
month = st.number_input("Month", min_value=1, max_value=12)
day = st.number_input("Day", min_value=1, max_value=31)
hour = st.number_input("Hour", min_value=0, max_value=23)
minute = st.number_input("Minute", min_value=0, max_value=59)
second = st.number_input("Second", min_value=0, max_value=59)
utc = st.text_input("UTC (e.g., +5:30)")
latitude = st.number_input("Latitude", format="%.6f")
longitude = st.number_input("Longitude", format="%.6f")
ayanamsa = st.selectbox("Ayanamsa", ["Lahiri", "Krishnamurti"])
house_system = st.selectbox("House System", ["Equal", "Placidus"])

if st.button("Generate Horoscope"):
    response = requests.post("https://your-render-url/get_all_horoscope_data", json={
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
        "utc": utc,
        "latitude": latitude,
        "longitude": longitude,
        "ayanamsa": ayanamsa,
        "house_system": house_system
    })
    if response.status_code == 200:
        chart_data = response.json()
        st.write("Generated Chart Data:", chart_data)
    else:
        st.error("Error generating chart data.")
