from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def generate_blog_content(title, previous_blogs):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    context = "\n".join([blog['content'] for blog in previous_blogs])
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional mental health blog writer. Write engaging, informative content that helps readers understand and manage their mental health."},
            {"role": "user", "content": f"Write a detailed blog post about '{title}'. Here is some context from previous blog posts for style and tone: {context}"}
        ]
    )
    
    return response.choices[0].message.content

# Test the function
if __name__ == "__main__":
    previous_blogs = [
        {"content": "Content of previous blog 1."},
        {"content": "Content of previous blog 2."}
    ]
    title = "How to Manage OCD for Better Mental Health"
    content = generate_blog_content(title, previous_blogs)
    print("Generated Content:", content)
