import streamlit as st
from vedicastro import VedicAstro, horary_chart

# Set page title
st.set_page_config(page_title="Vedic Astrology App")

# Input widgets
st.title("Vedic Astrology Chart Calculator")

# Date input
birth_date = st.date_input("Enter your birth date:")

# Time input
birth_time = st.time_input("Enter your birth time:")

# Location input
st.subheader("Location Details")
latitude = st.number_input("Latitude:", value=28.6334)
longitude = st.number_input("Longitude:", value=77.2834)
utc_offset = st.text_input("UTC Offset:", value="+5:30")

# Ayanamsa selection
ayanamsa = st.selectbox("Select Ayanamsa:", ["Lahiri", "Krishnamurti", "Krishnamurti_Senthilathiban"])

# Optional horary number input
horary_number = st.number_input("Horary Number (optional):", min_value=1, max_value=249, step=1)

# Calculate chart data
if st.button("Calculate Chart"):
    if horary_number:
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
