# Interesting script vor visualization of international relations hot topics
# I really enjoy the world map rendition



## PART 1 : EXTRACTION AND REPORT ##

import requests
from textblob import TextBlob
from collections import defaultdict

# Define the endpoint and parameters
url = 'https://newsapi.org/v2/everything'
parameters = {
    'q': 'international relations OR geopolitics',
    'pageSize': 100,
    'language': 'en',
    'sources': 'bloomberg,financial-times,reuters,the-guardian-uk',
    'domains': 'foreignaffairs.com,foreignpolicy.com',
    'apiKey': 'your-api-key' 
}

# Fetch the news
try:
    response = requests.get(url, params=parameters)
    response.raise_for_status()
    data = response.json()

    if 'articles' not in data:
        print("No articles found in the response")
        exit()

    # Define geographical categories and keywords/phrases
    geographical_categories = {
        'Europe': ['Europe', 'EU', 'European Union'],
        'Southeast Asia': ['Southeast Asia', 'ASEAN'],
        'US-China Tensions': ['US-China', 'Sino-American'],
        'Middle East': ['Middle East', 'Gulf', 'Saudi Arabia', 'Iran', 'Israel', 'Syria'],
        'North America': ['United States', 'Canada', 'Mexico'],
        'South America': ['Brazil', 'Argentina', 'Venezuela'],
        'Africa': ['Africa', 'Nigeria', 'South Africa', 'Egypt'],
        'East Asia': ['Japan', 'Korea', 'China', 'Taiwan'],
        'South Asia': ['India', 'Pakistan', 'Bangladesh', 'Sri Lanka'],
        'Russia': ['Russia', 'Moscow', 'Kremlin'],
        'Ukraine': ['Kiev', 'Zelensky', 'Ukraine'],
        'Australia and Oceania': ['Australia', 'New Zealand', 'Oceania'],
        'US-Russia Relations': ['US-Russia', 'Washington-Moscow'],
        'NATO': ['NATO', 'North Atlantic Treaty Organization'],
        'United Nations': ['United Nations', 'UN'],
        'Global Economy': ['World Bank', 'IMF', 'WTO', 'G20'],
        # Add more categories as needed
    }

    # Initialize a dictionary to store the count of articles and total polarity per category
    category_stats = defaultdict(lambda: {'count': 0, 'total_polarity': 0})

    # Analyzing articles
    for article in data['articles']:
        headline = article['title']
        description = article['description']
        text = headline + ' ' + description
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity

        # Check for geographical keywords/phrases
        for category, keywords in geographical_categories.items():
            if any(keyword in text for keyword in keywords):
                category_stats[category]['count'] += 1
                category_stats[category]['total_polarity'] += sentiment_score

    # Total number of articles
    total_articles = len(data['articles'])

    # Sorting the categories by count in descending order
    sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['count'], reverse=True)

    # Displaying the sorted counts, proportions, and average polarity
    for category, stats in sorted_categories:
        count = stats['count']
        total_polarity = stats['total_polarity']
        average_polarity = total_polarity / count if count > 0 else 0
        proportion = count / total_articles * 100  # Calculate the proportion in percentage
        print(f"{category}: {count} articles ({proportion:.2f}% of total), Average Polarity: {average_polarity:.4f}")


except requests.RequestException as e:
    print(f"An error occurred while fetching the news: {e}")




## PART 2 : WORLD MAP ##

import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from shapely.geometry import Point

# World map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Geolocator to fetch coordinates
geolocator = Nominatim(user_agent="geoapi")

# Creating a Geopandas DataFrame
gdf = gpd.GeoDataFrame(columns=['geometry', 'prevalence'], crs="EPSG:4326")

# Define representative locations for categories
category_locations = {
    'Europe': 'Europe',
    'Southeast Asia': 'Southeast Asia',
    'US-China Tensions': 'China',
    'Middle East': 'Iraq',
    'North America': 'Washington',
    'South America': 'South America',
    'Africa': 'Africa',
    'East Asia': 'East Asia',
    'South Asia': 'South Asia',
    'Russia': 'Russia',
    'Ukraine': 'Ukraine',
    'Australia and Oceania': 'Australia',
    'US-Russia Relations': 'Moscow',
    'NATO': 'Brussels',
    'United Nations': 'New York',
    'Global Economy': 'World'
}

# Fetching coordinates and prevalence
for category, location in category_locations.items():
    prevalence = category_stats[category]['count'] / total_articles
    location_info = geolocator.geocode(location)
    if location_info:
        point = Point(location_info.longitude, location_info.latitude) # Create a Point object
        gdf.loc[len(gdf)] = [point, prevalence] # Add to the GeoDataFrame

# Plotting the world map
ax = world.plot(figsize=(15, 10))
gdf.plot(ax=ax, markersize=gdf['prevalence'] * 10000, color='red', alpha=0.5)

plt.title("Article Prevalence by Geographical Category")
plt.axis('off')
plt.show()
