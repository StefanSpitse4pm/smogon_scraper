import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selectolax.parser import HTMLParser

df = pd.read_json("test.json")
links = df.to_numpy()
full_url = "https://www.smogon.com"


def get_html(url):
    driver = setup_driver(url)

    # click the cookies button
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div>div>button:nth-of-type(2)")
        )
    )
    button_element = driver.find_elements(
        By.CSS_SELECTOR, "div>div>button:nth-of-type(2)"
    )
    for button in button_element:
        button.click()

    # Wait until the page is loaded.
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "DexHeader "))
    )

    # Click all of the export buttons on the page to load the set data into the website.
    button_elements = driver.find_elements(By.CLASS_NAME, "ExportButton")
    for buttons in button_elements:
        buttons.click()

    html = driver.page_source
    driver.quit()
    return html

def parse_html(html):
    data = HTMLParser(html)
    
    data.css_first(".BlockMovesetInfo>div>textarea")


def setup_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor="http://192.168.1.97:4444", options=options
    )
    driver.get(f"{full_url}{url}")
    driver.maximize_window()
    return driver


for url in links:
    print(url[0])
    get_html(url[0])
