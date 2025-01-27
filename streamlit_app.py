
import streamlit as st
import requests

def get_weather(location):
    api_key = "OuHALnEfV5NQqakA7FbrAxv4ladrumiE"  # Your API key
    # Construct URL exactly like the curl command
    url = f'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=OuHALnEfV5NQqakA7FbrAxv4ladrumiE'
    
    try:
        st.write("Debug: Making API call...")
        response = requests.get(url)
        st.write(f"Debug: Response status: {response.status_code}")
        return response.json()
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
            response = "Hello! Please enter coordinates (like '42.3478,-71.0466') 🌍"
        else:
            try:
                weather_data = get_weather(user_input)
                st.write("Debug: Weather data received:", weather_data)  # Debug line
                
                if weather_data and 'data' in weather_data:
                    # Extract weather info from response
                    timelines = weather_data['data']['timelines'][0]['intervals'][0]['values']
                    temp = timelines['temperature']
                    humidity = timelines['humidity']
                    
                    response = f"📍 Weather for location {user_input}:\n"
                    response += f"🌡️ Temperature: {temp}°C\n"
                    response += f"💧 Humidity: {humidity}%\n"
                else:
                    response = "Sorry, I couldn't get the weather data. Please try again."
            except Exception as e:
                response = f"Oops! Something went wrong. Please try again."
                st.write(f"Debug error: {str(e)}")

        st.write(response)
        st.session_state.messages.append({"role": "bot", "content": response})

# Add debug expander
with st.expander("🔍 Debug Information"):
    st.write("Try entering coordinates exactly like this: 42.3478,-71.0466")
