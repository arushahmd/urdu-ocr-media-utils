import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_signup_for_user(user):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://[weeb-app-link]/accounts/signup/")

    try:
        # Wait for and fill in the first name field
        first_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstName"))
        )
        first_name_input.send_keys("gFirstname")

        # Wait for and fill in the last name field
        last_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "lastName"))
        )
        last_name_input.send_keys("gLastname")

        # Wait for and fill in the email field
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(user['username'])  # Email is used as the username

        # Wait for and fill in the institute field
        institute_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "institute"))
        )
        institute_input.send_keys("UET")

        # Wait for and fill in the password field
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.send_keys(user['password'])

        # Wait for and fill in the confirm password field
        confirm_password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cnfrmPassword"))
        )
        confirm_password_input.send_keys(user['password'])

        # Wait for and click the signup button
        signup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "generateBtn1"))
        )
        signup_button.click()

        # Wait for the signup process to complete
        time.sleep(6)  # Adjust if necessary based on actual wait time

    except Exception as e:
        print(f"An error occurred: {e}")

    # Keep the browser window open until manually closed
    print(f"Signup completed for user: {user['username']}")
    # Note: Avoid calling driver.quit() here to keep the browser open

# Load the users from the JSON file
with open('../credentials.json', 'r') as file:
    users = json.load(file)['users']

# Create a thread for each user
threads = []
for user in users:
    thread = threading.Thread(target=run_signup_for_user, args=(user,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
