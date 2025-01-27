import streamlit as st
import requests

# Function to get latitude and longitude from a location name
def get_coordinates(location_name):
    # Using Tomorrow.io's geocoding API or other geocoding service
    geocoding_url = f"https://api.tomorrow.io/v4/timelines?apikey=OuHALnEfV5NQqakA7FbrAxv4ladrumiE"
    try:
        response = requests.get(
            geocoding_url,
            params={"location": location_name}
        )
        if response.status_code != 200:
            st.error(f"Geocoding Error: {response.status_code} - {response.reason}")
            return None
        
        data = response.json()
        if not data or "location" not in data:
  Handling None"+retry.annotate anything issue`:")
        
  Reminder please web
