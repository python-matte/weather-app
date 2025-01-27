import streamlit as st
import requests

# Function to fetch weather data
def get_weather(location):
    api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Your Tomorrow.io API key
    url = "https://api.tomorrow.io/v4/weather/realtime"
    params = {"location": location, "apikey": api_key}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        # Extract temperature from the response
        temperature = data.get('data', {}).get('values', {}).get('temperature')
        if temperature is not None:
            return temperature
        else:
            return None
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

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
    if prompt := st.chat_input("Type a location (e.g., 'Berlin, Germany') and I'll fetch the weather for you! 🌈"):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Fetch weather data
        with st.chat_message("assistant"):
            with st.spinner("Fetching the latest weather..."):
                temperature = get_weather(prompt)
                if temperature:
                    response = f"✨ The current temperature in **{prompt}** is **{temperature}°C**. Don't forget your shades, babe! 😎☀️"
                else:
                    response = "Oops, I couldn't fetch the weather for that location. Maybe double-check the name and try again? 🧐"
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
