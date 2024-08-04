import streamlit as st
import requests
import csv
from io import StringIO

st.title("Vedic Astrology Chart Generator")

# User inputs for horoscope generation
year = st.number_input("Year", min_value=1900, max_value=2100)
month = st.number_input("Month", min_value=1, max_value=12)
day = st.number_input("Day", min_value=1, max_value=31)
hour = st.number_input("Hour (IST)", min_value=0, max_value=23)
minute = st.number_input("Minute (IST)", min_value=0, max_value=59)
second = st.number_input("Second (IST)", min_value=0, max_value=59)
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
        "utc": "+5:30",  # Fixed UTC offset for IST
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
        st.write("Ayanamsa Value:", chart_data.get("ayanamsa_value"))
        
        # Add copy and download options
        st.markdown("### Options")
        if st.button("Copy Chart Data"):
            st.write("Chart data copied to clipboard!")
            st.write(chart_data)
            st.clipboard(str(chart_data))
        
        if st.button("Download Chart Data"):
            st.write("Downloading chart data as CSV...")
            csv_data = convert_to_csv(chart_data)
            st.download_button(
                label="Download data as CSV",
                data=csv_data,
                file_name="chart_data.csv",
                mime="text/csv",
            )
    else:
        error_data = response.json()
        st.error(f"Error generating chart data. Status code: {response.status_code}")
        st.write("Error message:", error_data.get("error"))
        st.write("Details:", error_data.get("details"))

def convert_to_csv(data):
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    # Assuming the chart_data is a dictionary with lists as values
    for key, value in data.items():
        if isinstance(value, list):
            for row in value:
                writer.writerow([key] + row)
        else:
            writer.writerow([key, value])
    
    return csv_buffer.getvalue()
