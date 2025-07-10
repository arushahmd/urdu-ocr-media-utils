import os
import shutil
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from multiple_reports_testing.config import elemental_wait, generate_report_dashboard_url


def generate_users(prefix, n):
    users = []
    for i in range(1, n + 1):
        user_name = f"{prefix}{i}"
        email = f"{user_name}@gmail.com"
        password = "guest123"  # Password remains the same for all users
        user = {
            'user_name': user_name,
            # 'email': email,
            'email': "guest",
            'password': password
        }
        users.append(user)
    return users


def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)  # Remove the file
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Remove directory and its contents


def update_download_directory(driver, new_directory):
    # Set the new download directory using preferences
    prefs = {
        "download.default_directory": os.path.abspath(new_directory),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing-disable-download-protection": True
    }
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": os.path.abspath(new_directory)})


def return_to_home(driver):
    # Wait for the element with the specified class name to be present
    try:
        element = WebDriverWait(driver, elemental_wait).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'links'))
        )

        # Find the first <li> inside the element
        first_li = element.find_element(By.TAG_NAME, 'li')

        # Click the first <li>
        first_li.click()

        return True

    except TimeoutException:
        print("Element not found within the timeout period. Redirecting to the specified URL.")
        # Redirect the browser to a different URL (change 'your_redirect_url' to the desired URL)
        driver.execute_script(f"window.location.href = '{generate_report_dashboard_url}';")

        return False


def fill_dates(driver):
    """
        Fills dates for start and end.
    :param driver:
    :return:
    """