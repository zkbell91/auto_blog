import requests

def generate_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id=your_unsplash_access_key"
    response = requests.get(url)
    data = response.json()
    return data['urls']['regular']

image_url = generate_image("mental health")