from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def generate_seo_friendly_titles(keywords):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Create a prompt that includes all keywords
    keywords_str = ", ".join(keywords)
    prompt = f"Generate 3 SEO-friendly blog post titles about mental health topics related to these keywords: {keywords_str}. Make the titles engaging and informative."
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates SEO-friendly blog titles."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract titles from the response
    titles_text = response.choices[0].message.content
    titles = [title.strip() for title in titles_text.split('\n') if title.strip()]
    
    return titles

# Test the function
if __name__ == "__main__":
    keywords = ["manage OCD", "cope with anxiety", "improve mental health"]
    titles = generate_seo_friendly_titles(keywords)
    print("Generated Titles:", titles)