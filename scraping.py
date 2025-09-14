from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
 
# Set up Chrome options
options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Start WebDriver
driver = webdriver.Chrome(options=options)
driver.get("https://www.kolabtree.com/find-an-expert?search=quantitative%20researcher")

# Accept cookies
try:
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cookiescript_accept"))
    )
    accept_button.click()
    print("Cookies accepted.")
except:
    print("No cookie popup found")
    WebDriverWait(driver, 10)

# Login button clicked
try:
    loginpage = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "signInmobile"))
    )
    driver.execute_script("arguments[0].click();", loginpage)
    print("Login Button clicked.")
except:
    print("Login Button not found or could not be clicked.")

# Enter login details
email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "txtLoginEmail"))
)
email_input.send_keys("omp2025aug@gmail.com")  # Replace with your email

password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "txtLoginPassword"))
)
password_input.send_keys("OMii@123")  # Replace with your password

login_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "btnLogin")))
login_button.click()
print("Login submitted successfully.")
browse_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/find-an-expert') and //span[contains(text(), 'Browse Experts')]]")
    )
)
browse_link.click()
print("Browse Experts link clicked.")

#############

wait = WebDriverWait(driver, 60)

# Get all "View Profile" buttons/links

button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.text-btn[data-target='#FullviewprofileModal']"))
)

# Click the button
button.click()
time.sleep(10)
info = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.row.profile-information"))
)
for element in info:
    print(element.text)












#when all profile extraction done on current page move to next page
"""   try:
        next_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.pagination-next"))  # adjust selector for next page button
        )
        next_button.click()
        time.sleep(3)  # wait for new page to load
    except:
        print("No next page found, scraping complete.")
        break"""


print("code run")
# Parse HTML
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

driver.quit()
