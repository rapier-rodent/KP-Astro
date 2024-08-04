import streamlit as st
from vedicastro import VedicAstro

# Title of the app
st.title("Vedic Astrology Chart Generator")

# Input fields for user data
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

# Button to generate horoscope
if st.button("Generate Horoscope"):
    # Create VedicAstro object and generate chart
    horoscope = VedicAstro.VedicHoroscopeData(year, month, day, hour, minute, second, utc, latitude, longitude, ayanamsa, house_system)
    chart = horoscope.generate_chart()
    
    # Display the results
    st.write("Generated Chart Data:")
    st.json(chart)  # Display chart data in JSON format
