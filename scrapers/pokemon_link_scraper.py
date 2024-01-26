from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)


allowed_domain = "https://www.smogon.com"
start_url = "https://www.smogon.com/dex/"
driver.maximize_window()
driver.get(start_url)

# grabs all links on the start page
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
links = soup.select("a[href]")

# Clicks the cookies button
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div>div>button:nth-of-type(2)"))
)
button_element = driver.find_elements(By.CSS_SELECTOR, "div>div>button:nth-of-type(2)")
for button in button_element:
    button.click()


def getDexLinks(relative_links: list):
    # Gets all the pokemon links.
    for link in relative_links:
        if "/dex/" and "/pokemon/" in link.get("href"):
            source_link = link.get("href")
            global driver
            driver.get(f"{allowed_domain}{source_link}")

            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "DexContent"))
            )

            temp_pokemon = []
            start_height = driver.execute_script("return window.scrollY;")
            while True:
                # This code is here so beatifulsoup updates when the page is loaded
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")

                links = soup.select("a[href]")
                for link in links:
                    if "/pokemon/" in link.get("href"):
                        temp_pokemon.append(link.get("href"))
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "PokemonAltRow-name")
                    )
                )
                driver.execute_script("window.scrollBy(0, 100);")
                current_height = driver.execute_script("return window.scrollY;")

                if current_height == start_height:
                    break

                start_height = current_height
    print(temp_pokemon)


links = [links[15]]
getDexLinks(links)
