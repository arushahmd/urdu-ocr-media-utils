import os
import time
import csv
import uuid  # For generating unique task IDs
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import login_url, prefix
from multiple_reports_testing.config import temp_folder, elemental_wait, sleep_wait, no_users
from multiple_reports_testing.report_testing import test_audio_transcription, test_subtitle_generation, \
    test_news_ticker_analysis, test_keyword_based_search, test_trending_topics, \
    test_speaker_based_search
from multiple_reports_testing.utils import generate_users
import concurrent.futures

# Ensure that the 'results' directory exists
os.makedirs(os.path.join('results'), exist_ok=True)

# CSV file path for logging results
log_file = os.path.join(f"results/test_results_{no_users}.csv")

# Initialize the CSV file with headers
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "TaskID", "Username", "Email", "SignIn", "AudioTranscription",
                         "SubtitleGeneration", "KeywordBasedSearch", "SpeakerBasedSearch",
                         "NewsTickerAnalysis", "TrendingTopics"])



def log_result(user_name, email, login_status, test_results, task_id):
    """Logs the results of tests in the CSV file"""
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [current_time, task_id, user_name, email, login_status]
        row.extend(test_results)
        writer.writerow(row)


def run_test_single_user(user, task_id):
    # Initialize Chrome options
    options = webdriver.ChromeOptions()

    # Set preferences to handle the default download folder
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing-disable-download-protection": True,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # Initialize Chrome WebDriver with options
    driver = webdriver.Chrome(service=Service(), options=options)

    # Wait a bit for browser initialization
    time.sleep(3)
    driver.maximize_window()
    driver.get(login_url)

    login_status = "Failed"
    test_results = ["N/A"] * 6  # Initialize results for all tests as "N/A"

    # Try to login the user
    try:
        email_input = WebDriverWait(driver, elemental_wait).until(
            EC.presence_of_element_located((By.ID, "reportName1"))
        )
        email_input.send_keys(user['email'])

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputkeyword1"))
        )
        password_input.send_keys(user['password'])

        signin_button = WebDriverWait(driver, elemental_wait).until(
            EC.element_to_be_clickable((By.ID, "generateBtn1"))
        )
        signin_button.click()

        WebDriverWait(driver, elemental_wait).until(
            EC.presence_of_element_located((By.CLASS_NAME, "selection"))
        )

        print(f"Login Successful for {user['user_name']}")
        login_status = "Passed"  # Set login status to Passed

    except Exception as e:
        print(f"An Exception occurred while signing in: \n {e}")
        log_result(user['user_name'], user['email'], login_status, test_results, task_id)
        driver.quit()
        return

    time.sleep(sleep_wait)

    current_url = driver.current_url
    driver.execute_script("window.open(arguments[0], '_blank');", current_url)
    old_tab = driver.current_window_handle
    driver.switch_to.window(driver.window_handles[1])
    driver.switch_to.window(old_tab)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


    # Run the test functions and capture their results
    try:
        result = test_audio_transcription(user['user_name'], driver, temp_folder)
        if result == "Passed":
            test_results[0] = "Passed"
        else:
            test_results[0] = "Failed"
    except Exception as e:
        print(f"Audio Transcription Test Failed for {user['user_name']}: {e}")
        test_results[0] = "Failed"

    try:
        result = test_subtitle_generation(user['user_name'], driver, temp_folder)
        if result == "Passed":
            test_results[1] = "Passed"
        else:
            test_results[1] = "Failed"
    except Exception as e:
        print(f"Subtitle Generation Test Failed for {user['user_name']}: {e}")
        test_results[1] = "Failed"

    try:
        result = test_keyword_based_search(user['user_name'], driver, temp_folder)
        if result == "Passed":
            test_results[2] = "Passed"
        else:
            test_results[2] = "Failed"
    except Exception as e:
        print(f"Keyword Based Search Test Failed for {user['user_name']}: {e}")
        test_results[2] = "Failed"


    try:
        result = test_speaker_based_search(user['user_name'], driver, temp_folder)
        if result == "Passed":
            test_results[3] = "Passed"
        else:
            test_results[3] = "Failed"
    except Exception as e:
        print(f"Speaker Based Test Failed for {user['user_name']}: {e}")
        test_results[3] = "Failed"


    try:
        result = test_news_ticker_analysis(user['user_name'], driver, temp_folder)
        if result == "Passed":
            test_results[4] = "Passed"
        else:
            test_results[4] = "Failed"
    except Exception as e:
        print(f"News Ticker Analysis Test Failed for {user['user_name']}: {e}")
        test_results[4] = "Failed"

    try:
        result = test_trending_topics(user['user_name'], driver, temp_folder)
        if result == "Passed":
            test_results[5] = "Passed"
        else:
            test_results[5] = "Failed"
    except Exception as e:
        print(f"Trending Topics Test Failed for {user['user_name']}: {e}")
        test_results[5] = "Failed"


    # Log the results after all tests
    log_result(user['user_name'], user['email'], login_status, test_results, task_id)

    driver.quit()


# Generate users
user_list = generate_users(prefix, no_users)

# Generate a unique task ID for this batch of users
task_id = str(uuid.uuid4())  # Unique Task ID

# Run tests for multiple users in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Map run_test_single_user to the user_list with the task_id
    results = list(executor.map(lambda user: run_test_single_user(user, task_id), user_list[:no_users]))

print("All tests completed.")
