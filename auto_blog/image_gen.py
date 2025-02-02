from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlparse
import time

load_dotenv()

def sanitize_prompt(description):
    """Make the prompt more general and safe for DALL-E."""
    # Remove any potentially problematic terms
    unsafe_terms = ['stressed', 'distressed', 'anxiety', 'depression', 'OCD', 'mental health', 'disorder']
    safe_prompt = description
    for term in unsafe_terms:
        safe_prompt = safe_prompt.replace(term.lower(), 'peaceful')
        safe_prompt = safe_prompt.replace(term.title(), 'Peaceful')
        safe_prompt = safe_prompt.replace(term.upper(), 'PEACEFUL')
    
    # Add style modifiers to make the image more artistic and abstract
    safe_prompt = f"Digital art style: {safe_prompt}. Soft colors, inspirational and uplifting mood."
    return safe_prompt

def generate_image_descriptions(content, num_images=3):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional image description writer. Create uplifting, peaceful image descriptions that focus on positive themes like growth, peace, and wellness. Avoid any references to medical conditions or mental health challenges."},
                {"role": "user", "content": f"Based on this blog content, generate {num_images} uplifting image descriptions that would complement the post well. Focus on metaphors of growth, peace, and wellness. Format each description on a new line starting with 'Image: ':\n\n{content}"}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating image descriptions: {str(e)}")
        return None

def generate_images_with_gpt4o(description):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    try:
        # Sanitize the prompt to make it more DALL-E friendly
        safe_prompt = sanitize_prompt(description)
        print(f"Using safe prompt: {safe_prompt}")
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=safe_prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

def download_image(url, title, index):
    if not url:
        return None
        
    try:
        # Create blog_images directory if it doesn't exist
        os.makedirs('blog_images', exist_ok=True)
        
        # Create a safe filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        filename = f"blog_images/blog_{index + 1}.png"
        
        # Download the image
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded successfully: {filename}")
            return filename
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error downloading image: {str(e)}")
        return None

# Test the functions
if __name__ == "__main__":
    test_content = "A blog post about personal growth and wellness through mindfulness techniques."
    descriptions = generate_image_descriptions(test_content, num_images=2)
    print("Generated Descriptions:", descriptions)
    
    if descriptions:
        for i, desc in enumerate(descriptions.split('\n')):
            if desc.startswith('Image: '):
                image_url = generate_images_with_gpt4o(desc[7:])  # Skip the "Image: " prefix
                if image_url:
                    filename = download_image(image_url, "test_blog", i)
                    print(f"Downloaded image {i + 1}: {filename}")
