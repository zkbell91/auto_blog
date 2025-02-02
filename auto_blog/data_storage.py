import json
import os
import time

def load_previous_blogs(directory):
    blogs = []
    try:
        print(f"Checking directory: {os.path.abspath(directory)}")
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        for filename in os.listdir(directory):
            print(f"Found file: {filename}")
            if filename.endswith(".json"):
                with open(os.path.join(directory, filename), 'r') as file:
                    blogs.append(json.load(file))
    except Exception as e:
        print(f"An error occurred: {e}")
    return blogs

def save_blog(title, content):
    """Save blog content to a JSON file."""
    try:
        directory = './previous_blogs'
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create a unique filename using timestamp
        timestamp = int(time.time())
        filename = f"blog_{timestamp}.json"
        filepath = os.path.join(directory, filename)
        
        # Prepare blog data
        blog_data = {
            'title': title,
            'content': content,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to file
        with open(filepath, 'w') as file:
            json.dump(blog_data, file, indent=2)
            
        print(f"Blog saved to {filepath}")
        return True
        
    except Exception as e:
        print(f"Error saving blog: {str(e)}")
        return False

# Update this path to the actual path where your blog JSON files are stored
previous_blogs = load_previous_blogs('./previous_blogs')  # Adjusted path
print(f"Loaded {len(previous_blogs)} blogs")  # Debug line
