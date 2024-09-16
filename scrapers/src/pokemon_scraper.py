import concurrent.futures
import time
from time import sleep

import pandas as pd
from config.settings import Settings
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine

start_time = time.time()
df = pd.read_json("..//test_data.json")
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
        click_button(driver, button)

    # Wait until the page is loaded.
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "DexHeader "))
        )
    # if it never loads refresh chrome
    except TimeoutException:
        print("couldn't load page refreshing... ")
        driver.refresh()

    # Click all of the export buttons on the page to load the set data into the website.
    button_elements = driver.find_elements(By.CLASS_NAME, "ExportButton")
    for button in button_elements:
        click_button(driver, button)

    html = driver.page_source
    parsed_data = parse_html(html, url)
    driver.quit()
    return parsed_data


def click_button(driver, button):
    try:
        button.click()
    except ElementClickInterceptedException:
        print("couldn click export button waiting for it...")
        sleep(10)
        try:
            button.click()
        except ElementClickInterceptedException:
            print("still couldn't click it refreshing...")
            driver.refresh()
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div>div>button:nth-of-type(2)")
                )
            )
            button.click()


def parse_html(html, url):
    data = HTMLParser(html)
    format = data.css_first(".PokemonPage-StrategySelector ul li span.is-selected")
    set = data.css(".BlockMovesetInfo div textarea")
    name = data.css_first("#PokemonPage-HeaderGrouper div h1")
    return {
        "pokemon_name": (
            data.css_first("#PokemonPage-HeaderGrouper div h1").text(strip=True)
            if name is not None
            else None
        ),
        "pokemon_set": set.text(strip=True) if set is not None else None,
        "format": format.text(strip=True) if format is not None else None,
        "gen": url.split("/")[2],
    }


def setup_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
    driver.get(f"{full_url}{url}")
    driver.maximize_window()
    return driver


def insert_to_database(data):
    engine = create_engine(Settings.DB_URI)
    df = pd.DataFrame([data])
    df.to_sql(name="pokemon", con=engine, if_exists="append", index=False)


urls = list(links.ravel())

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(get_html, urls))

for res in results:
    insert_to_database(res)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time / 60} minutes")
