# FUN VIZUALIZATION OF HOT SCIENCE TOPICS

from newsapi import NewsApiClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

# Initialize the News API client
newsapi = NewsApiClient(api_key='your-api-key')

# Fetch articles from specified domains
articles = newsapi.get_everything(domains='nature.com,thelancet.com,sciencemag.org,nature.com/srep,scientificamerican.com',
                                  language='en',
                                  page_size=100)

# Print the number of articles retrieved
num_articles = len(articles['articles'])
print(f"Retrieved {num_articles} articles.")

# Extract texts from the articles
texts = [article['title'] + ' ' + article['description'] for article in articles['articles']]

# Use TF-IDF Vectorizer to convert the texts to vectors
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

# Use KMeans to cluster the documents
n_clusters = min(5, len(texts))
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)

# Get the cluster centers
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()

# Generate and print topic labels for each cluster
for i in range(n_clusters):
    top_terms = [terms[ind] for ind in order_centroids[i, :3]]  # Consider top 3 terms
    topic_label = " ".join(top_terms)
    print(f"Cluster {i} Topic: {topic_label}")

# Create a DataFrame to store the texts and labels
labels = kmeans.labels_
clusters = pd.DataFrame({'text': texts, 'label': labels})
cluster_counts = clusters['label'].value_counts(normalize=True)

# Print the clustered topics with their proportions
for cluster, proportion in cluster_counts.items():
    print(f"\nCluster {cluster} represents {proportion * 100:.2f}% of the articles")
    print("Sample articles from this cluster:")
    num_samples = min(3, clusters[clusters['label'] == cluster].shape[0])
    samples = clusters[clusters['label'] == cluster].sample(num_samples)['text']
    for sample in samples:
        print(f"- {sample}")


## VISIALIZATION ##

import matplotlib.pyplot as plt

# Generate topic labels
cluster_topics = [" ".join([terms[ind] for ind in order_centroids[i, :3]]) for i in range(n_clusters)]

# Create labels for the pie chart
labels = [f"Cluster {i} Topic: {cluster_topics[i]}" for i in range(n_clusters)]
sizes = [cluster_counts[i] * 100 for i in range(n_clusters)]

# Create a pie chart
plt.figure(figsize=(10, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
plt.title('Cluster Distribution')
plt.show()
