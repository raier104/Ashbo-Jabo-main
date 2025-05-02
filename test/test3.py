import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    BASE_URL   = "http://127.0.0.1:8000"
    SIGNUP_URL = f"{BASE_URL}/sign_up/"

    LOGIN_URL  = f"{BASE_URL}/log_in/"


    USERNAME   = "ashbojabo"

    EMAIL      = "ashbojabo@gmail.com"

    PASSWORD   = "123ashbo123"

    ROLE       = "user"


    FROM_INDEX  = 1

    TO_INDEX    = 2

    MODE_INDEX  = 1

    DEPART_DATE = "05/03/2025"

    PAX_COUNT   = "1"


    PMETHOD = "credit_card"

    AMOUNT  = "1000.00"

    TXN_ID  = "TXN20250502"

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(SIGNUP_URL)
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        time.sleep(2)
        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        time.sleep(2)
        driver.find_element(By.NAME, "password1").send_keys(PASSWORD)
        time.sleep(2)
        driver.find_element(By.NAME, "password2").send_keys(PASSWORD)
        Select(driver.find_element(By.NAME, "role")).select_by_value(ROLE)
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))).click()
        time.sleep(2)

        driver.get(LOGIN_URL)
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        time.sleep(2)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        time.sleep(2)
        # Navigate to Popular Destinations
        driver.find_element(By.LINK_TEXT, "Popular Destinations").click()
        print("Visited Popular Destinations page")
        time.sleep(3)

        # Navigate to About Us
        driver.find_element(By.LINK_TEXT, "About us").click()
        print("Visited About Us page")
        time.sleep(3)
        driver.get(BASE_URL)
        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Book Bus"))).click()
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'Book Your Ticket')]")))
        time.sleep(2)

        Select(driver.find_element(By.ID, "from_location")).select_by_index(FROM_INDEX)
        time.sleep(2)
        Select(driver.find_element(By.ID, "to_location")).select_by_index(TO_INDEX)
        time.sleep(2)
        Select(driver.find_element(By.ID, "mode_of_travel")).select_by_index(MODE_INDEX)
        time.sleep(2)
        dep = driver.find_element(By.ID, "departure_date"); dep.clear(); dep.send_keys(DEPART_DATE)
        time.sleep(2)
        pax = driver.find_element(By.ID, "number_of_passengers"); pax.clear(); pax.send_keys(PAX_COUNT)
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='form-group']/button[text()='Next']"))).click()
        time.sleep(2)


        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".transport-option a")))
        time.sleep(2)
        transport_links = driver.find_elements(By.CSS_SELECTOR, ".transport-option a")
        time.sleep(2)
        for i in range(len(transport_links)):
            transport_links = driver.find_elements(By.CSS_SELECTOR, ".transport-option a")
            time.sleep(2)
            transport_links[i].click()
            time.sleep(2)

            wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            time.sleep(2)
            seats = driver.find_elements(By.CSS_SELECTOR, ".seat-option a")
            time.sleep(2)
            if seats:
                seats[0].click()
                break
            driver.back()
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".transport-option a")))
        else:
            raise Exception("No available seats on any transport option")
        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Ashbo Jabo")
        time.sleep(2)
        driver.find_element(By.NAME, "address").send_keys("74/A, Green Road")
        time.sleep(2)
        driver.find_element(By.NAME, "phone_number").send_keys("0123456789")
        time.sleep(2)
        Select(driver.find_element(By.NAME, "gender")).select_by_value("Male")
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='form-group']/button[text()='Next']"))).click()
        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.NAME, "payment_method")))
        time.sleep(2)
        Select(driver.find_element(By.NAME, "payment_method")).select_by_value(PMETHOD)
        time.sleep(2)
        driver.find_element(By.NAME, "amount_paid").send_keys(AMOUNT)
        time.sleep(2)
        driver.find_element(By.NAME, "transaction_id").send_keys(TXN_ID)
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Payment Successful')]")))
        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Print Receipt"))).click()
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#receipt")))
        time.sleep(2)

        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})["data"]
        with open("receipt.pdf", "wb") as f:
            f.write(base64.b64decode(pdf_data))
        time.sleep(2)

        driver.get(BASE_URL)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))).click()

        time.sleep(4)


    finally:
        driver.quit()

if __name__ == "__main__":
    main()
