
import streamlit as st
import requests

def get_weather(location):
    api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Your API key
    # Construct URL exactly like the curl command
    url = f'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=OuHALnEfV5NQqakA7FbrAxv4ladrumiE'
    
    try:
        response = requests.get(url)
        # Let's print the full response to see what we're getting
        st.write("Debug - API Response:", response.json())
        
        data = response.json()
        
        # Check if we have an error message
        if 'code' in data:
            st.write(f"Debug - API Error Code: {data['code']}")
            st.write(f"Debug - API Error Message: {data.get('message', 'No message provided')}")
            return None
            
        current_weather = data['data']['timelines'][0]['intervals'][0]['values']
        return {
            'temperature': current_weather['temperature'],
            'precipitationProbability': current_weather['precipitationProbability']
        }
    except Exception as e:
        st.write(f"Debug - Full Error: {str(e)}")
        return None

# Rest of your code stays the same...
