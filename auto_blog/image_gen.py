import openai
from dotenv import load_dotenv
import os
import requests
import re

load_dotenv()

def sanitize_title(title):
    # Remove special characters and limit length
    sanitized = re.sub(r'\W+', '_', title)
    return sanitized[:50]  # Truncate to 50 characters

def generate_image_descriptions(content, num_images=3):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can generate images."},
        {"role": "user", "content": f"Generate {num_images} images based on the following blog content: {content}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300
    )
    
    return response['choices'][0]['message']['content']

def generate_images_with_gpt4o(description):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Image.create(
        prompt=description,
        n=1,
        size="1024x1024"
    )
    
    return response['data'][0]['url']

def download_image(image_url, title, index):
    folder = './blog_images'
    os.makedirs(folder, exist_ok=True)
    sanitized_title = sanitize_title(title)
    filename = os.path.join(folder, f"{sanitized_title}_{index + 1}.png")
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        print(f"Error: Could not download image from {image_url}")
        return None

# Test the functions
if __name__ == "__main__":
    content = "This blog post covers various aspects of managing OCD for better mental health..."
    title = "How to Manage OCD for Better Mental Health"
    descriptions = generate_image_descriptions(content, num_images=3)
    print("Generated Descriptions:", descriptions)
    
    descriptions_list = descriptions.split("\n")
    image_urls = []
    
    for i, description in enumerate(descriptions_list):
        if "Image" in description:
            print(f"Requesting image for: {description}")
            image_url = generate_images_with_gpt4o(description)
            if image_url:
                image_urls.append(image_url)
    
    for i, image_url in enumerate(image_urls):
        filename = download_image(image_url.strip(), title, i)
        if filename:
            print(f"Downloaded Image {i + 1}: {filename}")
        else:
            print(f"Failed to download image for URL: {image_url.strip()}")
