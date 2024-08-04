import streamlit as st
from vedicastro.chart import Chart
from vedicastro.settings import Settings
from vedicastro.time import to_utc_offset

# Constants
UTC_OFFSET = -5.5  # UTC offset for IST (-05:30)

def calculate_horoscope(year, month, day, hour, minute, second, latitude, longitude):
    # Convert local time to UTC
    utc_offset = to_utc_offset(UTC_OFFSET)
    
    # Create settings
    settings = Settings(ayanamsa="Lahiri", house_system="Equal")
    
    # Generate the chart
    chart = Chart(year, month, day, hour, minute, second, utc_offset, latitude, longitude, settings)
    
    # Get planet positions (assuming `get_planet_positions` is the correct method)
    planet_positions = chart.get_planet_positions()
    
    return planet_positions

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

        submit_button = st.form_submit_button(label="Get Horoscope Data")

    if submit_button:
        data = calculate_horoscope(year, month, day, hour, minute, second, latitude, longitude)
        st.json(data)

if __name__ == "__main__":
    main()
