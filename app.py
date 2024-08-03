import streamlit as st
import os
import swisseph as swe

# Set the path to the ephemeris data directory
swe.set_ephe_path(os.path.join(os.path.dirname(__file__), 'ephe')) 
from vedicastro import VedicAstro, horary_chart
from datetime import datetime, time

# Set page title
st.set_page_config(page_title="Vedic Astrology App")

# Input widgets
st.title("Vedic Astrology Chart Calculator")

# Chart type selection
chart_type = st.radio("Select Chart Type:", ["Natal Chart", "Horary Chart"])

# Date input (allowing any date)
birth_date = st.date_input("Enter your birth date:")

# Time input (allowing any time with seconds)
birth_hour = st.number_input("Hour:", min_value=0, max_value=23, step=1, value=datetime.now().hour)
birth_minute = st.number_input("Minute:", min_value=0, max_value=59, step=1, value=datetime.now().minute)
birth_second = st.number_input("Second:", min_value=0, max_value=59, step=1, value=datetime.now().second)
birth_time = time(birth_hour, birth_minute, birth_second)

# Location input
st.subheader("Location Details")
latitude = st.number_input("Latitude:", value=28.6334)
longitude = st.number_input("Longitude:", value=77.2834)
utc_offset = st.text_input("UTC Offset:", value="+5:30")

# Ayanamsa selection
ayanamsa = st.selectbox("Select Ayanamsa:", ["Lahiri", "Krishnamurti", "Krishnamurti_Senthilathiban"])

# Horary number input (only if Horary Chart is selected)
if chart_type == "Horary Chart":
    horary_number = st.number_input("Horary Number:", min_value=1, max_value=249, step=1)
else:
    horary_number = None

# Calculate chart data
if st.button("Calculate Chart"):
    if chart_type == "Horary Chart":
        # Calculate horary chart
        matched_time, _, houses_data = horary_chart.find_exact_ascendant_time(
            birth_date.year, birth_date.month, birth_date.day, utc_offset,
            latitude, longitude, horary_number, ayanamsa
        )
        birth_time = matched_time.time()  # Update birth time with matched time
        vhd = VedicAstro.VedicHoroscopeData(
            birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute, birth_time.second,
            utc_offset, latitude, longitude, ayanamsa, "Placidus"
        )
        chart = vhd.generate_chart()
        planets_data = vhd.get_planets_data_from_chart(chart)
    else:
        # Calculate birth chart
        vhd = VedicAstro.VedicHoroscopeData(
            birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute, birth_time.second,
            utc_offset, latitude, longitude, ayanamsa, "Placidus"
        )
        chart = vhd.generate_chart()
        planets_data = vhd.get_planets_data_from_chart(chart)
        houses_data = vhd.get_houses_data_from_chart(chart)

    # Display results
    st.subheader("Chart Data")
    st.write(f"Chart Type: {chart_type}")
    st.write(f"Ayanamsa: {ayanamsa}")
    st.write(f"Ayanamsa Value: {vhd.get_ayanamsa()}")  # Display Ayanamsa value

    st.subheader("Planetary Positions:")
    st.dataframe(planets_data)

    st.subheader("House Cusps:")
    st.dataframe(houses_data)

    st.subheader("Vimshottari Dasa:")
    st.write(vhd.compute_vimshottari_dasa(chart))

    st.subheader("Planet Significators:")
    st.dataframe(vhd.get_planet_wise_significators(planets_data, houses_data))

    st.subheader("House Significators:")
    st.dataframe(vhd.get_house_wise_significators(planets_data, houses_data))

    st.subheader("Planetary Aspects:")
    st.dataframe(vhd.get_planetary_aspects(chart))
