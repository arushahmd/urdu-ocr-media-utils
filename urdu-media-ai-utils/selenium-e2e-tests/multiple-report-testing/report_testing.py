import os
import time
import shutil
from time import sleep

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from setuptools.sandbox import save_path

from multiple_reports_testing.config import generate_report_dashboard_url, elemental_wait, timeout, result_wait, \
    sleep_wait
from multiple_reports_testing.utils import update_download_directory, clear_folder, return_to_home


def test_audio_transcription(username, driver, base_temp_folder):
    # Create a unique temp folder for the user
    user_folder = os.path.join(base_temp_folder, username)
    save_folder = os.path.join(user_folder, "audio_transcription")

    # Set the download directory to the user's audio transcription folder
    update_download_directory(driver, save_folder)

    # Create the user's folders if they don't exist
    os.makedirs(save_folder, exist_ok=True)
    clear_folder(save_folder)

    # Wait for and click the audio transcription button
    audio_transcription_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "transcriptionButton"))
    )
    audio_transcription_button.click()

    # Set dates using JavaScript
    driver.execute_script("document.getElementById('datepicker1').value = '2024-05-01';")
    driver.execute_script("document.getElementById('datepicker2').value = '2024-05-03';")

    # Wait for and click the generate report button
    generate_report_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "generateBtn1"))
    )
    generate_report_button.click()

    # Wait for the download buttons to appear
    time.sleep(3)

    download_buttons = WebDriverWait(driver, elemental_wait).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='Download-one']"))
    )

    for button in download_buttons:
        WebDriverWait(driver, elemental_wait).until(
            EC.element_to_be_clickable(button)
        ).click()

        # Wait for the file to be downloaded
        time.sleep(sleep_wait)  # Wait a bit for the download to start

        # Wait for the file to appear in the directory
        start_time = time.time()
        download_successful = False

        while time.time() - start_time < timeout:
            for filename in os.listdir(save_folder):
                if filename.endswith('.docx') or filename.endswith(".txt"):
                    download_successful = True
                    break

            if download_successful:
                break
        clear_folder(save_folder)
        if download_successful:
            print(f"File download successful for Audio Transcription.")
            return_to_home(driver)
            return "Passed"
        else:
            print(f"File download unsuccessful for Audio Transcription.")
            return_to_home(driver)
            return "Failed"


def test_subtitle_generation(username, driver, base_temp_folder):
    # Create a unique temp folder for the user
    user_folder = os.path.join(base_temp_folder, username)
    save_folder = os.path.join(user_folder, "subtitle_generation")

    # Create the user's folders if they don't exist
    os.makedirs(save_folder, exist_ok=True)
    clear_folder(save_folder)

    # Set the download directory to the user's audio transcription folder
    update_download_directory(driver, save_folder)

    # Wait for and click the subtitle transcription button
    subtitle_transcription_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "subtitlingButton"))
    )
    subtitle_transcription_button.click()

    # Set dates using JavaScript
    driver.execute_script("document.getElementById('datepicker1').value = '2024-05-01';")
    driver.execute_script("document.getElementById('datepicker2').value = '2024-05-03';")

    # Wait for and click the generate report button
    generate_report_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "generateBtn1"))
    )
    generate_report_button.click()

    time.sleep(5)

    # Wait for the download buttons to appear
    download_buttons = WebDriverWait(driver, elemental_wait).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='Download-one']"))
    )

    for button in download_buttons:
        WebDriverWait(driver, elemental_wait).until(
            EC.element_to_be_clickable(button)
        ).click()

        # Wait for the file to be downloaded
        time.sleep(sleep_wait)  # Wait a bit for the download to start

        # Wait for the file to appear in the directory
        start_time = time.time()
        download_successful = False

        while time.time() - start_time < timeout:
            for filename in os.listdir(save_folder):
                if  filename.endswith('.srt'): #  filename.endswith('.docx') or filename.endswith(".txt")
                    download_successful = True
                    break

            if download_successful:
                break
        clear_folder(save_folder)
        if download_successful:
            print(f"File download successful for Subtitle Generation.")
            return_to_home(driver)
            return "Passed"
        else:
            print(f"File download unsuccessful for Subtitle Generation.")
            return_to_home(driver)
            return "Failed"


