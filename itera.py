from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# === Setup Chrome Options ===
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# === Start WebDriver ===
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# === Navigate to Target Page ===
driver.get("https://www.kolabtree.com/find-an-expert?search=quantitative%20researcher")

# Accept cookies
try:
    accept_button = wait.until(EC.element_to_be_clickable((By.ID, "cookiescript_accept")))
    accept_button.click()
    print("Cookies accepted.")
except:
    print("No cookie popup found")

# Login button clicked
try:
    loginpage = wait.until(EC.presence_of_element_located((By.ID, "signInmobile")))
    driver.execute_script("arguments[0].click();", loginpage)
    print("Login Button clicked.")
except:
    print("Login Button not found or could not be clicked.")

# Enter login details
email_input = wait.until(EC.presence_of_element_located((By.ID, "txtLoginEmail")))
email_input.send_keys("omp2025aug@gmail.com")  # Replace with your email
time.sleep(1)

password_input = wait.until(EC.presence_of_element_located((By.ID, "txtLoginPassword")))
password_input.send_keys("OMii@123")  # Replace with your password

login_button = wait.until(EC.presence_of_element_located((By.ID, "btnLogin")))
time.sleep(1)
login_button.click()
print("Login submitted successfully.")

# Click Browse Experts
try:
    browse_link = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href, '/find-an-expert')]//span[contains(text(), 'Browse Experts')]")
        )
    )
    browse_link.click()
    print("Browse Experts link clicked.")
except:
    print("Browse Experts link not found.")

# === Pagination Loop ===
while True:
    # Wait for all profile buttons
    profile_buttons = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a.text-btn[data-target='#FullviewprofileModal']")
        )
    )

    # Only keep "VIEW FULL PROFILE" buttons
    profile_buttons = [btn for btn in profile_buttons if "FULL" in btn.text.upper()]
    print(f"Found {len(profile_buttons)} unique profiles on this page.")

    for i in range(len(profile_buttons)):
        try:
            # Re-query buttons each time (DOM refreshes after modal close)
            profile_buttons = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "a.text-btn[data-target='#FullviewprofileModal']")
                )
            )
            profile_buttons = [btn for btn in profile_buttons if "FULL" in btn.text.upper()]
            button = profile_buttons[i]

            # Scroll & click
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)

            # Wait for modal to load
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.row.profile-information")))

            print(f"\n----- PROFILE {i+1} -----")

            # ✅ Extract Name + Link
            try:
                profile_anchor = driver.find_element(By.CSS_SELECTOR, "a.profile-new-page")
                profile_name = profile_anchor.text.strip()
                profile_link = profile_anchor.get_attribute("href")
            except:
                profile_name, profile_link = "N/A", "N/A"

            # ✅ Extract profile info (excluding Publications)
            headers = driver.find_elements(By.CSS_SELECTOR, "div.section-header")
            sections = driver.find_elements(By.CSS_SELECTOR, "div.row.profile-information")

            profile_data = {
                "name": profile_name,
                "link": profile_link,
                "sections": {}
            }

            # Pair headers with sections
            for header, section in zip(headers, sections):
                try:
                    parent_id = section.find_element(By.XPATH, "./ancestor::div[1]").get_attribute("id")
                    if parent_id and "publication" in parent_id.lower():
                        continue
                except:
                    pass

                header_text = header.text.strip()
                section_text = section.text.strip()
                profile_data["sections"][header_text] = section_text

            # ✅ Print (later you can insert this dict into MongoDB)
            print(profile_data)

            # Close modal
            back_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.profile-back-btn.proximanova-semibold-18px"))
            )
            driver.execute_script("arguments[0].click();", back_button)
            time.sleep(2)

        except Exception as e:
            print(f"Error reading profile {i+1}: {e}")
            continue

    # === Next Page ===
    try:
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="javascript:void(0)" and normalize-space(text())=">"]'))
        )
        
        driver.execute_script("arguments[0].click();", next_button)
        print("Moving to next page...\n")
        time.sleep(25)
    except:
        print("No more pages. Scraping complete.")
        break

# === Close Browser ===
driver.quit()
