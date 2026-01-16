#!/usr/bin/env python3
"""
Fetch weather data from OpenWeatherMap API and append to CSV file.
"""

import csv
import os
import sys
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError
import json


def fetch_weather_data(api_url):
    """Fetch weather data from the API."""
    try:
        with urlopen(api_url) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except URLError as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)


def flatten_weather_data(data):
    """Flatten the nested weather data structure."""
    return {
        'timestamp': datetime.now().isoformat(),
        'api_timestamp': data.get('dt'),
        'city_id': data.get('id'),
        'city_name': data.get('name'),
        'country': data.get('sys', {}).get('country'),
        'lat': data.get('coord', {}).get('lat'),
        'lon': data.get('coord', {}).get('lon'),
        'timezone': data.get('timezone'),
        'weather_id': data.get('weather', [{}])[0].get('id'),
        'weather_main': data.get('weather', [{}])[0].get('main'),
        'weather_description': data.get('weather', [{}])[0].get('description'),
        'temp': data.get('main', {}).get('temp'),
        'feels_like': data.get('main', {}).get('feels_like'),
        'temp_min': data.get('main', {}).get('temp_min'),
        'temp_max': data.get('main', {}).get('temp_max'),
        'pressure': data.get('main', {}).get('pressure'),
        'humidity': data.get('main', {}).get('humidity'),
        'sea_level_pressure': data.get('main', {}).get('sea_level'),
        'grnd_level_pressure': data.get('main', {}).get('grnd_level'),
        'visibility': data.get('visibility'),
        'wind_speed': data.get('wind', {}).get('speed'),
        'wind_direction': data.get('wind', {}).get('deg'),
        'clouds_all': data.get('clouds', {}).get('all'),
        'sunrise': data.get('sys', {}).get('sunrise'),
        'sunset': data.get('sys', {}).get('sunset'),
    }


def append_to_csv(data, csv_path='weather_data.csv'):
    """Append weather data to CSV file, creating it with headers if needed."""
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, 'a', newline='') as csvfile:
        fieldnames = [
            'timestamp', 'api_timestamp', 'city_id', 'city_name', 'country',
            'lat', 'lon', 'timezone', 'weather_id', 'weather_main',
            'weather_description', 'temp', 'feels_like', 'temp_min', 'temp_max',
            'pressure', 'humidity', 'sea_level_pressure', 'grnd_level_pressure',
            'visibility', 'wind_speed', 'wind_direction', 'clouds_all',
            'sunrise', 'sunset'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

    print(f"Weather data appended to {csv_path}")


def get_csv_filename(data):
    """Generate CSV filename based on year and coordinates."""
    lat = data.get('lat')
    lon = data.get('lon')
    year = datetime.now().year
    return f'{year}-{lat}-{lon}.csv'


def main():
    # Get API parameters from environment variables
    api_key = os.getenv('WEATHER_API_KEY')
    lat = os.getenv('WEATHER_LAT', '16.0544')
    lon = os.getenv('WEATHER_LON', '108.2022')

    # Construct API URL
    if api_key:
        api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    else:
        # Fallback to hardcoded URL (for local testing)
        api_url = 'https://api.openweathermap.org/data/2.5/weather?lat=16.0544&lon=108.2022&appid=d16c000ae5dc1648b49213b3311a43dd'

    # Fetch weather data
    print("Fetching weather data...")
    weather_data = fetch_weather_data(api_url)

    # Flatten the data
    flat_data = flatten_weather_data(weather_data)

    # Generate CSV filename based on year and coordinates
    csv_path = os.getenv('CSV_OUTPUT_PATH') or get_csv_filename(flat_data)
    append_to_csv(flat_data, csv_path)


if __name__ == '__main__':
    main()
