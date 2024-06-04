from auto_blog.content_gen import generate_blog_content
from auto_blog.data_storage import load_previous_blogs
from auto_blog.image_gen import generate_image_descriptions, generate_images_with_gpt4o, download_image
from auto_blog.post import post_blog
from auto_blog.title_gen import generate_seo_friendly_titles
from auto_blog.schedule import schedule_job
from dotenv import load_dotenv
import os
import schedule
import time
import sys

load_dotenv()

def main():
    try:
        # Step 1: Load previous blogs
        print("Step 1: Load previous blogs")
        previous_blogs = load_previous_blogs('./previous_blogs')
        print(f"Loaded {len(previous_blogs)} blogs: {previous_blogs}")  # Debug line

        # Step 2: Generate SEO-friendly titles
        print("Step 2: Generate SEO-friendly titles")
        keywords = ["manage OCD", "cope with anxiety", "improve mental health", "overcome depression"]
        titles = generate_seo_friendly_titles(keywords)
        print(f"Generated titles: {titles}")  # Debug line

        # Step 3: Generate blog content
        print("Step 3: Generate blog content")
        content = generate_blog_content(titles[0], previous_blogs)
        print(f"Generated content: {content}")  # Debug line

        # Step 4: Generate image descriptions and images
        print("Step 4: Generate image descriptions and images")
        descriptions = generate_image_descriptions(content, num_images=3)
        print(f"Generated image descriptions: {descriptions}")  # Debug line
        image_filenames = []
        descriptions_list = descriptions.split("\n")
        
        for i, description in enumerate(descriptions_list):
            if "Image" in description:
                print(f"Requesting image for: {description}")
                image_url = generate_images_with_gpt4o(description)
                if image_url:
                    filename = download_image(image_url.strip(), titles[0], i)
                    if filename:
                        image_filenames.append(filename)
                        print(f"Downloaded Image {i + 1}: {filename}")
                    else:
                        print(f"Failed to download image for URL: {image_url.strip()}")
                else:
                    print(f"Failed to generate image URL for description: {description}")

        # Step 5: Combine content and images
        print("Step 5: Combine content and images")
        content_with_images = content
        for filename in image_filenames:
            content_with_images += f"\n\n![Image]({filename})"
        print(f"Content with images: {content_with_images}")  # Debug line

        # Step 6: Post the blog
        print("Step 6: Post the blog")
        post_blog(titles[0], content_with_images, image_filenames)
        print("Blog post successfully created and posted!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Checking for manual trigger argument...")  # Debug line
    print(f"Command-line arguments: {sys.argv}")  # Debug line
    if len(sys.argv) > 1 and sys.argv[1] == "run_once":
        print("Manual trigger detected. Running the job once for testing purposes.")
        main()
    else:
        print("Starting the scheduler. Press Ctrl+C to exit.")
        schedule_job(main, "10:00")
