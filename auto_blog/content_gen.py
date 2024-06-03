import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def generate_blog_content(title, previous_blogs):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    context = "\n".join([blog['content'] for blog in previous_blogs])
    prompt = f"Write a detailed blog post about '{title}'.\n\n{context}"
    
    response = openai.Completion.create(
      engine="gpt-4o",
      prompt=prompt,
      max_tokens=1500,
      temperature=0.7
    )
    
    return response.choices[0].text

# Example usage (this would be called from main.py)
# previous_blogs = load_previous_blogs('path_to_previous_blogs')
# title = "How to manage OCD for Better Mental Health"
# content = generate_blog_content(title, previous_blogs)
# print(content)
