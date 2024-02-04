import concurrent.futures

import pandas as pd
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

df = pd.read_json("test_data.json")
links = df.to_numpy()
full_url = "https://www.smogon.com"


def get_html(url):
    driver = setup_driver(url)

    # click the cookies button
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div>div>button:nth-of-type(2)")
            )
        )
    except TimeoutException:
        driver.refresh()

    button_element = driver.find_elements(
        By.CSS_SELECTOR, "div>div>button:nth-of-type(2)"
    )
    for button in button_element:
        button.click()

    # Wait until the page is loaded.
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "DexHeader "))
        )
    except TimeoutException:
        driver.refresh()

    # Click all of the export buttons on the page to load the set data into the website.
    button_elements = driver.find_elements(By.CLASS_NAME, "ExportButton")
    for buttons in button_elements:
        buttons.click()

    html = driver.page_source
    driver.quit()
    return html, url


def parse_html(html, url):
    data = HTMLParser(html)
    format = data.css_first(".PokemonPage-StrategySelector ul li span.is-selected")
    set = data.css_first(".BlockMovesetInfo div textarea")
    return {
        "pokemon": data.css_first("#PokemonPage-HeaderGrouper div h1").text(strip=True),
        "set": set.text(strip=True) if set is not None else None,
        "format": format.text(strip=True) if format is not None else None,
        "gen": url.split("/")[2],
    }


def setup_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor="http://192.168.1.97:4444", options=options
    )
    driver.get(f"{full_url}{url}")
    driver.maximize_window()
    return driver


urls = list(links.ravel())

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(get_html, urls))

df = pd.DataFrame()

for res in results:
    df = df._append(parse_html(res[0], res[1]), ignore_index=True)
df.to_json("please.json")
