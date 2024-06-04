import openai
from dotenv import load_dotenv
import os

load_dotenv()

def generate_blog_content(title, previous_blogs):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    context = "\n".join([blog['content'] for blog in previous_blogs])
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Write a detailed blog post about '{title}'. Here is some context from previous blog posts: {context}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1500
    )
    
    return response['choices'][0]['message']['content']

# Test the function
if __name__ == "__main__":
    previous_blogs = [
        {"content": "Content of previous blog 1."},
        {"content": "Content of previous blog 2."}
    ]
    title = "How to manage OCD for Better Mental Health"
    content = generate_blog_content(title, previous_blogs)
    print("Generated Content:", content)
