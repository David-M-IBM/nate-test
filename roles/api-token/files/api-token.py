import time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_api_token(arguments):

    # Initialize Variables
    username = arguments[1]
    password = arguments[2]
    login_url = arguments[3]
    endpoint = '/#/config/team/accessControl/apiTokens'
    api_url = login_url + endpoint
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=chrome_options)
    timeout = 30

    # Load Instana page
    while True:
        try:
            driver.get(login_url)
            WebDriverWait(driver, timeout).until(EC.title_contains("Sign in"))
            break
        except TimeoutException:
                driver.refresh()
                time.sleep(10)
        except Exception as e:
            if "err_connection_closed" in str(e).lower():
                 driver.refresh()
                 time.sleep(10)
            else:
                break
        
    # Login to Instana
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, 'email')))
    email_field = driver.find_element(By.ID, 'email')
    email_field.send_keys(username)
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, 'password')))
    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//button[@type="submit"]')))
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()

    # Click Go to Instana button, if the first time login page exists
    while True:
        try: 
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(., "Go to Instana")]')))
            instana_button = driver.find_element(By.XPATH, '//button[contains(., "Go to Instana")]')
            instana_button.click()
            break
        except TimeoutException:
             WebDriverWait(driver, timeout).until(EC.title_contains("Home"))
             break

    # Go to Settings > Team Settings > API Tokens
    driver.get(api_url)
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[text()="Add API Token"]')))
    api_tokens_button = driver.find_element(By.XPATH, '//*[text()="Add API Token"]')
    api_tokens_button.click()

    # Select Configuration of applications permission
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "permission-canConfigureApplications")))
    website_checkbox = driver.find_element(By.ID, "permission-canConfigureApplications")
    website_div = website_checkbox.find_element(By.XPATH, "./ancestor::td")
    website_div.click()

    # Select Website monitoring configuration permission
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "permission-canConfigureEumApplications")))
    website_checkbox = driver.find_element(By.ID, "permission-canConfigureEumApplications")
    website_div = website_checkbox.find_element(By.XPATH, "./ancestor::td")
    website_div.click()

    # Reveal API Token
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, 'in-settings-form-group')))
    reveal_token_div = driver.find_element(By.CLASS_NAME, 'in-settings-form-group')
    reveal_token_button = reveal_token_div.find_element(By.TAG_NAME, 'button')
    driver.execute_script("window.scrollTo(0, 0);")
    reveal_token_button.click()

    # Set API Token value
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "api-token-accessGrantingToken")))
    api_token_label = driver.find_element(By.ID, "api-token-accessGrantingToken")
    WebDriverWait(driver, timeout).until(lambda driver: '*****' not in api_token_label.text)
    api_token = api_token_label.text

    # Save API Token
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[text()="Save"]')))
    save_button = driver.find_element(By.XPATH, '//*[text()="Save"]')
    save_button.click()
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[text()="Add API Token"]')))
    driver.quit()

    # Return API Token
    return api_token

print(get_api_token(sys.argv))
