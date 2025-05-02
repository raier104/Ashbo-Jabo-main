from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Start Chrome browser
driver = webdriver.Chrome()

#Open your Django site
driver.get("http://127.0.0.1:8000/")

#Let the page load
time.sleep(2)

#Login
driver.find_element(By.LINK_TEXT, "Login").click()
time.sleep(1)
driver.find_element(By.NAME, "username").send_keys("ovi")
driver.find_element(By.NAME, "password").send_keys("ovi")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(2)

#Navigate to Popular Destinations
driver.find_element(By.LINK_TEXT, "Popular Destinations").click()
print("Visited Popular Destinations page")
time.sleep(3)

#Navigate to About Us
driver.find_element(By.LINK_TEXT, "About us").click()
print("Visited About Us page")
time.sleep(3)

#Navigate to Bookings
driver.find_element(By.LINK_TEXT, "Booking").click()
print("Visited Bookings page")
time.sleep(2)

driver.find_element(By.NAME, "from_location").send_keys("Dhaka")
time.sleep(2)
driver.find_element(By.NAME, "to_location").send_keys("Chittagong")
time.sleep(2)
driver.find_element(By.NAME, "mode_of_travel").send_keys("Bus")
time.sleep(2)
driver.find_element(By.NAME, "departure_date").send_keys("05/03/2025")
time.sleep(2)
#driver.find_element(By.NAME, "number_of_passengers").send_keys("1")
#time.sleep(2)

driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(2)

select_links = driver.find_elements(By.LINK_TEXT, "Select")
if select_links:
    select_links[0].click()
    print("Clicked the first 'Select' link.")
else:
    print("No 'Select' link found.")
time.sleep(2)

select_links = driver.find_elements(By.LINK_TEXT, "Select this seat")
if select_links:
    select_links[0].click()
    print("Clicked the first 'Select' link.")
else:
    print("No 'Select' link found.")
time.sleep(5)

driver.find_element(By.NAME, "Name").send_keys("ovi")
time.sleep(2)
driver.find_element(By.NAME, "Address").send_keys("Jigatola")
time.sleep(2)
driver.find_element(By.NAME, "Phone Number").send_keys("Bus")
time.sleep(2)
driver.find_element(By.NAME, "Gender").send_keys("Male")
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(2)

#Close the browser
driver.quit()