# earth pictures from nasa epic cam 

import requests
import random
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# Replace YOUR_API_KEY_HERE with your actual API key
API_KEY = 'your-api-key'
URL = f'https://api.nasa.gov/EPIC/api/natural?api_key={API_KEY}'

# Make a GET request to fetch the available images
URL = 'https://epic.gsfc.nasa.gov/api/natural'
response = requests.get(URL)

if response.status_code == 200:
    # Parse the JSON response
    images = response.json()
    
    # Select a random image
    selected_image = random.choice(images)
    date = selected_image['date'].split(' ')[0].replace('-', '/')
    image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{date}/png/{selected_image['image']}.png"
    
    # Fetch the image
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    
    # Display the image
    plt.imshow(img)
    plt.axis('off') # To hide the axis
    plt.show()

    print(f"Date: {selected_image['date']}")
    print(f"Caption: {selected_image['caption']}")
else:
    print(f"Error fetching images from EPIC camera, status code: {response.status_code}")