def test_keyword_based_search(username, driver, base_temp_folder):
    # Create a unique temp folder for the user
    user_folder = os.path.join(base_temp_folder, username)
    save_folder = os.path.join(user_folder, "keyword_based")

    # Create the user's folders if they don't exist
    os.makedirs(save_folder, exist_ok=True)
    clear_folder(save_folder)

    # Set the download directory to the user's audio transcription folder
    update_download_directory(driver, save_folder)

    # Wait for and click the keyword-based search button
    keyword_search_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "keywordBasedButton"))
    )
    keyword_search_button.click()

    # Set dates and keyword using JavaScript
    driver.execute_script("document.getElementById('t1').value = 'کی';")
    driver.execute_script("document.getElementById('datepicker1').value = '2024-05-01';")
    driver.execute_script("document.getElementById('datepicker2').value = '2024-05-03';")

    # Wait for and click the generate report button
    generate_report_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "generateBtn1"))
    )
    generate_report_button.click()

    # Wait for the download button to appear
    download_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, 'downloadBtn'))
    )
    download_button.click()

    # Wait for the file to be downloaded
    time.sleep(sleep_wait)  # Wait a bit for the download to start

    # Wait for the file to appear in the directory
    start_time = time.time()
    download_successful = False

    while time.time() - start_time < timeout:
        for filename in os.listdir(save_folder):
            if filename.endswith('.docx') or filename.endswith(".txt") or filename.endswith(".txt"):
                download_successful = True
                break

        if download_successful:
            break

    clear_folder(save_folder)

    if download_successful:
        print(f"File download successful for Keyword Based Search.")
        return_to_home(driver)
        return "Passed"
    else:
        print(f"File download unsuccessful for Keyword Based Search.")
        return_to_home(driver)
        return "Failed"

def test_speaker_based_search(username, driver, base_temp_folder):
    # Create a unique temp folder for the user
    user_folder = os.path.join(base_temp_folder, username)
    save_folder = os.path.join(user_folder, "speaker_based")

    # Create the user's folders if they don't exist
    os.makedirs(save_folder, exist_ok=True)
    clear_folder(save_folder)

    # Set the download directory to the user's audio transcription folder
    update_download_directory(driver, save_folder)

    # Wait for and click the speaker-based search button
    speaker_search_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "speakerBasedButton"))
    )
    speaker_search_button.click()

    # Set dates and speaker name using JavaScript
    driver.execute_script("document.getElementById('speaker_name').value = 'Nasim Zehra';")
    driver.execute_script("document.getElementById('t1').value = 'کی';")
    driver.execute_script("document.getElementById('datepicker1').value = '2024-05-01';")
    driver.execute_script("document.getElementById('datepicker2').value = '2024-05-05';")

    time.sleep(5)

    # Wait for and click the generate report button
    generate_report_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "generateBtn1"))
    )
    generate_report_button.click()

    # Wait for the download button to appear
    download_button = WebDriverWait(driver, elemental_wait).until(
        EC.presence_of_element_located((By.ID, "downloadBtn"))
    )

    # Wait until the button is clickable and click it
    WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "downloadBtn"))
    ).click()

    # Wait for the file to be downloaded
    time.sleep(sleep_wait)  # Wait a bit for the download to start

    # Wait for the file to appear in the directory
    start_time = time.time()
    download_successful = False

    while time.time() - start_time < timeout:
        for filename in os.listdir(save_folder):
            if filename.endswith('.docx') or filename.endswith(".txt"):
                download_successful = True
                break

        if download_successful:
            break

    clear_folder(save_folder)
    if download_successful:
        print(f"File download successful for Speaker Based Search.")
        return_to_home(driver)
        return "Passed"
    else:
        print(f"File download unsuccessful for Speaker Based Search.")
        return_to_home(driver)
        return "Failed"


