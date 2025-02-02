from openai import OpenAI
from dotenv import load_dotenv
import os
from .post import format_content_with_images  # Import our formatting function

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_blog_content(title, previous_content):
    """Generate blog content using OpenAI's GPT model."""
    try:
        prompt = f"""Write a comprehensive blog post about {title}. 

Format the blog post with the following EXACT structure:

1. Title should be a single line without any "Title:" prefix
2. Start with a friendly greeting on its own line (e.g., "Hello, wellness warriors!")
3. Add an introduction paragraph

Then for each main section:
- Use numbered headings exactly like this: "1. Section Title" (not "Section 1:" or any other format)
- Each section should have 2-3 paragraphs
- Use descriptive subheadings with colons where appropriate (e.g., "Key Insight:", "Remember:")
- Add image markers between major sections like this: [IMAGE: description]

For example:

Hello, wellness seekers!

Introduction paragraph here...

1. Understanding the Basics
First paragraph of this section...

Second paragraph of this section...

[IMAGE: A calming illustration showing the main concept]

2. Key Strategies
Content here...

Key Insight: Additional important information...

Make sure to:
- Use EXACTLY this formatting
- Keep paragraphs separated by double newlines
- Place image markers on their own lines between sections
- End with a conclusion and call to action
- Don't add any extra formatting or markdown"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional blog writer specializing in mental health and wellness topics. You follow formatting instructions exactly."},
                {"role": "user", "content": f"Previous blog content for reference (to avoid duplication): {previous_content}"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Return the raw content
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating blog content: {str(e)}")
        return None

def generate_image_descriptions(content):
    """Extract image descriptions from the content and generate new ones if needed."""
    # Extract existing image descriptions
    image_descriptions = []
    lines = content.split('\n')
    content_without_markers = []
    
    for line in lines:
        if line.strip().startswith('[IMAGE:'):
            # Extract the description from [IMAGE: description]
            desc = line.strip()[7:-1].strip()
            image_descriptions.append(desc)
        else:
            content_without_markers.append(line)
    
    # If we don't have enough image descriptions, generate more
    while len(image_descriptions) < 3:
        try:
            prompt = f"""Based on this blog content:
            
{content}

Generate a description for an additional image that would complement the content.
The description should be detailed enough for image generation but avoid any references to specific medical conditions.
Focus on positive, uplifting imagery that represents wellness, growth, and healing."""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at creating image descriptions that are both meaningful and safe for AI image generation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            new_desc = response.choices[0].message.content.strip()
            image_descriptions.append(new_desc)
            
        except Exception as e:
            print(f"Error generating additional image description: {str(e)}")
            break
    
    # Return both the cleaned content and the image descriptions
    return '\n'.join(content_without_markers), image_descriptions 