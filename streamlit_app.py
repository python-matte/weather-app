import streamlit as st
import requests

# Function to retrieve weather data
def get_weather(location):
    api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Replace with your valid API key
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        # Handle non-200 status codes
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
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
        return None

# Streamlit App
def main():
    st.title("Camping Weather Assistant Bot")
    
    # User input: Coordinates
    location = st.text_input("Enter location coordinates (latitude,longitude):", "42.3478,-71.0466")
    
    if st.button("Get Weather"):
        if not validate_coordinates(location):
            st.error("Invalid coordinates. Please use the format: latitude,longitude (e.g., 42.3478,-71.0466).")
        else:
            st.write("Fetching weather data...")
            weather = get_weather(location)
            
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

# Validate input coordinates
def validate_coordinates(location):
    try:
        lat, lon = map(float, location.split(","))
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except ValueError:
        return False

if __name__ == "__main__":
    main()
