import streamlit as st
import requests
import time

def get_weather(city):
    # Tomorrow.io API settings
    api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Replace with your Tomorrow.io API key
    curl --request GET --url 'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=OuHALnEfV5NQqakA7FbrAxv4ladrumiE'
    
    # Parameters for the API request
    params = {
        "location": city,
        "apikey": api_key
    }
    
    response = requests.get(url, params=params)
    return response.json()

st.title("🏕️ Camping Weather Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Hi! I'm your camping weather assistant! 👋 What city are you planning to camp in?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Your message...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Bot response
    with st.chat_message("bot"):
        if "bye" in user_input.lower():
            response = "Goodbye! Happy camping! ⛺"
        elif "thank" in user_input.lower():
            response = "You're welcome! Need any other weather info? 😊"
        elif "hello" in user_input.lower() or "hi" in user_input.lower():
            response = "Hello camper! Which city's weather would you like to check? 🌍"
        else:
            try:
                weather_data = get_weather(user_input)
                
                if weather_data.get("data"):
                    values = weather_data["data"]["values"]
                    temp = values["temperature"]
                    humidity = values["humidity"]
                    wind_speed = values["windSpeed"]
                    precipitation = values["precipitationProbability"]
                    
                    response = f"📍 Current Weather in {user_input}:\n\n"
                    response += f"🌡️ Temperature: {temp}°C\n"
                    response += f"💨 Wind Speed: {wind_speed} m/s\n"
                    response += f"💧 Humidity: {humidity}%\n"
                    response += f"🌧️ Chance of Rain: {precipitation}%\n\n"
                    
                    # Camping advice based on conditions
                    if precipitation > 50:
                        response += "⚠️ High chance of rain! Make sure your tent is waterproof!"
                    elif wind_speed > 20:
                        response += "⚠️ It's quite windy! Secure your tent well!"
                    elif temp < 10:
                        response += "🥶 It's cold! Bring a warm sleeping bag!"
                    elif temp > 30:
                        response += "🌞 It's hot! Bring plenty of water and sun protection!"
                    else:
                        response += "👍 Looks like good camping weather!"
                    
                    response += "\n\nWould you like to check another city?"
                else:
                    response = "I couldn't find that city. Could you please check the spelling and try again? 🤔"
            except Exception as e:
                response = "Oops! Something went wrong. Please try again with a different city name. 😅"

        st.write(response)
        st.session_state.messages.append({"role": "bot", "content": response})

# Add helpful instructions at the bottom
with st.expander("ℹ️ How to use this bot"):
    st.write("""
    - Type a city name to get current weather
    - Say 'hi' or 'hello' to start over
    - Say 'bye' to end conversation
    - Type 'thank you' for a polite response
    
    The bot will give you weather details and camping-specific advice!
    """)
