import streamlit as st
import requests

# Function to fetch weather data
def get_weather(location):
    api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Your Tomorrow.io API key
    url = "https://api.tomorrow.io/v4/weather/realtime"
    params = {
        "location": location,
        "units": "metric",  # Ensure data is in Celsius
        "apikey": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        
        # Debugging: Log the API response to identify issues
        st.write(f"Debug - Full API Response: {data}")
        
        # Extract temperature
        temperature = data.get('data', {}).get('values', {}).get('temperature')
        return temperature
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

# Streamlit app
def main():
    st.set_page_config(page_title="Weather Buddy", page_icon="☀️")
    st.title("Your Fabulous Weather Buddy! 🌤️")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    if prompt := st.chat_input("Type a location (e.g., 'Boston, USA') and I'll fetch the weather for you! 🌈"):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Fetch weather data
        with st.chat_message("assistant"):
            with st.spinner("Fetching the latest weather..."):
                temperature = get_weather(prompt)
                if temperature is not None:
                    response = (
                        f"✨ The current temperature in **{prompt}** is **{temperature}°C**. "
                        "Don't forget your shades, babe! 😎☀️"
                    )
                else:
                    response = (
                        "Oops, I couldn't fetch the weather for that location. "
                        "Maybe double-check the name and try again? 🧐"
                    )
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
