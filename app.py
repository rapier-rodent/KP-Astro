import streamlit as st
import requests

st.title("Vedic Astrology Chart Generator")

# User inputs for horoscope generation
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
    # Prepare the payload for the API request
    payload = {
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
    }

    # Make a POST request to the FastAPI backend
    response = requests.post("https://kp-astro.onrender.com/get_all_horoscope_data", json=payload)

    if response.status_code == 200:
        chart_data = response.json()
        st.write("Generated Chart Data:")
        st.json(chart_data)  # Display the chart data in a readable format
        
        # Display additional information
        st.write("Birth Time (IST):", chart_data.get("birth_time_ist"))
        st.write("Ayanamsa Value:", chart_data.get("ayanamsa"))
        st.write("Krishnamurti Ayanamsa Value:", chart_data.get("krishnamurti_ayanamsa"))
    else:
        st.error("Error generating chart data.")
