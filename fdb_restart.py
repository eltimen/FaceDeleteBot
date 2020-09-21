from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.keys import Keys

LOGIN = '###LOGIN'
PASSWORD = '#PASSWORD'
RUN_COMMAND = 'python3.7 bot.py'
SELENIUM_DRIVER = webdriver.Firefox(executable_path='./geckodriver.exe')
TIMEOUT = 10  # seconds

if __name__ == '__main__':
    driver = SELENIUM_DRIVER
    driver.get('https://www.pythonanywhere.com/login/')
    driver.find_element(By.ID, 'id_auth-username').send_keys(LOGIN)
    driver.find_element(By.ID, 'id_auth-password').send_keys(PASSWORD)
    driver.find_element(By.ID, 'id_next').click()
    WebDriverWait(driver, TIMEOUT).until(cond.visibility_of_element_located((By.CLASS_NAME, 'dashboard_recent_console')))
    driver.find_element(By.CLASS_NAME, 'dashboard_recent_console').click()
    driver.switch_to.frame("id_console")
    driver.switch_to.frame(0)
    driver.switch_to.frame(0)
    WebDriverWait(driver, TIMEOUT).until(cond.text_to_be_present_in_element((By.TAG_NAME, 'x-screen'), '$'))
    driver.find_element(By.TAG_NAME, 'x-screen').send_keys(RUN_COMMAND)
    driver.find_element(By.TAG_NAME, 'x-screen').send_keys(Keys.ENTER)
    WebDriverWait(driver, TIMEOUT).until(cond.text_to_be_present_in_element((By.TAG_NAME, 'x-screen'), '...'))
    driver.quit()
