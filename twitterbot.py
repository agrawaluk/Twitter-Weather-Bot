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
weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}"
response = requests.get(weather_url)

weather_data = response.json()
temperature = round(weather_data["main"]["temp"] - 273.15, 1)
description = weather_data["weather"][0]["description"].capitalize()
data = {"text": f"Good morning Nagpur! Current weather is {temperature}°C and {description}."}

# Send POST request to create a new tweet

response = requests.post(url, headers=headers, data=json.dumps(data), auth=auth)

# Print response information
print("Response status code:", response.status_code)
print("Response JSON:", response.json())
