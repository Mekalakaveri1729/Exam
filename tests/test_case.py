import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
import time
@pytest.fixture
def setup_teardown():
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://127.0.0.1:5000")
    yield driver
    driver.quit()
def get_alert_text():
    alert=Alert(driver)
    text=alert.text
    alert.accept()
    return text    
def test_empty_username(setup_teardown):
    driver=setup_teardown
    driver.get("http://127.0.0.1:5000")
    driver.find_element(By.NAME,"username").clear()
    driver.find_element(By.NAME,"password").send_keys("Kaveri@1729")
    driver.find_element(By.NAME,"sb").click()
    time.sleep(1)
    alert_text=get_alert_text(driver)
    assert alert_text=="Username cannot be empty"
def test_empty_password(setup_teardown):
    driver=setup_teardown
    driver.get("http://127.0.0.1:5000")
    driver.find_element(By.NAME,"username").send_keys("Kaveri")
    driver.find_element(By.NAME,"password").clear() 
    driver.find_element(By.NAME,"sb").click()
    time.sleep(1)
    alert_text=get_alert_text(driver)
    assert alert_text=="Password cannot be empty"
def test_short_pwd(setup_teardown):
    driver=setup_teardown
    driver.get("http:/127.0.0.1.:5000")
    driver.find_element(By.NAME,"username").send_keys("Kaveri")
    driver.find_element(By.NAME,"password").send_keys("Kave")
    driver.find_element(By.NAME,"sb").click()
    time.sleep(1)
    alert_text=get_alert_text(driver)
    assert alert_text=="Password must be at least 6 characters long"
def test_valid_input(setup_teardown):
    driver=setup_teardown
    driver.get("http://127.0.0.1:5000")
    driver.find_element(By.NAME,"username").send_keys("Kaveri")
    driver.find_element(By.NAME,"password").send_keys("Kaveri@1729")
    driver.find_element(By.NAME,"sb").click()
    time.sleep(2)
    current_url=driver.current_url
    assert "/submit" in current_url,f'expected greeting page but find {current_url}'
    body_text=driver.fibd_element(By.TAG_NAME,"body").text
    assert "Hello,Kaveri!Welcome to the Website" in body_text,f'expected not matched with {body_text}'


