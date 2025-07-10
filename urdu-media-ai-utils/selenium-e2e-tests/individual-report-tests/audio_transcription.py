from selenium import webdriver
import time

driver = webdriver.Chrome()

driver.maximize_window()

driver.get("login url here")

email_input = driver.find_element("id", "reportName1")
email_input.send_keys("guest")

password_input = driver.find_element("id", "inputkeyword1")
password_input.send_keys("guest123")

signin_button = driver.find_element("id", "generateBtn1")
signin_button.click()

audio_transcription_button = driver.find_element("id", "transcriptionButton")
audio_transcription_button.click()

driver.execute_script("document.getElementById('datepicker1').value = '2024-05-01';")
driver.execute_script("document.getElementById('datepicker2').value = '2024-05-03';")

generate_report_button = driver.find_element("id", "generateBtn1")
generate_report_button.click()

time.sleep(5)

download_buttons = driver.find_elements("xpath", "//*[@id='Download-one']")
for button in download_buttons:
    button.click()
    time.sleep(2))

time.sleep(30)

driver.quit()
