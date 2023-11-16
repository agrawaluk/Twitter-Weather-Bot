import requests
import json
from requests_oauthlib import OAuth1
import os
from config import twitter_api_keys, openweather_api_key

# Set up OAuth1 authentication
auth = OAuth1(
    twitter_api_keys["consumer_key"],
    twitter_api_keys["consumer_secret"],
    twitter_api_keys["access_token"],
    twitter_api_keys["access_token_secret"]
)

# Set up API endpoint and headers
url = "https://api.twitter.com/2/tweets"
headers = {"User-Agent": "v2FilteredStreamPython", "Content-Type": "application/json", "Accept-Encoding": "gzip"}

# Set up request data

city = "Nagpur"  # Change this to the desired city
forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={openweather_api_key}"
response = requests.get(forecast_url)

forecast_data = response.json()

# Extract relevant weather information
temperature = round(forecast_data["list"][0]["main"]["temp"] - 273.15, 1)
feels_like = round(forecast_data["list"][0]["main"]["feels_like"] - 273.15, 1)
description = forecast_data["list"][0]["weather"][0]["description"]
icon = forecast_data["list"][0]["weather"][0]["icon"]
rain_chance = forecast_data["list"][0]["pop"]*100 
population = round(forecast_data["city"]["population"])
formatted_population = "{:,}".format(population)

# Map weather icons to emoji characters
emoji_mapping = {
    "01d": "☀️",  # Clear sky (day)
    "01n": "🌙",  # Clear sky (night)
    "02d": "⛅",  # Few clouds (day)
    "02n": "🌥️",  # Few clouds (night)
    "03d": "☁️",  # Scattered clouds (day)
    "03n": "☁️",  # Scattered clouds (night)
    "04d": "☁️",  # Broken clouds (day)
    "04n": "☁️",  # Broken clouds (night)
    "09d": "🌧️",  # Shower rain (day)
    "09n": "🌧️",  # Shower rain (night)
    "10d": "🌦️",  # Rain (day)
    "10n": "🌧️",  # Rain (night)
    "11d": "⛈️",  # Thunderstorm (day)
    "11n": "⛈️",  # Thunderstorm (night)
    "13d": "❄️",  # Snow (day)
    "13n": "❄️",  # Snow (night)
    "50d": "🌫️",  # Mist (day)
    "50n": "🌫️",  # Mist (night)
}

emoji = emoji_mapping.get(icon, "🤔")  # Default emoji if icon is not found in the mapping

data = {
    "text": f"Good morning Nagpur!\nCurrent temperature is {temperature}°C, and it feels like {feels_like}°C.\nIt will (be) {description} {emoji} most of the day with chances of rain being {rain_chance}%\nToday's population: {formatted_population}"
}

# Send POST request to create a new tweet
response = requests.post(url, headers=headers, data=json.dumps(data), auth=auth)

# Print response information
print("Response status code:", response.status_code)
print("Response JSON:", response.json())
