from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Start Chrome browser
driver = webdriver.Chrome()

# Open your Django site
driver.get("http://127.0.0.1:8000/")

# Let the page load
time.sleep(2)

# Login
driver.find_element(By.LINK_TEXT, "Login").click()
time.sleep(1)
driver.find_element(By.NAME, "username").send_keys("ovi")
driver.find_element(By.NAME, "password").send_keys("ovi")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(2)

# Navigate to Bookings
driver.find_element(By.LINK_TEXT, "Booking").click()
print("Visited Bookings page")
time.sleep(2)

# Navigate to Popular Destinations
driver.find_element(By.LINK_TEXT, "Popular Destinations").click()
print("Visited Popular Destinations page")
time.sleep(2)

# Navigate to About Us
driver.find_element(By.LINK_TEXT, "About us").click()
print("Visited About Us page")
time.sleep(2)

# Close the browser
driver.quit()
