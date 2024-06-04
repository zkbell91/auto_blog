from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import os
from dotenv import load_dotenv

load_dotenv()

def close_overlay(driver):
    try:
        print("Closing overlays if any...")
        overlay = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cc-nb-main-container"))
        )
        driver.execute_script("arguments[0].style.display = 'none';", overlay)
    except TimeoutException:
        print("No overlay found or it cannot be closed.")

def post_blog(title, user, description, keywords, content, image_filenames):
    # Initialize the browser
    driver = webdriver.Chrome()
    driver.get(os.getenv('BLOG_URL'))

    try:
        # Wait for the login page to load completely
        print("Waiting for login page to load...")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_email")))
        
        # Locate the email field and enter the email
        print("Entering email...")
        email_field = driver.find_element(By.ID, "user_email")
        email_field.send_keys(os.getenv('BLOG_EMAIL'))
        
        # Locate the password field and enter the password
        print("Entering password...")
        password_field = driver.find_element(By.NAME, "user[password]")
        password_field.send_keys(os.getenv('BLOG_PASSWORD'))
        
        # Submit the login form
        print("Submitting login form...")
        password_field.send_keys(Keys.RETURN)
        
        # Wait for the "Signed in successfully" message to appear
        print("Waiting for successful login message...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'text-green-700') and contains(text(), 'Signed in successfully.')]"))
        )
        
        # Navigate to the new post page
        print("Navigating to new blog post page...")
        driver.get(os.getenv('NEW_POST_URL'))
        
        # Wait for the new post page to load completely
        print("Waiting for new blog post page to load...")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "blog_title")))
        
        # Enter the title
        print("Entering the title...")
        title_field = driver.find_element(By.ID, "blog_title")
        title_field.send_keys(title)
        
        # Enter the user
        print("Entering the user...")
        user_field = driver.find_element(By.ID, "blog_user_id")
        user_field.send_keys(user)
        
        # Enter the description
        print("Entering the description...")
        description_field = driver.find_element(By.ID, "blog_description")
        description_field.send_keys(description)
        
        # Enter the keywords
        print("Entering the keywords...")
        keywords_field = driver.find_element(By.ID, "blog_keywords")
        keywords_field.send_keys(keywords)
        
        # Enter the content
        print("Entering the content...")
        content_field = driver.find_element(By.ID, "blog_content")
        content_field.send_keys(content)
        
        # Upload images (if applicable)
        for image_filename in image_filenames:
            # Verify the image file exists
            if not os.path.exists(image_filename):
                print(f"Error: File not found - {image_filename}")
                continue

            close_overlay(driver)

            # Scroll the "Attach Files" button into view and click it using JavaScript
            print("Clicking the 'Attach Files' button...")
            attach_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-trix-action='attachFiles']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", attach_button)
            driver.execute_script("arguments[0].click();", attach_button)
            time.sleep(1)  # Allow time for the file dialog to open

            # Simulate the file selection in the dialog
            print(f"Uploading image: {image_filename}")
            file_input = driver.execute_script("return document.querySelector('input[type=file]');")
            if file_input:
                file_input.send_keys(os.path.abspath(image_filename))
            else:
                print("File input element not found.")
            time.sleep(1)  # Wait a bit for the upload to process

        close_overlay(driver)

        # Click the submit button to publish the blog
        print("Clicking the submit button...")
        submit_button = driver.find_element(By.NAME, "commit")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Wait to ensure the post is published
        print("Waiting for the post to be published...")
        WebDriverWait(driver, 20).until(EC.url_contains("/blogs"))
        
        print("Blog post successfully created and posted!")
        
    except ElementClickInterceptedException as e:
        print(f"ElementClickInterceptedException occurred: {str(e)}")
    except TimeoutException as e:
        print(f"TimeoutException occurred: {str(e)}")
    except NoSuchElementException as e:
        print(f"NoSuchElementException occurred: {str(e)}")
    except Exception as e:
        print(f"An error occurred while posting the blog: {e.__class__.__name__}: {str(e)}")
        
    finally:
        driver.quit()

# Test case for post_blog function
if __name__ == "__main__":
    test_title = "Test Blog Post Title"
    test_user = "Zachary Bell (Admin)"
    test_description = "This is a test description."
    test_keywords = "test, blog, selenium"
    test_content = "This is a test blog post content."
    test_image_filenames = [
        "/Users/zack/Desktop/coding-environment/src/web-check/auto_blog/blog_images/how_to_manage_ocd_for_better_mental_health_1.png", 
        "/Users/zack/Desktop/coding-environment/src/web-check/auto_blog/blog_images/how_to_manage_ocd_for_better_mental_health_2.png"
    ]  # Replace with actual paths to test images
    post_blog(test_title, test_user, test_description, test_keywords, test_content, test_image_filenames)
