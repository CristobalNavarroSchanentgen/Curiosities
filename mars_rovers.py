# most of the time it's just damn rocks tho

import requests
import random
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# Replace YOUR_API_KEY_HERE with your actual API key
API_KEY = 'your-api-key'
ROVER_URL = f'https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={API_KEY}'

# Get the list of rovers
response = requests.get(ROVER_URL)
rovers = response.json()['rovers']

# Select a random rover
selected_rover = random.choice(rovers)
rover_name = selected_rover['name']

# Get the maximum Sol for the selected rover
max_sol = selected_rover['max_sol']

# Select a random Sol
selected_sol = random.randint(0, max_sol)

# Fetch photos for the selected rover and Sol
PHOTOS_URL = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos'
params = {
    'sol': selected_sol,
    'api_key': API_KEY
}
response = requests.get(PHOTOS_URL, params=params)
photos = response.json()['photos']

# If there are photos available for the selected Sol, pick a random one
if photos:
    selected_photo = random.choice(photos)
    img_url = selected_photo['img_src']

    # Fetch and display the image
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    plt.imshow(img)
    plt.axis('off')  # To hide the axis
    plt.show()
else:
    print(f"No photos available for rover {rover_name} on Sol {selected_sol}")
