# retrieving nasa astronomy picture of the day, useful script to download a daily magnificent wall paper if integrated with cron

import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

API_KEY = 'your-api-key'
URL = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}'

# Make a GET request to fetch the APOD
response = requests.get(URL)

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    image_url = data['url']
    
    print(f"Title: {data['title']}")
    print(f"Date: {data['date']}")
    print(f"Explanation: {data['explanation']}")
    
    # Fetch the image
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    
    # Display the image
    plt.imshow(img)
    plt.axis('off') # To hide the axis
    plt.show()
else:
    print(f"Error fetching APOD, status code: {response.status_code}")
