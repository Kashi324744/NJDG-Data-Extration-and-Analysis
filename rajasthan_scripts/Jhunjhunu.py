import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# Path to ChromeDriver
PATH = r"C:/Users/Ritika Sharma/OneDrive - JK LAKSHMIPAT UNIVERSITY/Major_project/chromedriver.exe"

# Excel File
EXCEL_PATH = r"C:\Users\Ritika Sharma\OneDrive - JK LAKSHMIPAT UNIVERSITY\Major_project\NJDG-Data-Extration-and-Analysis\rajasthan_scripts\Rajasthan_data.xlsx"

# State and District to process
STATE_NAME = "Rajasthan"
DISTRICT_NAME = "Jhunjhunu"

def setup_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    service = Service(PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

def save_to_excel(excel_path, sheet, data):
    """Save data to specific sheet in Excel"""
    columns = [
        "Date and Time", "Civil Cases", "Criminal Cases", "Total Cases", "Pre-Litigation / Pre-Trial",
        "Instituted in last month - Civil", "Instituted in last month - Criminal", "Instituted in last month - Total",
        "Disposal in last month - Civil", "Disposal in last month - Criminal", "Disposal in last month - Total",
        "Contested - Civil", "Contested - Criminal", "Contested - Total",
        "Uncontested - Civil", "Uncontested - Criminal", "Uncontested - Total",
        "Cases Listed Today - Civil", "Cases Listed Today - Criminal", "Cases Listed Today - Total",
        "Undated - Civil", "Undated - Criminal", "Undated - Total",
        "Excessive Dated Cases - Civil", "Excessive Dated Cases - Criminal", "Excessive Dated Cases - Total",
        "Cases Filed By Woman - Civil", "Cases Filed By Woman - Criminal", "Cases Filed By Woman - Total",
        "Cases Filed By Senior Citizen - Civil", "Cases Filed By Senior Citizen - Criminal", "Cases Filed By Senior Citizen - Total"
    ]

    while len(data) < len(columns):
        data.append(0)

    df = pd.DataFrame([data], columns=columns)

    with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
        try:
            existing_df = pd.read_excel(excel_path, sheet_name=sheet)
            df = pd.concat([existing_df, df], ignore_index=True)
        except Exception:
            pass
        df.to_excel(writer, sheet_name=sheet, index=False)

def extract_data(driver, name):
    """Extract case data from dashboard"""
    wait = WebDriverWait(driver, 30)
    data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

    try:
        # --- Summary cards ---
        categories = {
            "Civil Cases": "//h4[contains(text(), 'Civil Cases')]/following-sibling::span",
            "Criminal Cases": "//h4[contains(text(), 'Criminal Cases')]/following-sibling::span",
            "Total Cases": "//h4[contains(text(), 'Total Cases')]/following-sibling::span",
            "Pre-Litigation / Pre-Trial": "//h4[contains(text(), 'Pre-Litigation')]/following-sibling::span"
        }

        extracted_data = {}
        for category, xpath in categories.items():
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                extracted_data[category] = element.text.strip().replace(",", "")
            except:
                extracted_data[category] = "0"

        data.extend([
            extracted_data.get("Civil Cases", "0"),
            extracted_data.get("Criminal Cases", "0"),
            extracted_data.get("Total Cases", "0"),
            extracted_data.get("Pre-Litigation / Pre-Trial", "0")
        ])

        # --- Table cards ---
        table_cards = [
            "Instituted in last month",
            "Disposal in last month",
            "Cases Listed Today",
            "Undated",
            "Excessive Dated Cases",
            "Cases Filed By Woman",
            "Cases Filed By Senior Citizen"
        ]

        for case_type in table_cards:
            try:
                section = wait.until(EC.presence_of_element_located(
                    (By.XPATH, f"//span[contains(text(), '{case_type}')]/ancestor::div[contains(@class,'card')]")
                ))
                # Handle “Disposal in last month” specially (it contains contested & uncontested)
                if case_type == "Disposal in last month":
                    rows = section.find_elements(By.XPATH, ".//table//tr")
                    nums = []
                    for tr in rows:
                        tds = tr.find_elements(By.XPATH, ".//td/span[contains(@class,'h4')]")
                        if len(tds) == 3:
                            vals = [td.text.strip().replace(",", "") or "0" for td in tds]
                            nums.append(vals)

                    # Expected order: main disposal, contested, uncontested
                    main_disposal = nums[0] if len(nums) > 0 else ["0","0","0"]
                    contested = nums[1] if len(nums) > 1 else ["0","0","0"]
                    uncontested = nums[2] if len(nums) > 2 else ["0","0","0"]

                    data.extend(main_disposal)
                    data.extend(contested)
                    data.extend(uncontested)

                else:
                    # Normal extraction for all other sections
                    cells = section.find_elements(By.XPATH, ".//table//tr[2]/td")
                    vals = []
                    for td in cells[:3]:
                        raw = td.text.strip()
                        if not raw:
                            try:
                                raw = td.find_element(By.XPATH, ".//span|.//a").text.strip()
                            except:
                                raw = "0"
                        vals.append(raw.replace(",", "") if raw else "0")

                    while len(vals) < 3:
                        vals.append("0")
                    data.extend(vals[:3])

            except:
                # If section missing, fill with zeros
                if case_type == "Disposal in last month":
                    data.extend(["0"] * 9)  # main + contested + uncontested
                else:
                    data.extend(["0"] * 3)

    except Exception as e:
        print(f"Error extracting {name}: {e}")
        return None

    return data


def process_district(state, district, excel_path):
    driver = setup_driver()
    driver.set_window_size(1920, 1080)
    driver.get("https://njdg.ecourts.gov.in/njdg_v3/")
    wait = WebDriverWait(driver, 20)

    try:
        # Select state
        state_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "state_code_chosen")))
        state_dropdown.click()
        time.sleep(1)
        state_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{state}')]")))
        state_option.click()
        time.sleep(3)
        driver.execute_script("document.getElementById('state_code').dispatchEvent(new Event('change', { bubbles: true }));")
        time.sleep(2)

        go_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Go')]")))
        driver.execute_script("arguments[0].click();", go_button)
        time.sleep(5)

        # Select district
        district_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "dist_code_chosen")))
        district_dropdown.click()
        time.sleep(1)
        district_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[normalize-space(text())='{district}']")))
        district_option.click()
        time.sleep(2)
        driver.execute_script("document.getElementById('dist_code').dispatchEvent(new Event('change', { bubbles: true }));")
        time.sleep(2)

        go_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Go')]")))
        driver.execute_script("arguments[0].click();", go_button)
        time.sleep(6)

        # Extract & save
        data = extract_data(driver, district)
        if data:
            save_to_excel(excel_path, district, data)

    except Exception as e:
        print(f"Error processing {district}: {e}")
    finally:
        driver.quit()

process_district(STATE_NAME, DISTRICT_NAME, EXCEL_PATH)

print("\n District-level data saved in Rajasthan_data.xlsx!")
