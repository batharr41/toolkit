import requests
import socket
from dotenv import load_dotenv
import os
import datetime as dt

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("API_KEY")
print("API_KET", OPENWEATHER_API_KEY)

# --- CONFIGURATION ---
IP_GEOLOCATION_URL = "http://ip-api.com/json/"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Map OpenWeather codes to simple emojis/icons
WEATHER_ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌧️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
}


def get_icon_url(icon_code: str, scale: str = "@2x") -> str:
    """Constructs the full OpenWeatherMap icon URL."""
    base_path = "https://openweathermap.org/img/wn/"
    return f"{base_path}{icon_code}{scale}.png"


def fetch_weather_forecast(CITY_NAME: str):
    """
    Fetches a 5-day forecast from OpenWeatherMap API and formats it.
    Returns:
        list: A list of dicts structured like the forecast_data example.
    """

    params = {
        "q": CITY_NAME,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  # for Celsius
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # 1. Group the 3-hour forecasts by day
        daily_data = {}
        for item in data["list"]:
            timestamp = item["dt"]
            date = dt.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            temp = item["main"]["temp"]

            # The 'main' weather description is used for the icon
            weather_main = item["weather"][0]["main"]
            weather_icon_code = item["weather"][0]["icon"]
            if date not in daily_data:
                daily_data[date] = {
                    "temps": [],
                    "weather_main": weather_main,
                    "icon_code": weather_icon_code,
                    "dt": dt.datetime.fromtimestamp(timestamp),
                }
            daily_data[date]["temps"].append(temp)

            # We update the icon based on the last observed weather for the day
            daily_data[date]["weather_main"] = weather_main
            daily_data[date]["icon_code"] = weather_icon_code

        # 2. Format the data for the next 5 days
        formatted_forecast = []
        for i, (date_str, daily_info) in enumerate(list(daily_data.items())[:5]):
            if i == 0 and daily_info["dt"].day == dt.datetime.now().day:
                # Skip the current day if we only want full future days,
                # or include it for a full 5-day block starting today
                day_name = "Today"
            else:
                day_name = daily_info["dt"].strftime("%a")

            # Calculate High and Low for the day
            high = max(daily_info["temps"])
            low = min(daily_info["temps"])

            # Determine the icon
            icon = WEATHER_ICONS.get(daily_info["weather_main"], "❓")
            owm_icon_code = daily_info["icon_code"]
            icon_url = get_icon_url(owm_icon_code)  # <-- NEW: Generate the URL

            formatted_forecast.append(
                {
                    "day": day_name,
                    "icon": icon,
                    "high": f"{round(high)}°",
                    "low": f"{round(low)}°",
                    "icon_url": icon_url,
                    "icon_code": owm_icon_code,
                    "weather_main": weather_main,
                }
            )

        return formatted_forecast

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return []


def get_local_ip():
    """Attempts to get the local (internal) IP address."""
    try:
        # Create a socket connection to an external address (doesn't send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Use a reliable public DNS for connection check
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "N/A"


def fetch_network_details():
    """
    Fetches public network data (Public IP, Location, ISP) using an API.

    Returns:
        dict: A dictionary structured like the network_data example.
    """

    # 1. Get Public IP, Location, and ISP from the API
    try:
        response = requests.get(IP_GEOLOCATION_URL)
        response.raise_for_status()
        public_data = response.json()

        if public_data.get("status") == "success":
            public_ip = public_data.get("query", "N/A")
            location = (
                f"{public_data.get('city', 'N/A')}, {public_data.get('country', 'N/A')}"
            )
            isp = public_data.get("isp", "N/A")
        else:
            public_ip = "N/A"
            location = "N/A"
            isp = "N/A"
            print(f"API Error: {public_data.get('message', 'Unknown API Error')}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching public network data: {e}")
        public_ip = "N/A"
        location = "N/A"
        isp = "N/A"

    # 2. Get Local IP
    local_ip = get_local_ip()

    # 3. Compile final dictionary
    network_data = {
        "ip_address": local_ip,
        "location": location,
        "isp": isp,
        "public_ip": public_ip,
    }

    return network_data


def get_network_and_forecast():
    network_data = fetch_network_details()
    wf = fetch_weather_forecast(network_data["location"])
    return (network_data, wf)


if __name__ == "__main__":
    # Example of how to call this helper:
    data = get_network_and_forecast()
    print("Data", data)
