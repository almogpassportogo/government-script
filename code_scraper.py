import base64
import csv
import json
import os
import sys
import time
import requests
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from twocaptcha import TwoCaptcha
from webdriver_manager.chrome import ChromeDriverManager


def api(data):
    webhook_url_2 = "https://hook.eu1.make.com/g3at8whhmxefm4n26ojkgncdbrrbe4jh"
    try:
        # Send a POST request to the second webhook
        response_2 = requests.post(webhook_url_2, json=data)
        print(response_2.content)
        # Check the response from the second webhook
        if response_2.status_code == 200:
            print("Webhook 2: Request sent successfully.")
        else:
            print("Webhook 2: Request failed with status code:", response_2.status_code)
    except Exception as e:
        print(e)


def solve_captcha():
    # library url: https://github.com/My-kal/2Captcha
    result = None

    sitekey="6LeDhLIZAAAAAA0Hy0VLO7wOeB5aNIibYM-aQ2_3"
    api_key = 'ad836997350d2f9ea35e60f0eb512567'
    solver = TwoCaptcha(api_key)
    balance = solver.balance()
    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url='https://nacionalidade.justica.gov.pt/'
        )

    except Exception as e:
        print("Failed to solve captcha")
        sys.exit(e)
        
    print(result)
    return result['code']


def start_browser():
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')  # Disables the webdriver flag
    # options.add_argument("--disable-web-security")  # disable same-origin policy
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-sandbox")  # Bypass OS-level security, VERY UNSAFE
    options.add_argument("--disable-popup-blocking")  # Allows popups
    options.add_argument("--disable-infobars")  # Prevent infobar from coming
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--remote-debugging-port=9222")
    # Set preferences for automatic translation without any prompts
    prefs = {
        "translate": {"enabled": "true"},
        "translate_blocked": "false",
        "translate_whitelists": {"fr": "en"}
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument(r'--load-extension=' + os.getcwd() + r'\extensions\3.3.4_0_1')
    # options.add_argument(r"--load-extension=C:\Users\kk\Downloads\scrapit_2021\3.3.4_0")
    # input("load ext ")
    # use the derived Chrome class that handles prefs
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    time.sleep(2)
    driver.get("https://nacionalidade.justica.gov.pt/")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    driver.get("chrome-extension://ifibfemgeogfhoebkmokieepdoobkbpo/options/options.html")
    time.sleep(2)
    driver.find_element("name", "apiKey").send_keys("ad836997350d2f9ea35e60f0eb512567")
    time.sleep(2)
    driver.find_element("xpath", "//button[text()='Login']").click()
    time.sleep(2)
    driver.switch_to.alert.accept()
    # self.driver.find_element("tag name","body").send_keys(Keys.ENTER)
    time.sleep(2)
    for e in driver.find_elements("xpath", "//div[@class='switch']//input[contains(@name,'auto')]")[:4]:
        action = ActionChains(driver)
        action.move_to_element(e).click().perform()
        time.sleep(0.7)

    # driver.maximize_window()
    return driver


def Government(code, driver,output_folder):
    driver.get("https://nacionalidade.justica.gov.pt/")
    time.sleep(3)
    code_input = driver.find_element(By.XPATH, '//input[@placeholder="xxxx-xxxx-xxxx"]')
    code_input.send_keys(code)
    try:
        # Wait for the elements with the specified condition
        # wait = WebDriverWait(driver, 120) ----> this is the original wait time
        # result = solve_captcha()
        # driver.find_element(By.XPATH,
        #     "//textarea[@class='g-recaptcha-response']").click()
        
        # driver.find_element(By.XPATH,
        #     "//textarea[@class='g-recaptcha-response']").send_keys(result)
        # captcha.send_keys(result)
        
        wait = WebDriverWait(driver, 40)
        
        time.sleep(2)
          
        steps = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH,
            "//section[@class='step-indicator']/div[contains(@class,'step')]")))
        
        time.sleep(2)
        notes = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH,
            "(//div[@class='container'])[3]")))
        
        OfficeStation = driver.find_element(By.CSS_SELECTOR, "body > div:first-child > div:nth-child(2)")
            
        note = notes[0].text.casefold()
        
        if len(steps) == 7:
            try:
                
                last_active3 = None
                last_active1 = None
                curr_user_step = None
                for step in reversed(steps):
                    if "active3" in step.get_attribute("class"):
                        last_active3 = step
                        step_text = step.text[2:]
                        break
                    elif "active1" in step.get_attribute("class"):
                        last_active1 = step
                        step_text = step.text[2:]
                        break

                if last_active3 is not None:
                    curr_user_step =  last_active3
                elif last_active1 is not None:
                    curr_user_step = last_active1 
                
                    
                class_names = curr_user_step.get_attribute("class").split()
                if class_names[2] == "active3":
                    step = class_names[1][4:]
                    step +="B"
                elif class_names[2] == "active1":
                    step = class_names[1][4:]
                    step +="A"
            
            except Exception as e:
                print("An error occurred: {e}")      
      
        info = {
            "code": code,
            "step": step,
            "step_title": step_text,
            "text": note,
            "station": OfficeStation.text
        }
        
        
    except Exception as e:
        info = {
            "code": code,
            "step": "",
            "step_title": "",
            "text": "Error",
            "station": ""
        }
    print("--------------------------------------------------------------------")
    print("script finished, output: ", info)
    print("--------------------------------------------------------------------")

    return info
    


input_file_path = input("Enter input file path : ")

output_folder = input("Enter output folder path : ")
driver = start_browser()


with open(input_file_path, "r", encoding="cp437", errors='ignore') as input_file:
    code = [code.strip("\n") for code in input_file.readlines()]
    for code in code:
        if code==0 or code=="0":
            continue
        result = Government(code, driver,output_folder)

        if result['step'] != "":
            with open(output_folder+r"/output.csv", "a",encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([result['code'], result['step'], result['step_title'], result['text'], result['station']])
            # api(result)
        else :
            second_result = Government(code, driver,output_folder)
            if result['step'] != "":
                with open(output_folder+r"/output.csv", "a",encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([result['code'], result['step'], result['step_title'], result['text'], result['station']])
                # api(result)

            else:
                continue

# code_input = "9605-1349-2252"
