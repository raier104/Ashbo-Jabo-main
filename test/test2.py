from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class SignUpTest(unittest.TestCase):

    def setUp(self):
        # Initialize the WebDriver
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000"

    def test_sign_up_redirect_to_home(self):
        driver = self.driver
        # Test data
        username = "done104"
        email = "done104@gmail.com"
        password = "123done123"
        confirm_password = "123done123"
        role = "user"  

        # home page
        driver.get(self.base_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(5)  # Wait to visualize the page load

        # Click the signup link in the navbar
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up"))
        ).click()
        time.sleep(5)  

        # Fill out the signup form
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        driver.find_element(By.NAME, "username").send_keys(username)
        time.sleep(5)
        driver.find_element(By.NAME, "email").send_keys(email)
        time.sleep(5)
        driver.find_element(By.NAME, "password1").send_keys(password)
        time.sleep(5)
        driver.find_element(By.NAME, "password2").send_keys(confirm_password)
        time.sleep(5)
        role_dropdown = Select(driver.find_element(By.NAME, "role"))
        role_dropdown.select_by_value(role)

        # Submit the signup form
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)  # Wait to visualize form submission

        # Wait for redirection to the home page
        WebDriverWait(driver, 10).until(
            EC.url_to_be(f"{self.base_url}/home")
        )

        # redirection to the home page
        self.assertEqual(driver.current_url, f"{self.base_url}/home")

    def tearDown(self):
        # Close the browser
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()