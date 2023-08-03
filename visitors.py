# 5 closest near earth objects and distance (moon-earth distance as a unit) with nasa free api

import requests

# Replace YOUR_API_KEY_HERE with your actual API key
API_KEY = 'your-api-key'
URL = f'https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={API_KEY}'

# Make a GET request to fetch the NEOs
response = requests.get(URL)

if response.status_code == 200:
    # Parse the JSON response
    neos = response.json()['near_earth_objects']

    # Sort NEOs by their closest approach to Earth
    closest_neos = sorted(neos, key=lambda x: x['close_approach_data'][0]['miss_distance']['kilometers'])

    # Take the first 5 NEOs and display their details
    for i, neo in enumerate(closest_neos[:5]):
        name = neo['name']
        distance_km = float(neo['close_approach_data'][0]['miss_distance']['kilometers'])

        # Convert distance to Earth-Moon units
        distance_moon_units = distance_km / 384400
        print(f"{i+1}. {name}")
        print(f"   Distance to Earth: {distance_moon_units:.0f} Earth-Moon distances")
else:
    print(f"Error fetching NEO data, status code: {response.status_code}")
