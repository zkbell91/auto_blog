import sys
from auto_blog.blog_generator import generate_blog_content, generate_image_descriptions
from auto_blog.image_gen import generate_images_with_gpt4o, download_image
from auto_blog.post import post_blog
from auto_blog.data_storage import load_previous_blogs, save_blog
from auto_blog.title_gen import generate_seo_friendly_titles
from auto_blog.schedule import schedule_job

def main():
    """Run the blog generation process."""
    try:
        # Step 1: Load previous blogs
        print("Step 1: Load previous blogs")
        previous_blogs = load_previous_blogs('./previous_blogs')
        print(f"Loaded {len(previous_blogs)} blogs: {previous_blogs}")

        # Step 2: Generate SEO-friendly titles
        print("Step 2: Generate SEO-friendly titles")
        keywords = ["manage OCD", "cope with anxiety", "improve mental health", "overcome depression"]
        titles = generate_seo_friendly_titles(keywords)
        if not titles:
            print("Failed to generate titles")
            return False
        print(f"Generated titles: {titles}")

        # Step 3: Generate blog content with embedded image markers
        print("Step 3: Generate blog content")
        content = generate_blog_content(titles[0], str(previous_blogs))
        if not content:
            print("Failed to generate blog content")
            return False

        # Step 4: Extract image descriptions and clean content
        print("Step 4: Generate image descriptions and images")
        clean_content, image_descriptions = generate_image_descriptions(content)
        if not image_descriptions:
            print("Failed to generate image descriptions")
            return False
        print(f"Generated image descriptions: {image_descriptions}")

        # Generate images for each description
        image_paths = []
        for i, description in enumerate(image_descriptions):
            print(f"Requesting image for: {description}")
            image_url = generate_images_with_gpt4o(description)
            if image_url:
                filename = download_image(image_url.strip(), titles[0], i)
                if filename:
                    image_paths.append(filename)
                    print(f"Downloaded Image {i + 1}: {filename}")
                else:
                    print(f"Failed to download image for URL: {image_url.strip()}")
            else:
                print(f"Failed to generate image URL for description: {description}")

        # Step 5: Post the blog
        print("Step 5: Post the blog")
        success = post_blog(titles[0], clean_content, image_paths)
        
        if success:
            # Save the blog details for future reference
            save_blog(titles[0], clean_content)
            print("Blog post successfully created and posted!")
            return True
        else:
            print("Failed to post blog")
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Checking for manual trigger argument...")
    print(f"Command-line arguments: {sys.argv}")
    if len(sys.argv) > 1 and sys.argv[1] == "run_once":
        print("Manual trigger detected. Running the job once for testing purposes.")
        main()
    else:
        # Use the separate scheduling module
        schedule_job(main)
