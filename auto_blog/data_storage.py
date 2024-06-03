import json
import os

def load_previous_blogs(directory):
    blogs = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                blogs.append(json.load(file))
    return blogs

previous_blogs = load_previous_blogs('path_to_previous_blogs')