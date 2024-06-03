from auto_blog import (
    generate_blog_content,
    load_previous_blogs,
    generate_image,
    post_blog,
    schedule_job,
    generate_seo_friendly_titles
)
from dotenv import load_dotenv

load_dotenv()

def main():
    # Load previous blogs
    previous_blogs = load_previous_blogs('path_to_previous_blogs')

    # Generate SEO-friendly titles
    keywords = ["manage OCD", "cope with anxiety", "improve mental health", "overcome depression"]
    titles = generate_seo_friendly_titles(keywords)

    # Generate blog content
    content = generate_blog_content(titles[0], previous_blogs)

    # Generate image
    image_url = generate_image("mental health")

    # Post the blog
    post_blog(titles[0], content, image_url)

if __name__ == "__main__":
    # Schedule the job to run daily at a specific time
    schedule_job(main, "10:00")
