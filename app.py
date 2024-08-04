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
        
        # Add copy and download options at the top of the output
        st.markdown("### Options")
        
        # Button to copy chart data to clipboard
        if st.button("Copy Chart Data"):
            # Show a text area with the chart data for manual copying
            st.text_area("Chart Data (Copy this):", str(chart_data), height=300)
        
        # Button to download chart data as CSV
        csv_data = convert_to_csv(chart_data)
        st.download_button(
            label="Download Chart Data as CSV",
            data=csv_data,
            file_name="chart_data.csv",
            mime="text/csv",
            key="download-csv"  # Unique key to prevent caching issues
        )
        
        # Display generated chart data
        st.write("Generated Chart Data:")
        st.json(chart_data)  # Display the chart data in a readable format
        
        # Display additional information
        st.write("Birth Time (IST):", chart_data.get("birth_time_ist"))
        st.write("Ayanamsa Value:", chart_data.get("ayanamsa_value"))
    else:
        error_data = response.json()
        st.error(f"Error generating chart data. Status code: {response.status_code}")
        st.write("Error message:", error_data.get("error"))
        st.write("Details:", error_data.get("details"))

def convert_to_csv(data):
    """Converts the chart data dictionary to CSV format."""
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    # Write the header
    writer.writerow(data.keys())
    
    # Write the data
    writer.writerow(data.values())
    
    return csv_buffer.getvalue()
