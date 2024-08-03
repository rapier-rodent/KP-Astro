import streamlit as st
from datetime import datetime
from vedicastro import VedicAstro, horary_chart

def generate_chart(year, month, day, hour, minute, second, latitude, longitude, ayanamsa, house_system):
    try:
        horoscope = VedicAstro.VedicHoroscopeData(year, month, day, hour, minute, second, latitude, longitude, ayanamsa, house_system)
        chart = horoscope.generate_chart()
        planets_data = horoscope.get_planets_data_from_chart(chart)
        houses_data = horoscope.get_houses_data_from_chart(chart)
        planet_significators = horoscope.get_planet_wise_significators(planets_data, houses_data)
        planetary_aspects = horoscope.get_planetary_aspects(chart)
        house_significators = horoscope.get_house_wise_significators(planets_data, houses_data)
        vimshottari_dasa_table = horoscope.compute_vimshottari_dasa(chart)
        consolidated_chart_data = horoscope.get_consolidated_chart_data(planets_data=planets_data, houses_data=houses_data)
        
        return {
            "planets_data": [planet._asdict() for planet in planets_data],
            "houses_data": [house._asdict() for house in houses_data],
            "planet_significators": planet_significators,
            "planetary_aspects": planetary_aspects,
            "house_significators": house_significators,
            "vimshottari_dasa_table": vimshottari_dasa_table,
            "consolidated_chart_data": consolidated_chart_data
        }
    except Exception as e:
        st.error(f"Error generating chart: {e}")
        return None

def generate_horary_chart(year, month, day, hour, minute, second, latitude, longitude, horary_number, ayanamsa, house_system):
    try:
        matched_time, vhd_hora_houses_chart, houses_data = horary_chart.find_exact_ascendant_time(year, month, day, latitude, longitude, horary_number, ayanamsa)
        vhd_hora = VedicAstro.VedicHoroscopeData(year, month, day, hour, minute, second, latitude, longitude, ayanamsa, house_system)
        vhd_hora_planets_chart = vhd_hora.generate_chart()
        planets_data = vhd_hora.get_planets_data_from_chart(vhd_hora_planets_chart, vhd_hora_houses_chart)
        planet_significators = vhd_hora.get_planet_wise_significators(planets_data, houses_data)
        planetary_aspects = vhd_hora.get_planetary_aspects(vhd_hora_planets_chart)
        house_significators = vhd_hora.get_house_wise_significators(planets_data, houses_data)
        vimshottari_dasa_table = vhd_hora.compute_vimshottari_dasa(vhd_hora_planets_chart)
        consolidated_chart_data = vhd_hora.get_consolidated_chart_data(planets_data=planets_data, houses=houses_data)
        
        return {
            "planets_data": [planet._asdict() for planet in planets_data],
            "houses_data": [house._asdict() for house in houses_data],
            "planet_significators": planet_significators,
            "planetary_aspects": planetary_aspects,
            "house_significators": house_significators,
            "vimshottari_dasa_table": vimshottari_dasa_table,
            "consolidated_chart_data": consolidated_chart_data
        }
    except Exception as e:
        st.error(f"Error generating horary chart: {e}")
        return None

def main():
    st.title("Vedic Astrology App")

    # Input for birth details
    st.sidebar.header("Birth Details")
    date_of_birth = st.sidebar.date_input("Date of Birth", datetime.now())
    hour = st.sidebar.number_input("Hour", min_value=0, max_value=23, value=datetime.now().hour)
    minute = st.sidebar.number_input("Minute", min_value=0, max_value=59, value=datetime.now().minute)
    second = st.sidebar.number_input("Second", min_value=0, max_value=59, value=datetime.now().second)
    latitude = st.sidebar.number_input("Latitude", value=0.0)
    longitude = st.sidebar.number_input("Longitude", value=0.0)
    ayanamsa = st.sidebar.selectbox("Ayanamsa", ["Lahiri", "Krishnamurti"])
    house_system = st.sidebar.selectbox("House System", ["Equal", "Placidus"])

    year = date_of_birth.year
    month = date_of_birth.month
    day = date_of_birth.day

    if st.sidebar.button("Generate Chart"):
        data = generate_chart(year, month, day, hour, minute, second, latitude, longitude, ayanamsa, house_system)
        if data:
            st.write("Horoscope Data:", data)

    st.sidebar.header("Horary Details")
    horary_number = st.sidebar.number_input("Horary Number", value=0)

    if st.sidebar.button("Generate Horary Chart"):
        horary_data = generate_horary_chart(year, month, day, hour, minute, second, latitude, longitude, horary_number, ayanamsa, house_system)
        if horary_data:
            st.write("Horary Data:", horary_data)

if __name__ == "__main__":
    main()
