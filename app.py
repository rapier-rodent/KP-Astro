import streamlit as st
import requests

# Constants
API_URL = "https://your-fastapi-service-url.com"  # Replace with your actual FastAPI service URL
UTC_OFFSET = "-05:30:00"

def get_horoscope_data(year, month, day, hour, minute, second, latitude, longitude, ayanamsa="Lahiri", house_system="Equal"):
    payload = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
        "utc": UTC_OFFSET,
        "latitude": latitude,
        "longitude": longitude,
        "ayanamsa": ayanamsa,
        "house_system": house_system
    }
    response = requests.post(f"{API_URL}/get_all_horoscope_data", json=payload)
    return response.json()

def main():
    st.title("Vedic Astrology Horoscope Chart")

    with st.form("horoscope_form"):
        year = st.number_input("Year", min_value=1900, max_value=2100, value=2023)
        month = st.number_input("Month", min_value=1, max_value=12, value=1)
        day = st.number_input("Day", min_value=1, max_value=31, value=1)
        hour = st.number_input("Hour", min_value=0, max_value=23, value=0)
        minute = st.number_input("Minute", min_value=0, max_value=59, value=0)
        second = st.number_input("Second", min_value=0, max_value=59, value=0)
        latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=0.0)
        longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=0.0)
        ayanamsa = st.selectbox("Ayanamsa", ["Lahiri", "Krishnamurti"])
        house_system = st.selectbox("House System", ["Equal", "Placidus"])

        submit_button = st.form_submit_button(label="Get Horoscope Data")

    if submit_button:
        data = get_horoscope_data(year, month, day, hour, minute, second, latitude, longitude, ayanamsa, house_system)
        st.json(data)

if __name__ == "__main__":
    main()
