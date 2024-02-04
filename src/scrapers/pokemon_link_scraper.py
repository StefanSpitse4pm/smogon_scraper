import concurrent.futures
from time import sleep

import pandas as pd
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

full_url = "https://www.smogon.com"

urls = [
    "/dex/rs/pokemon/",
    "/dex/ss/pokemon/",
    "/dex/sv/pokemon/",
    "/dex/dp/pokemon/",
    "/dex/bw/pokemon/",
    "/dex/gs/pokemon/",
    "/dex/xy/pokemon/",
    "/dex/rb/pokemon/",
    "/dex/sm/pokemon/",
]


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

    # wait untill the page is loaded
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "DexContent"))
    )
    # To get everything on the page we take the html that is on the page
    # Then scroll down some pixels check if we moved since last time.
    # If we didn't move it stops otherwise it repeates
    html = []
    start_height = driver.execute_script("return window.scrollY;")
    while True:
        sleep(0.3)
        html.append(driver.page_source)
        driver.execute_script("window.scrollBy(0, 100);")
        current_height = driver.execute_script("return window.scrollY;")

        if current_height == start_height:
            break
        start_height = current_height

    driver.quit()
    return html


def parse_html(html):
    data = HTMLParser(html)
    href_elements = data.css("a[href]")
    substrings = ["/pokemon/", "/dex/"]
    href_attributes = [
        element.attributes.get("href", "")
        for element in href_elements
        if all(
            substring in element.attributes.get("href", "") for substring in substrings
        )
    ]

    return href_attributes


def setup_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor="http://192.168.1.97:4444", options=options
    )
    driver.get(f"{full_url}{url}")
    driver.maximize_window()
    return driver


with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(get_html, urls))

links = []
for res in results:
    for part in res:
        links.append(parse_html(part))

unique_links_set = set(item for sublist in links for item in sublist)
unique_links_list = list(unique_links_set)
print(len(unique_links_list))
pokemon_link_df = pd.DataFrame(unique_links_list, columns=["links"])
pokemon_link_df.to_json("test_data.json")
