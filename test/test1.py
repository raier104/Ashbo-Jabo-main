from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Start Chrome browser
driver = webdriver.Chrome()

# Open your Django site
driver.get("http://127.0.0.1:8000/")

# Wait a bit to load (better to use WebDriverWait later)
time.sleep(2)

# Example: Click a link
driver.find_element(By.LINK_TEXT, "Login").click()

# Example: Fill a login form
driver.find_element(By.NAME, "username").send_keys("tausif112")
driver.find_element(By.NAME, "password").send_keys("sadman106")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Wait and then close
time.sleep(10)
driver.quit()