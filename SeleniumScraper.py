from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
#options.add_argument("--headless") 
options.add_argument("--log-level=3")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options = options)  # Or use webdriver.Firefox() for Firefox

# Step 1: Set up the WebDriver
def getAwardsPage():


    driver.get("https://www.imdb.com/title/tt15398776/awards/?ref_=tt_awd")  # Replace with your target website URL
    bhie = "ipc-see-more__text"

    buttons = driver.find_elements(By.CLASS_NAME, bhie)  # Replace 'button-id' with the actual ID of the button
    for button in buttons:
        
        try:  
            driver.execute_script("arguments[0].scrollIntoView();", button)  
            time.sleep(0.7)
            button.click()
        except:
            continue

    time.sleep(2)
    html = driver.page_source
    html = BeautifulSoup(html, "html.parser")



    driver.quit()
    return html

    