from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os

load_dotenv()

def post_blog(title, content, image_url):
    driver = webdriver.Chrome()
    driver.get("https://mosaicmindscounseling.com/admin")

    # Log in
    driver.find_element(By.NAME, "username").send_keys(os.getenv('WEBSITE_USERNAME'))
    driver.find_element(By.NAME, "password").send_keys(os.getenv('WEBSITE_PASSWORD'))
    driver.find_element(By.NAME, "login").click()

    time.sleep(3)  # Wait for the login to complete

    # Navigate to new post
    driver.find_element(By.LINK_TEXT, "New Post").click()
    
    # Fill in the post details
    driver.find_element(By.NAME, "title").send_keys(title)
    driver.find_element(By.NAME, "content").send_keys(content)
    driver.find_element(By.NAME, "image_url").send_keys(image_url)
    
    # Publish the post
    driver.find_element(By.NAME, "publish").click()
    
    driver.quit()
