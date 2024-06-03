import random

def generate_seo_friendly_titles(keywords, num_titles=5):
    titles = []
    for _ in range(num_titles):
        keyword = random.choice(keywords)
        title = f"How to {keyword} for Better Mental Health"
        titles.append(title)
    return titles

keywords = ["manage OCD", "cope with anxiety", "improve mental health", "overcome depression"]
titles = generate_seo_friendly_titles(keywords)