from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login_success(driver): #OK
    # driver = webdriver.Chrome()
    driver.get("https://opensource-demo.orangehrmlive.com/")
    # driver.maximize_window()
    #time.sleep(10)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.TAG_NAME, "button").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("dashboard")
    )
    assert "dashboard" in driver.current_url

    #driver.quit()


def test_forgot_password_success(driver): #OK
    # driver = webdriver.Chrome()
    driver.get("https://opensource-demo.orangehrmlive.com/")
    # driver.maximize_window()

    forgot_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "orangehrm-login-forgot-header"))
    )
    forgot_link.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("requestPasswordResetCode")
    )
    assert "requestPasswordResetCode" in driver.current_url

    #driver.quit()

def test_original_sitelink(driver): #OK
    # driver = webdriver.Chrome()
    driver.get("https://opensource-demo.orangehrmlive.com/")
    # driver.maximize_window()

    original_sitelink = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "OrangeHRM, Inc"))
    )

    #check for corrent link
    href = original_sitelink.get_attribute('href')
    assert href == "http://www.orangehrm.com/"

    original_sitelink.click()

    #switch to new window
    driver.switch_to.window(driver.window_handles[1])

    assert "orangehrm.com" in driver.current_url

    #driver.quit()

social_links = {
    "linkedin": "https://www.linkedin.com/company/orangehrm",
    "facebook": "https://www.facebook.com/OrangeHRM/",
    "twitter": "https://twitter.com/orangehrm",
    "youtube": "https://www.youtube.com/c/OrangeHRMInc"
}

@pytest.mark.parametrize("platform, expected_url", social_links.items())
def test_social_links(driver, platform, expected_url):
    # driver = webdriver.Chrome()
    driver.get("https://opensource-demo.orangehrmlive.com/")

    #use CSS classname to locate the icon
    icon_selector = f"a[href*='{platform}']"

    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, icon_selector))
    )

    href = link.get_attribute("href")
    assert expected_url in href

    #check for opening of new tab
    assert link.get_attribute("target") == "_blank"

dummy_usernames = {
    ""     :"Required", #No input
    "Wrong":"None"      #might not return error
}

@pytest.mark.parametrize("username, expected_error_message", dummy_usernames.items())
def test_login_error(driver, username, expected_error_message):
    driver.get("https://opensource-demo.orangehrmlive.com/")

    #find username input field
    input_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(By.NAME, "username")
    )
    input_field.send_keys(username)

    #click login button
    login_button = driver.find_element(By.TAG_NAME, "button")
    login_button.click()

    if expected_error_message:
        #wait
        error_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "oxd-input-field-input-message"))
        )
        assert expected_error_message in error_element.text
    else:
        #If error not thrown, make sure we in same page
        WebDriverWait(driver, 10).until(
            EC.url_contains("opensource-demo.orangehrm")
        )


