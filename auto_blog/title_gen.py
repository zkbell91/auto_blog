import openai
from dotenv import load_dotenv
import os

load_dotenv()

def generate_seo_friendly_titles(keywords, num_titles=5):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Generate SEO-friendly blog post titles for a mental health blog. Use the following keywords: " + ", ".join(keywords) + ". Provide {} titles.".format(num_titles)}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=100,
    )
   
    titles = []
    for choice in response['choices']:
        if choice['message']['role'] == 'assistant':
            titles.append(choice['message']['content'])
    return titles

# Test the function
if __name__ == "__main__":
    keywords = ["manage OCD", "cope with anxiety", "improve mental health", "overcome depression"]
    titles = generate_seo_friendly_titles(keywords)
    print("Generated Titles:", titles)