def test_news_ticker_analysis(username, driver, base_temp_folder):
    # Create a unique temp folder for the user
    user_folder = os.path.join(base_temp_folder, username)
    save_folder = os.path.join(user_folder, "news_ticker_analysis")

    # Create the user's folders if they don't exist
    os.makedirs(save_folder, exist_ok=True)
    clear_folder(save_folder)

    # Set the download directory to the user's audio transcription folder
    update_download_directory(driver, save_folder)

    # Wait for and click the news ticker button
    news_ticker_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "tickerButton"))
    )
    news_ticker_button.click()

    # Set dates using JavaScript
    driver.execute_script("document.getElementById('datepicker1').value = '2024-05-01';")
    driver.execute_script("document.getElementById('datepicker2').value = '2024-05-03';")

    # Wait for and click the generate report button
    generate_report_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "generateBtn1"))
    )
    generate_report_button.click()

    # Wait for the download buttons to appear
    download_buttons = WebDriverWait(driver, elemental_wait).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='Download-one']"))
    )

    for button in download_buttons:
        WebDriverWait(driver, elemental_wait).until(
            EC.element_to_be_clickable(button)
        ).click()

        # Wait for the file to be downloaded
        time.sleep(sleep_wait)  # Wait a bit for the download to start

        # Wait for the file to appear in the directory
        start_time = time.time()
        download_successful = False

        while time.time() - start_time < timeout:
            for filename in os.listdir(save_folder):
                if filename.endswith('.docx') or filename.endswith(".txt"):
                    download_successful = True
                    break

            if download_successful:
                break

        clear_folder(save_folder)
        if download_successful:
            print(f"File download successful for News Ticker Analysis.")
            return_to_home(driver)
            return "Passed"
        else:
            print(f"File download unsuccessful for News Ticker Analysis.")
            return_to_home(driver)
            return "Failed"


def test_trending_topics(username, driver, base_temp_folder):
    # Create a unique temp folder for the user
    user_folder = os.path.join(base_temp_folder, username)
    save_folder = os.path.join(user_folder, "tending_topics")

    # Create the user's folders if they don't exist
    os.makedirs(save_folder, exist_ok=True)
    clear_folder(save_folder)

    # Set the download directory to the user's audio transcription folder
    update_download_directory(driver, save_folder)

    # Wait for and click the audio transcription button
    subtitle_transcription_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "trendingTopicsButton"))
    )
    subtitle_transcription_button.click()

    # Set dates using JavaScript
    driver.execute_script("document.getElementById('inputkeyword1').value = '4';")
    driver.execute_script("document.getElementById('datepicker1').value = '2024-05-01';")
    driver.execute_script("document.getElementById('datepicker2').value = '2024-05-03';")

    # Wait for and click the generate report button
    generate_report_button = WebDriverWait(driver, elemental_wait).until(
        EC.element_to_be_clickable((By.ID, "generateBtn1"))
    )
    generate_report_button.click()

    time.sleep(3)

    # Wait for the chart element to be visible after generating the report
    try:
        WebDriverWait(driver, result_wait).until(
            EC.visibility_of_element_located((By.ID, "myChart"))
        )
        WebDriverWait(driver, result_wait).until(
            EC.visibility_of_element_located((By.ID, "plot-div"))
        )
        print("Report generation passed: myChart and plot-div are visible.")
        return "Passed"  # Return "Passed" if both elements are visible

    except Exception as e:
        print(f"Report generation failed: {e}")
        return_to_home(driver)
        return "Failed"  # Return "Failed" if an exception occurs

