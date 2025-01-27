import streamlit as st
import requests

def get_weather(city):
    api_key = "1b3124725b1ab859ef38f754c546a1c7"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

st.title("☔ Simple Weather Bot for Campers")
st.write("I can tell you the current weather for any city. Just type a city name below!")

# Add clear instructions
st.write("### What I can do:")
st.write("✅ Tell you the current temperature")
st.write("✅ Tell you if it's raining, sunny, cloudy, etc.")
st.write("✅ Show current weather conditions")

st.write("### What I cannot do:")
st.write("❌ Give travel advice")
st.write("❌ Recommend camping spots")
st.write("❌ Predict future weather")

city = st.text_input("Enter a city name:")

if city:
    try:
        weather_data = get_weather(city)
        if weather_data.get("main"):
            temp = weather_data["main"]["temp"]
            weather_desc = weather_data["weather"][0]["description"]
            
            st.write(f"### Weather in {city}:")
            st.write(f"🌡️ Temperature: {temp}°C")
            st.write(f"🌤️ Conditions: {weather_desc}")
        else:
            st.error("City not found. Please check the spelling.")
    except:
        st.error("Sorry, there was an error. Please try again.")

# Add a note at the bottom
st.write("---")
st.write("Note: For travel advice, please consult travel websites or local tourism offices.")
