# 🕸️ Extract jobs from RemoteOK HTML
import time
import sys
import os
from typing import Dict, List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Add the project root to the Python path to allow for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

 # Import configuration
from config import BASE_URL, SEARCH_KEYWORD, LOCATION, MIN_SALARY

# --- Selectors (Constants) ---
# Using constants for selectors makes them easier to update if the site changes.
LOCATION_BUTTON_SELECTOR = ".location-filter-input"
LOCATION_RESULTS_SELECTOR = ".location-filter-results"
SEARCH_INPUT_SELECTOR = ".search-filter-input"
SALARY_FILTER_SELECTOR = ".salary-filter"
SALARY_SLIDER_SELECTOR = ".salary-filter-input"
JOB_ROW_SELECTOR = "tr.job"  # Selector for the entire job row

def setup_driver() -> webdriver.Chrome:
    """Sets up the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run without opening a browser window
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def apply_filters(driver: webdriver.Chrome, keyword: str, location: str, min_salary: int):
    """Navigates to the site and applies search, location, and salary filters."""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    try:

        # --- Location Filter ---
        print(f"Applying location filter: {location}")
        location_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, LOCATION_BUTTON_SELECTOR)))
        location_button.click()

        location_dropdown = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, LOCATION_RESULTS_SELECTOR)))
        location_options = location_dropdown.find_elements(By.TAG_NAME, "div")

        found_location = False
        for element in location_options:
            if element.text == location:
                element.click()
                found_location = True
                print("Location filter applied.")
                break
        if not found_location:
            print(f"Warning: Location '{location}' not found.")
            ActionChains(driver).move_by_offset(1, 1).click().perform() # Click away to close
        time.sleep(1)  # Wait for UI to settle after filter

        # --- Search Filter ---
        print(f"Applying search keyword: {keyword}")
        search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_INPUT_SELECTOR)))
        search_box.click()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        print("Search keyword applied.")
        time.sleep(2)  # A short static sleep is often okay after a search to allow results to refresh.

        # --- Salary Filter ---
        print(f"Applying minimum salary: ${min_salary:,}")
        salary_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SALARY_FILTER_SELECTOR)))
        salary_box.click()

        draggable = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SALARY_SLIDER_SELECTOR)))
        set_slider_value(driver, draggable, min_salary)
        print("Salary filter applied.")
        time.sleep(2)  # Wait for filter to apply

    except TimeoutException as e:
        print(f"Error applying filters: A timeout occurred while waiting for an element. {e}")
        raise
    except NoSuchElementException as e:
        print(f"Error applying filters: Could not find an element. {e}")
        raise

def set_slider_value(driver: webdriver.Chrome, slider_element: WebElement, target_salary: int):
    """Drags the salary slider to a target value using a calculated offset."""
    if not (0 <= target_salary <= 250000):
        print(f"Warning: target_salary {target_salary} is outside the 0-250k range. Clamping.")
        target_salary = max(0, min(target_salary, 250000))

    # This is a linear interpolation mapping salary (0-250k) to a pixel offset (-120 to 120)
    # The slider's center is $120k (0px offset).
    offset = (target_salary / 250000) * 240 - 120

    print(f"Calculated slider offset: {offset:.2f}px for ${target_salary:,}")
    ActionChains(driver).drag_and_drop_by_offset(slider_element, offset, 0).perform()

def scrape_jobs(html: str) -> List[Dict[str, str]]:
    """Parses the HTML and extracts job details for each listing."""
    soup = BeautifulSoup(html, 'lxml')
    jobs = []
    job_rows = soup.select(JOB_ROW_SELECTOR)
    print(f"Found {len(job_rows)} job listings on the page.")

    for job_row in job_rows:
        if 'data-id' not in job_row.attrs:
            continue

        title_element = job_row.select_one("h2[itemprop='title']")
        company_element = job_row.select_one("h3[itemprop='name']")
        location_element = job_row.select_one(".location")
        salary_element = job_row.select_one(".salary")

        title = title_element.get_text(strip=True) if title_element else "N/A"
        company = company_element.get_text(strip=True) if company_element else "N/A"
        relative_link = job_row.get('data-url', '')
        apply_link = f"{BASE_URL.rstrip('/')}{relative_link}" if relative_link else "N/A"
        location = location_element.get_text(strip=True).replace('\n', ' ').strip() if location_element else "N/A"
        salary = salary_element.get_text(strip=True) if salary_element else "N/A"

        job_data = {
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "apply_link": apply_link,
        }
        jobs.append(job_data)
    return jobs

def scrape_remoteok() -> List[Dict[str, str]]:
    """
    Orchestrates the RemoteOK scraping process: launches browser, applies filters,
    scrapes job data, and returns it.
    """
    driver = None
    jobs = []
    try:
        driver = setup_driver()
        apply_filters(driver, SEARCH_KEYWORD, LOCATION, MIN_SALARY)

        print("Waiting for page to load with all jobs...")
        # Wait for at least one job row to be present after filtering. This is more reliable.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, JOB_ROW_SELECTOR))
        )
        html = driver.page_source
        jobs = scrape_jobs(html)
    except Exception as e:
        print(f"An error occurred during the scraping process: {e}")
        raise  # Re-raise the exception so the main function can handle it.
    finally:
        if driver:
            print("Closing browser.")
            driver.quit()
    return jobs