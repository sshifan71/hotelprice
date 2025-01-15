from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_booking(place, checkin, checkout):
    # Set up the WebDriver
    driver = webdriver.Chrome()  # Use your browser's WebDriver
    driver.maximize_window()
    
    try:
        # Open booking.com
        driver.get("https://www.booking.com/")

        try:
            pop_up_close_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "button[aria-label='Dismiss sign in information.']"))
            )
            pop_up_close_button.click()
  
        except Exception as e:
            print("No pop-up detected or unable to locate it.")
        
        # Input place
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, ":rh:"))
        )
        search_box.send_keys(place)


        
        # Input check-in date
        checkin_box = driver.find_element(By.XPATH, '//button[@data-testid="date-display-field-start"]')
        checkin_box.click()
        time.sleep(1)
        for i in range(2):
        #calander turner
            try:    
                calander_turner = driver.find_element(By.XPATH, '//button[@aria-label="Next month"]')
                calander_turner.click()
            except Exception as e:
                print("Error just happend", str(e))


        checkin_date = driver.find_element(By.XPATH, f"//span[@aria-label='{checkin}']")
        checkin_date.click()
        
        # Input check-out date
        checkout_date = driver.find_element(By.XPATH, f"//span[@aria-label='{checkout}']")
        checkout_date.click()
        
        # Submit search
        search_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        search_button.click()
        
        # Wait for search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="property-card"]'))
        )
        
        # Scrape hotel names and prices
        hotels = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
        for hotel in hotels:
            try:
                name = hotel.find_element(By.XPATH, '//div[@data-testid="title"]').text
                price = hotel.find_element(By.XPATH, '//span[@data-testid="price-and-discounted-price"]').text
                print(f"Hotel: {name}, Price: {price}")
            except Exception as e:
                continue  # Skip if name or price is not found

    finally:
        driver.quit()

# Input data
#place = input("Enter the destination: ")
#checkin = input("Enter check-in date (YYYY-MM-DD): ")
#checkout = input("Enter check-out date (YYYY-MM-DD): ")
place = 'Makkah'
checkin = '15 March 2025'
checkout = '5 April 2025'
scrape_booking(place, checkin, checkout)
