import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def create_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)

    driver.get('http://localhost:4200')

    return driver


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root


def test_execute_script_id():
    driver = create_driver()
    try:
        container = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'container')))
        shadow_root = expand_shadow_element(driver, container)

        no_radio = shadow_root.find_element(By.ID, "no")
        no_radio.click()
    finally:
        time.sleep(5)
        driver.quit()


def test_execute_script_xpath():
    driver = create_driver()
    try:
        container = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'container')))
        shadow_root = expand_shadow_element(driver, container)

        no_radio = shadow_root.find_element(By.XPATH, ".//app-select//input[@value='no']")
        no_radio.click()
    finally:
        time.sleep(10)
        driver.quit()
