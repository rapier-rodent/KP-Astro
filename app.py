import streamlit as st
from vedicastro import Chart  # Assuming `Chart` is a class from `vedicastro`

def main():
    st.title("Vedic Astrology App")

    # Input for birth details
    date_of_birth = st.date_input("Date of Birth")
    time_of_birth = st.time_input("Time of Birth")
    place_of_birth = st.text_input("Place of Birth")

    if st.button("Generate Chart"):
        # Generate chart using vedicastro library
        # Example usage, adjust according to the actual API
        try:
            chart = Chart(date_of_birth, time_of_birth, place_of_birth)
            st.write("Your Vedic Astrology Chart:")
            st.write(chart)
        except Exception as e:
            st.error(f"Error generating chart: {e}")

if __name__ == "__main__":
    main()
