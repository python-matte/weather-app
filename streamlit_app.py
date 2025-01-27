def get_weather(location_name):
    api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Replace with your API key
    url = f"https://api.tomorrow.io/v4/weather/forecast"
    
    try:
        response = requests.get(
            url,
            params={"location": location_name, "apikey": api_key}
        )
        
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
