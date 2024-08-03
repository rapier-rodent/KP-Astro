import streamlit as st
from vedicastrology import Chart

def main():
    st.title("Vedic Astrology App")

    # Input for birth details
    date_of_birth = st.date_input("Date of Birth")
    time_of_birth = st.time_input("Time of Birth")
    place_of_birth = st.text_input("Place of Birth")

    if st.button("Generate Chart"):
        # Generate chart using vedicastrology library
        # Example usage, adjust according to the actual API
        chart = Chart(date_of_birth, time_of_birth, place_of_birth)

        st.write("Your Vedic Astrology Chart")
        st.write(chart)

if __name__ == "__main__":
    main()
