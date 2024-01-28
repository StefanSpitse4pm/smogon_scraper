import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

df = pd.read_json("data.json")
links = df.to_numpy()
print(type(links))
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

allowed_domain = "https://www.smogon.com"
start_url = "https://www.smogon.com/dex/"
driver.get(start_url)
driver.maximize_window()

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

# click the cookies button
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div>div>button:nth-of-type(2)"))
)
button_element = driver.find_elements(By.CSS_SELECTOR, "div>div>button:nth-of-type(2)")
for button in button_element:
    button.click()


def get_pokemon_data(links):
    global driver
    for link in links:
        driver.get(f"{allowed_domain}{link[0]}")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "DexHeader "))
        )


get_pokemon_data(links)
