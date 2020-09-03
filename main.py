from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

data = json.loads(os.environ.get("URL_AND_CREDS_JSON"))

for d in data["instances"]:
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(d["url"])
    driver.switch_to.frame("gsft_main")
    try:
        user = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_name"))
        )
        current_url = driver.current_url
        user.clear()
        user.send_keys(d["username"])
        passwd = driver.find_element_by_name("user_password")
        passwd.clear()
        passwd.send_keys(d["password"])
        login = driver.find_element_by_id("sysverb_login").click()
        WebDriverWait(driver, 15).until(EC.url_changes(current_url))
    except Exception as e:
        print(e)

    finally:
        print(driver.page_source)
        driver.close()
