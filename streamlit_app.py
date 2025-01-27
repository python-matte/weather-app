
import streamlit as st
import requests

def get_weather(location):
    api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Your API key
    # Construct URL exactly like the curl command
    url = f'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=OuHALnEfV5NQqakA7FbrAxv4ladrumiE'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Get just the first timeframe's data (current forecast)
        current_weather = data['data']['timelines'][0]['intervals'][0]['values']
        
        # Extract only temperature and precipitation probability
        return {
            'temperature': current_weather['temperature'],
            'precipitationProbability': current_weather['precipitationProbability']
        }
    except Exception as e:
        st.write(f"Debug: Error - {str(e)}")
        return None

st.title("🏕️ Camping Weather Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Hi! I'm your camping weather assistant! 👋 Enter coordinates (like '42.3478,-71.0466')"}
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
        if any(word in user_input.lower() for word in ["hey", "hello", "hi"]):
            response = "Hello camper! Please enter coordinates (like '42.3478,-71.0466') 🌍"
        else:
            try:
                weather_data = get_weather(user_input)
                
                if weather_data:
                    temp = weather_data['temperature']
                    rain_chance = weather_data['precipitationProbability']
                    
                    response = f"📍 Weather forecast:\n\n"
                    response += f"🌡️ Temperature: {temp}°C\n"
                    response += f"🌧️ Chance of rain: {rain_chance}%\n\n"
                    
                    # Add camping advice based on conditions
                    if rain_chance > 50:
                        response += "⚠️ High chance of rain! Make sure to bring waterproof gear! ⛺"
                    elif temp < 10:
                        response += "🥶 It's going to be cold! Bring warm sleeping bags!"
                    elif temp > 30:
                        response += "🌞 It's going to be hot! Bring plenty of water and sun protection!"
                    else:
                        response += "👍 Looks like good camping weather!"
                else:
                    response = "Sorry, I couldn't get the weather data. Please try again."
            except Exception as e:
                response = f"Oops! Something went wrong. Please try again."
                st.write(f"Debug error: {str(e)}")

        st.write(response)
        st.session_state.messages.append({"role": "bot", "content": response})

