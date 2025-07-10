import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_test_for_user(user, transcription_type):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://[web app link]/login/")

    try:
        # Wait for the email input field and enter the username
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "reportName1"))
        )
        email_input.send_keys(user['username'])

        # Wait for the password input field and enter the password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputkeyword1"))
        )
        password_input.send_keys(user['password'])

        # Wait for and click the sign-in button
        signin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "generateBtn1"))
        )
        signin_button.click()

        # Wait for and click the audio transcription button
        audio_transcription_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "transcriptionButton"))
        )
        audio_transcription_button.click()

        # Set dates using JavaScript
        driver.execute_script("document.getElementById('datepicker1').value = '2024-05-01';")
        driver.execute_script("document.getElementById('datepicker2').value = '2024-05-03';")

        # Wait for and click the generate report button
        generate_report_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "generateBtn1"))
        )
        generate_report_button.click()

        # Wait for the download buttons to appear
        time.sleep(5)  # Allow some time for the report to be generated

        download_buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='Download-one']"))
        )
        for button in download_buttons:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='Download-one']"))
            ).click()
            time.sleep(2)  # Wait between clicks

        time.sleep(60)  # Wait to ensure downloads are complete

    except Exception as e:
        print(f"An error occurred: {e}")

    # Keep the browser window open until manually closed
    print(f"Test completed for user: {user['username']}")
    # Note: Avoid calling driver.quit() here to keep the browser open

# Load the users from the JSON file
with open('../credentials.json', 'r') as file:
    users = json.load(file)['users']

# Create a thread for each user
threads = []
for user in users:
    thread = threading.Thread(target=run_test_for_user, args=(user,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
