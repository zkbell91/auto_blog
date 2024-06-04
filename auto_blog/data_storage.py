import json
import os

def load_previous_blogs(directory):
    blogs = []
    try:
        print(f"Checking directory: {os.path.abspath(directory)}")  # Debug line
        if not os.path.exists(directory):
            print(f"Error: The directory '{directory}' does not exist.")
            return blogs
        for filename in os.listdir(directory):
            print(f"Found file: {filename}")  # Debug line
            if filename.endswith(".json"):
                with open(os.path.join(directory, filename), 'r') as file:
                    blogs.append(json.load(file))
    except Exception as e:
        print(f"An error occurred: {e}")
    return blogs

# Update this path to the actual path where your blog JSON files are stored
previous_blogs = load_previous_blogs('./previous_blogs')  # Adjusted path
print(f"Loaded {len(previous_blogs)} blogs")  # Debug line
