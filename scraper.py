from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)


allowed_domain = "https://www.smogon.com"
start_url = "https://www.smogon.com/dex/sv/pokemon/"
driver.maximize_window()
driver.get(start_url)

