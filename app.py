import streamlit as st
from vedicastro import VedicAstro
from flatlib import const, chart
from flatlib.datetime import Datetime

# Constants
UTC_OFFSET = "+00:00"  # Set to UTC since flatlib uses UTC

def calculate_horoscope(year, month, day, hour, minute, second, latitude, longitude, ayanamsa="Lahiri", house_system="Equal"):
    # VedicAstro calculation
    horoscope = VedicAstro.VedicHoroscopeData(
        year=year, 
        month=month, 
        day=day, 
        hour=hour, 
        minute=minute, 
        second=second, 
        utc=UTC_OFFSET, 
        latitude=latitude, 
        longitude=longitude, 
        ayanamsa=ayanamsa, 
        house_system=house_system
    )
    vedic_chart = horoscope.generate_chart()
    vedic_planets_data = horoscope.get_planets_data()
    vedic_houses_data = horoscope.get_houses_data()

    # flatlib calculation
    date_str = f"{year}/{month}/{day} {hour}:{minute}:{second}"
    date_obj = Datetime(date_str, UTC_OFFSET)  # Use UTC offset as needed
    flatlib_chart = chart.Chart(date_obj, latitude, longitude, hsys=const.HOUSES_PLACIDUS if house_system == "Placidus" else const.HOUSES_EQUAL)
    flatlib_planets = {p.id: p for p in flatlib_chart.planets}
    flatlib_houses = {h.id: h for h in flatlib_chart.houses}

    return {
        "vedic_chart": vedic_chart,
        "vedic_planets_data": vedic_planets_data,
        "vedic_houses_data": vedic_houses_data,
        "flatlib_planets": flatlib_planets,
        "flatlib_houses": flatlib_houses
    }

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
        data = calculate_horoscope(year, month, day, hour, minute, second, latitude, longitude, ayanamsa, house_system)
        st.json(data)

if __name__ == "__main__":
    main()
