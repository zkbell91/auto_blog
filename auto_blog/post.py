import os
import requests
import mimetypes
import base64
import json
from dotenv import load_dotenv

load_dotenv()

def create_trix_attachment(image_path):
    """Create a Trix attachment for an image."""
    try:
        # Determine the mime type
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = 'image/png'
        
        # Read and encode the image
        with open(image_path, 'rb') as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            
        # Create the Trix attachment format
        filename = os.path.basename(image_path)
        attachment = {
            "contentType": mime_type,
            "filename": filename,
            "filesize": os.path.getsize(image_path),
            "url": f"data:{mime_type};base64,{encoded}",
            "sgid": f"Attachment_{filename}"  # This might need to be adjusted based on your Rails setup
        }
        
        # Create the Trix attachment HTML with center alignment
        figure = f'<div style="text-align: center; margin: 20px 0;"><figure data-trix-attachment=\'{json.dumps(attachment)}\'></figure></div>'
        return figure
            
    except Exception as e:
        print(f"Error creating Trix attachment: {str(e)}")
        return None

def format_content_with_images(content, image_paths):
    """Format content with proper spacing and distributed images."""
    # Split content into paragraphs
    paragraphs = content.split('\n\n')
    
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
            # Use heading1 attribute for first section, heading2 for others
            heading_attr = 'heading1' if i == 0 else 'heading2'
            formatted_paragraph = f'<div data-trix-content-type="block" data-trix-attributes="{{\\"heading\\": true}}">{title_part.strip()}</div>'
            if rest_part.strip():
                formatted_paragraph += f'\n<div data-trix-content-type="block"><div class="paragraph">{rest_part.strip()}</div></div>'
        elif ':' in paragraph and len(paragraph.split(':')[0]) < 50:
            # Treat lines with colons as headings with bold attribute
            title_part = paragraph.split(':')[0]
            rest_part = ':'.join(paragraph.split(':')[1:])
            formatted_paragraph = f'<div data-trix-content-type="block" data-trix-attributes="{{\\"bold\\": true}}">{title_part.strip()}:</div>'
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
            (i > 2 and i % 3 == 0) or  # Every few paragraphs
            paragraph.strip().startswith(str(i)) or  # After numbered sections
            paragraph.strip().startswith('#')  # After headers
        ):
            # Use the create_trix_attachment function to properly format the image
            image_attachment = create_trix_attachment(image_paths[image_index])
            if image_attachment:
                formatted_content.append(image_attachment)
                formatted_content.append('<br data-trix-content-type="block">')  # Add block break after image
            image_index += 1
    
    # Add any remaining images near the end
    while image_index < len(image_paths):
        image_attachment = create_trix_attachment(image_paths[image_index])
        if image_attachment:
            formatted_content.append(image_attachment)
            formatted_content.append('<br data-trix-content-type="block">')  # Add block break after image
        image_index += 1
    
    return '\n'.join(formatted_content)

def post_blog(title, content, image_paths):
    """Post a blog using the API endpoint."""
    try:
        # Clean up the title (remove numbering and extra quotes)
        if title.startswith(('1. ', '2. ', '3. ')):
            title = title[3:]
        title = title.strip('"')
        
        # Format content with distributed images
        formatted_content = format_content_with_images(content, image_paths)
        
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

# Test case for post_blog function
if __name__ == "__main__":
    test_title = "Test Blog Post"
    test_content = "This is a test blog post content created via the API."
    post_blog(test_title, test_content)
