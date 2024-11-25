import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 40.71,
    "longitude": 74.00,
    "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "showers", "snowfall", "snow_depth",
               "weather_code", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility",
               "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "is_day", "sunshine_duration"],
    "forecast_days": 1
}
responses = openmeteo.weather_api(url, params=params)

# Save response as json
# with open("response.json", "w") as f:
#     f.write(responses[0].json())

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s.py")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
hourly_rain = hourly.Variables(3).ValuesAsNumpy()
hourly_showers = hourly.Variables(4).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(5).ValuesAsNumpy()
hourly_snow_depth = hourly.Variables(6).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(7).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(8).ValuesAsNumpy()
hourly_cloud_cover_low = hourly.Variables(9).ValuesAsNumpy()
hourly_cloud_cover_mid = hourly.Variables(10).ValuesAsNumpy()
hourly_cloud_cover_high = hourly.Variables(11).ValuesAsNumpy()
hourly_visibility = hourly.Variables(12).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(13).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(14).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(15).ValuesAsNumpy()
hourly_is_day = hourly.Variables(16).ValuesAsNumpy()
hourly_sunshine_duration = hourly.Variables(17).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s.py", utc=True),
    end=pd.to_datetime(hourly.TimeEnd(), unit="s.py", utc=True),
    freq=pd.Timedelta(seconds=hourly.Interval()),
    inclusive="left"
), "temperature_2m": hourly_temperature_2m, "relative_humidity_2m": hourly_relative_humidity_2m,
    "precipitation": hourly_precipitation, "rain": hourly_rain, "showers": hourly_showers, "snowfall": hourly_snowfall,
    "snow_depth": hourly_snow_depth, "weather_code": hourly_weather_code, "cloud_cover": hourly_cloud_cover,
    "cloud_cover_low": hourly_cloud_cover_low, "cloud_cover_mid": hourly_cloud_cover_mid,
    "cloud_cover_high": hourly_cloud_cover_high, "visibility": hourly_visibility,
    "wind_speed_10m": hourly_wind_speed_10m, "wind_direction_10m": hourly_wind_direction_10m,
    "wind_gusts_10m": hourly_wind_gusts_10m, "is_day": hourly_is_day, "sunshine_duration": hourly_sunshine_duration}

hourly_dataframe = pd.DataFrame(data=hourly_data)
hourly_dataframe.to_csv("hourly_data.csv", index=False)
df_json = hourly_dataframe.to_json()
with open("hourly_data.json", "w") as f:
    f.write(df_json)