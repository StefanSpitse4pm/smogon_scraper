import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

df = pd.read_json("data.json")
links = df.to_numpy()
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
    df = pd.DataFrame()
    for link in links:
        driver.get(f"{allowed_domain}{link[0]}")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "OtherGensList"))
        )
        button_elements = driver.find_elements(By.CLASS_NAME, "ExportButton")
        for buttons in button_elements:
            buttons.click()

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        set_divs = soup.select(".BlockMovesetInfo>div>textarea")
        pkmn_format = soup.select_one(
            ".PokemonPage-StrategySelector>ul>li>.is-selected"
        )
        if pkmn_format is not None:
            pkmn_format = pkmn_format.decode_contents()
        pkmn_gen = link[0].split("/")[2]
        pokemon_name = soup.select_one("#PokemonPage-HeaderGrouper>div>h1")
        pokemon_move_sets = []
        for div in set_divs:
            pokemon_move_sets.append(div.decode_contents())
        output_dict = {
            "pokemon": pokemon_name.decode_contents(),
            "sets": pokemon_move_sets,
            "format": pkmn_format,
            "gen": pkmn_gen,
        }

        df = df._append(output_dict, ignore_index=True)
    print(df)
    df.to_json("please.json")


get_pokemon_data(links)
