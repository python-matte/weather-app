import streamlit as st
import requests

# Function to get latitude and longitude from a location name
def get_coordinates(location_name):
    # Replace with your preferred geocoding API (e.g., Tomorrow.io or OpenCage/Google Geocoding)
    geocoding_api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Replace with your API key
    geocoding_url = f"https://api.tomorrow.io/v4/geocode"
    
    try:
        response = requests.get(
            geocoding_url,
            params={"location": location_name, "apikey": geocoding_api_key}
        )
        
        if response.status_code != 200:
            st.error(f"Geocoding Error: {response.status_code} - {response.reason}")
            return None
        
        data = response.json()
        if "location" not in data or not data["location"]:
            st.error(f"Could not find coordinates for '{location_name}'. Please check the spelling.")
            return None
        
        return data["location"]["lat"], data["location"]["lon"]
    except requests.exceptions.RequestException as e:
        st.error(f"Request Error: {str(e)}")
        return None

# Function to retrieve weather data
def get_weather(lat, lon):
    weather_api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Replace with your valid API key
    weather_url = f"https://api.tomorrow.io/v4/weather/forecast"
    
    try:
        response = requests.get(
            weather_url,
            params={"location": f"{lat},{lon}", "apikey": weather_api_key}
        )
        
        if response.status_code != 200:
            st.error(f"API Error: {response.status_code} - {response.reason}")
            return None
        
        data = response.json()
        
        # Validate the response structure
        if 'data' not in data or 'timelines' not in data['data']:
            st.error("Unexpected API response structure. Please check the API documentation.")
            return None
        
        # Extract relevant fields
        try:
            current_weather = data['data']['timelines'][0]['intervals'][0]['values']
            return {
                'temperature': current_weather.get('temperature', 'N/A'),
                'precipitationProbability': current_weather.get('precipitationProbability', 'N/A')
            }
        except (IndexError, KeyError):
            st.error("Failed to extract weather details. Check the API response format.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request Error: {str(e)}")
        return None

# Streamlit App
def main():
    st.title("Camping Weather Assistant Bot")
    
    # User input: Location name
    location_name = st.text_input("Enter a location (e.g., 'Berlin, Germany'):")
    
    if st.button("Get Weather"):
        if not location_name:
            st.error("Please enter a location.")
        else:
            st.write("Fetching location coordinates...")
            coordinates = get_coordinates(location_name)
            
            if coordinates:
                lat, lon = coordinates
                st.write(f"Location found: Latitude {lat}, Longitude {lon}")
                
                st.write("Fetching weather data...")
                weather = get_weather(lat, lon)
                
                if weather:
                    st.success("Weather data retrieved successfully!")
                    st.write(f"**Temperature:** {weather['temperature']} °C")
                    st.write(f"**Chance of Rain:** {weather['precipitationProbability']} %")
                    
                    # Camping-specific advice
                    if weather['precipitationProbability'] > 50:
                        st.info("Camping Tip: Bring waterproof gear!")
                    else:
                        st.info("Camping Tip: Clear skies! Enjoy your trip!")
                else:
                    st.error("Failed to retrieve weather data. Please try again.")
            else:
                st.error("Could not determine location coordinates. Please try another location.")

if __name__ == "__main__":
    main()
