import os
import requests
import base64
import mimetypes
import json

def create_trix_attachment(image_path):
    """Create a Trix attachment for an image."""
    try:
        # Get the mime type
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = 'image/png'
            
        # Read and encode the image
        with open(image_path, 'rb') as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            
        # Create the attachment data
        attachment = {
            "contentType": mime_type,
            "filename": os.path.basename(image_path),
            "filesize": os.path.getsize(image_path),
            "url": f"data:{mime_type};base64,{encoded}"
        }
        
        # Create the Trix attachment HTML
        attachment_html = f'<div data-trix-content-type="block" class="attachment-gallery attachment-gallery--1">'
        attachment_html += f'<figure data-trix-attachment=\'{json.dumps(attachment)}\' class="attachment attachment--preview attachment--png">'
        attachment_html += f'<img src="data:{mime_type};base64,{encoded}" width="1024" height="683">'
        attachment_html += '</figure></div>'
        return attachment_html
    except Exception as e:
        print(f"Error creating Trix attachment: {str(e)}")
        return None

def format_content_with_images(content, image_paths):
    # Clean up the title and content
    content = content.strip()
    
    # Remove the "Title: " prefix if it exists
    if content.startswith('Title:'):
        content = content[len('Title:'):].strip()
    
    # Split content into paragraphs
    paragraphs = content.split('\n\n')
    
    # Calculate spacing for images
    if image_paths:
        spacing = max(1, len(paragraphs) // (len(image_paths) + 1))
    
    # Initialize formatted content
    formatted_content = []
    image_index = 0
    
    for i, paragraph in enumerate(paragraphs):
        # Skip empty paragraphs
        if not paragraph.strip():
            continue
            
        # Handle numbered sections and headings with proper formatting
        if paragraph.strip()[0].isdigit() and '. ' in paragraph:
            # Numbered sections
            title_part = paragraph.split('\n')[0]
            rest_part = '\n'.join(paragraph.split('\n')[1:])
            # Combine heading with block formatting
            formatted_paragraph = f'<div data-trix-content-type="block"><h1>{title_part.strip()}</h1></div>'
            if rest_part.strip():
                formatted_paragraph += f'\n<div data-trix-content-type="block"><div class="paragraph">{rest_part.strip()}</div></div>'
        elif ':' in paragraph and len(paragraph.split(':')[0]) < 50:
            # Treat lines with colons as headings
            title_part = paragraph.split(':')[0]
            rest_part = ':'.join(paragraph.split(':')[1:])
            formatted_paragraph = f'<div data-trix-content-type="block"><h2>{title_part.strip()}:</h2></div>'
            if rest_part.strip():
                formatted_paragraph += f'\n<div data-trix-content-type="block"><div class="paragraph">{rest_part.strip()}</div></div>'
        else:
            # Regular paragraphs with block formatting
            formatted_paragraph = f'<div data-trix-content-type="block"><div class="paragraph">{paragraph.strip()}</div></div>'
        
        formatted_content.append(formatted_paragraph)
        formatted_content.append('<br data-trix-content-type="block">')  # Add block break between paragraphs
        
        # Add image after introduction, after a major section, or at calculated intervals
        if image_index < len(image_paths) and (
            i == 2 or  # After introduction
            (i > 2 and i % spacing == 0) or  # At calculated intervals
            paragraph.strip().startswith(str(i)) or  # After numbered sections
            paragraph.strip().startswith('#')  # After headers
        ):
            attachment_html = create_trix_attachment(image_paths[image_index])
            if attachment_html:
                formatted_content.append(attachment_html)
                formatted_content.append('<br data-trix-content-type="block">')  # Add block break after image
            image_index += 1
    
    # Add any remaining images near the end
    while image_index < len(image_paths):
        attachment_html = create_trix_attachment(image_paths[image_index])
        if attachment_html:
            formatted_content.append(attachment_html)
            formatted_content.append('<br data-trix-content-type="block">')  # Add block break after image
        image_index += 1
    
    return '\n'.join(formatted_content)

def post_blog(title, content, image_paths):
    # Clean up the title (remove numbering and extra quotes)
    if title.startswith(('1. ', '2. ', '3. ')):
        title = title[3:]
    title = title.strip('"')  # Remove surrounding quotes
    
    # Format content with distributed images
    formatted_content = format_content_with_images(content, image_paths)
    
    # Add title to the content with proper styling
    title_html = f'<div data-trix-content-type="block"><h1>{title}</h1></div>'
    formatted_content = title_html + '\n' + formatted_content
    
    # Wrap in Trix content div
    formatted_content = f'<div class="trix-content">\n{formatted_content}\n</div>'
    
    # Prepare the blog post data
    blog_data = {
        'blog': {
            'title': title,
            'content': formatted_content
        }
    }
    
    # Send the request to create the blog post
    api_endpoint = os.getenv('API_ENDPOINT')
    api_key = os.getenv('API_KEY')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.post(api_endpoint, json=blog_data, headers=headers)
        print("Sending request to API...")
        print(f"Endpoint: {api_endpoint}")
        print(f"Title: {title}")
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 201:
            blog_data = response.json()
            blog = blog_data.get('blog', {})
            
            print("\nBlog post successfully created!")
            print(f"Blog ID: {blog.get('id')}")
            print(f"Title: {blog.get('title')}")
            print(f"Slug: {blog.get('slug')}")
            print(f"Author: {blog.get('author')}")
            print(f"Created at: {blog.get('created_at')}")
            
            # Get the blog URL
            blog_base_url = os.getenv('BLOG_BASE_URL', 'http://localhost:3000')
            blog_url = f"{blog_base_url}/blogs/{blog.get('slug')}"
            print(f"URL: {blog_url}")
            
            print("Blog post successfully created and posted!")
            return True
        else:
            print(f"Failed to create blog post. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error creating blog post: {str(e)}")
        return False

def test_formatting():
    """Test function to verify formatting with sample content."""
    # Sample title with formatting issues we want to fix
    title = '1. "Understanding Mental Health: A Comprehensive Guide"'
    
    # Sample content with various formatting cases
    content = """Title: Understanding Mental Health: A Comprehensive Guide

Hello, wellness seekers!

In today's fast-paced world, understanding and maintaining our mental health has never been more important. Let's explore some key aspects of mental wellness and discover practical strategies for a healthier mind.

1. What is Mental Health?

Mental health encompasses our emotional, psychological, and social well-being. It affects how we think, feel, and act as we cope with life's challenges and relate to others.

2. Common Misconceptions

Many people believe that mental health only matters when there's a problem. However, just like physical health, our mental well-being requires constant attention and care.

3. Building Resilience

Resilience is our ability to bounce back from life's challenges. It's not about avoiding stress but developing healthy ways to cope with it.

4. Daily Practices

Simple daily practices can make a significant difference in our mental well-being. These might include meditation, exercise, or connecting with loved ones.

Remember, taking care of your mental health is not a sign of weakness - it's a sign of strength and self-awareness.

Your mental health journey is unique to you, and every small step counts towards overall well-being."""

    # Use actual existing images
    image_paths = [
        'blog_images/blog_1.png',
        'blog_images/blog_3.png',
        'blog_images/blog_5.png'
    ]
    
    # Test the blog posting with sample content
    return post_blog(title, content, image_paths)

if __name__ == "__main__":
    # Add test function call
    test_formatting() 