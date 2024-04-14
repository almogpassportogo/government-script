import base64
import csv
import json
import os
import re
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytz
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

# pythongovernmentscript123! ---> password for email
# ridx zani sdxa hxrb  ---> app password

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

api_key = "ad836997350d2f9ea35e60f0eb512567"
solver = TwoCaptcha(api_key)
balance = solver.balance()
print("remaining Balance: ", balance)

server.login("pythongovernmentscript@gmail.com", "ridx zani sdxa hxrb")

def api(data):
    webhook_url_2 = "https://hook.eu1.make.com/g3at8whhmxefm4n26ojkgncdbrrbe4jh"
    try:
        # Send a POST request to the second webhook
        response_2 = requests.post(webhook_url_2, json=data)
        # print(response_2.content)
        # Check the response from the second webhook
        # if response_2.status_code == 200:
        #     print("Webhook 2: Request sent successfully.")
        # else:
        #     print("Webhook 2: Request failed with status code:", response_2.status_code)
    except Exception as e:
        print(e)


def solve_captcha():
    # library url: https://github.com/My-kal/2Captcha
    result = None

    sitekey = "6LeDhLIZAAAAAA0Hy0VLO7wOeB5aNIibYM-aQ2_3"
    api_key = "ad836997350d2f9ea35e60f0eb512567"
    solver = TwoCaptcha(api_key)
    balance = solver.balance()
    print("remaining Balance: ", balance)
    try:
        result = solver.recaptcha(
            sitekey=sitekey, url="https://nacionalidade.justica.gov.pt/"
        )

    except Exception as e:
        print("Failed to solve captcha")
        sys.exit(e)

    print(result)
    return result["code"]


def start_browser():
    options = Options()
    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )  # Disables the webdriver flag
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
        "translate_whitelists": {"fr": "en"},
    }
    options.add_experimental_option("prefs", prefs)

    # options.add_argument(r"--load-extension=" + os.getcwd() + r"\extensions\3.3.4_0_1")
    # options.add_argument(r"--load-extension=C:\Users\kk\Downloads\scrapit_2021\3.3.4_0")
    # input("load ext ")
    # use the derived Chrome class that handles prefs
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    time.sleep(1)
    driver.get("https://nacionalidade.justica.gov.pt/")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    driver.get(
        "chrome-extension://ifibfemgeogfhoebkmokieepdoobkbpo/options/options.html"
    )
    time.sleep(1)
    driver.find_element("name", "apiKey").send_keys("ad836997350d2f9ea35e60f0eb512567")
    time.sleep(1)
    driver.find_element("xpath", "//button[text()='Login']").click()
    time.sleep(2)
    driver.switch_to.alert.accept()
    # self.driver.find_element("tag name","body").send_keys(Keys.ENTER)
    time.sleep(1)
    for e in driver.find_elements(
        "xpath", "//div[@class='switch']//input[contains(@name,'auto')]"
    )[:4]:
        action = ActionChains(driver)
        action.move_to_element(e).click().perform()
        time.sleep(0.7)

    # driver.maximize_window()
    return driver

class unknownStepException(Exception):
    pass

def contains_date(text):
    # Regular expression pattern for date in MM/DD/YYYY format
    date_pattern = r'\b(?:0[1-9]|[12][0-9]|3[01])/(?:0[1-9]|1[0-2])/(?:\d{4})\b'
    
    # Search for the pattern in the string
    match = re.search(date_pattern, text)

    # Return True if a match is found, False otherwise
    return bool(match)

def Government(code, driver, output_folder, exception_counter):
    try:
        driver.get("https://nacionalidade.justica.gov.pt/")
        time.sleep(3)
        code_input = driver.find_element(
            By.XPATH, '//input[@placeholder="xxxx-xxxx-xxxx"]'
        )
        code_input.send_keys(code)

        wait = WebDriverWait(driver, 40)

        time.sleep(2)
        steps = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//section[@class='step-indicator']/div[contains(@class,'step')]",
                )
            )
        )

        time.sleep(2)
        notes = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "(//div[@class='container'])[3]")
            )
        )

        OfficeStation = driver.find_element(
            By.CSS_SELECTOR, "body > div:first-child > div:nth-child(2)"
        )
        station_text = OfficeStation.text
        index_na = station_text.find('na')
        if index_na != -1:
            station = station_text[index_na + 3:]
        else:
            station = station_text
        
        name = driver.find_element(
            By.CSS_SELECTOR, "body > div:first-child > div:nth-child(3)"
        )
        
        number = driver.find_element(
            By.CSS_SELECTOR, "body > div:first-child > div:nth-child(1) > div:nth-child(1)"
        )

        note = notes[0].text.casefold()

        last_active3 = None
        last_active2 = None
        last_active1 = None
        step_text = ""
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
            elif "active2" in step.get_attribute("class"):
                last_active2 = step
                step_text = step.text[2:]
                break

        if last_active1 == None and last_active2 == None and last_active3 == None:
            raise unknownStepException("An error occurred", {"code": "unknown step"})

        if last_active3 is not None:
            curr_user_step = last_active3
        elif last_active1 is not None:
            curr_user_step = last_active1
        elif last_active2 is not None:
            curr_user_step = last_active2

        class_names = curr_user_step.get_attribute("class").split()
        if class_names[2] == "active3":
            step = class_names[1][4:]
            step += "B"
        elif class_names[2] == "active1":
            step = class_names[1][4:]
            step += "A"
        elif class_names[2] == "active2":
            step = class_names[1][4:]
            step += "N"

        if step != "7A" and step != "7B":
            if(contains_date(note)):
                print("date is in the text!")
                msg = MIMEMultipart()
                msg["From"] = "pythongovernmentscript@gmail.com"
                toaddr = ["danat@passportogo.co.il", "kfirn@passportogo.co.il", "vladimirt@passportogo.co.il"]
                msg["To"] = ', '.join(toaddr)
                msg["Subject"] = "סקריפט ממשלה - התראת ביטול"

                body = "היי זה הסקריפט ממשלה, שימו לב התיק קיבל התראת ביטול: " + code + ", " + name.text
                msg.attach(MIMEText(body, "plain"))
                server.sendmail(
                    "pythongovernmentscript@gmail.com",
                    ["danat@passportogo.co.il", "kfirn@passportogo.co.il", "vladimirt@passportogo.co.il"],
                    msg.as_string(),
                )

        info = {
            "code": code,
            "step": step,
            "step_title": step_text,
            "text": note,
            "station": station,
            "number": number.text[-12:],
            "name": name.text
        }
        exception_counter = 0
    except unknownStepException as e:
        info = {
            "code": code,
            "step": "unknown step detected",
            "step_title": "",
            "text": "Error",
            "station": "",
            "number": "",
            "name": ""
        }
    except Exception as e:

        try:
            invalidCode = driver.find_element(
            By.CSS_SELECTOR, "body > div:first-child > div:first-child"
            )
            if invalidCode.get_attribute("id") == "txtErro":
                msg = MIMEMultipart()

                msg["From"] = "pythongovernmentscript@gmail.com"
                toaddr = ["danat@passportogo.co.il", "kfirn@passportogo.co.il", "vladimirt@passportogo.co.il"]

                msg["To"] = ', '.join(toaddr)
                msg["Subject"] = "invalid status code☹️"

                body = "היי זה הסקריפט ממשלה, שימו לב התיק בוטל בממשלה: " + code
                msg.attach(MIMEText(body, "plain"))
                server.sendmail(
                    "pythongovernmentscript@gmail.com",
                    ["danat@passportogo.co.il", "kfirn@passportogo.co.il", "vladimirt@passportogo.co.il"],
                    msg.as_string(),
                )
        
        except Exception as e:
            print("could not solve captcha")

        
        exception_counter += 1
        info = {
            "code": code,
            "step": "None",
            "step_title": "None",
            "text": "Error",
            "station": "None",
            "number": "",
            "name": ""
        }

    print("--------------------------------------------------------------------")
    print("script finished, output: ", info)
    print("--------------------------------------------------------------------")

    return info

input_file_path = input("Enter input file path : ")

output_folder = input("Enter output folder path : ")
driver = start_browser()


def keep_numbers_and_dash(s):
    result = ""
    for char in s:
        if char.isdigit() or char == "-":
            result += char
    return result


with open(input_file_path, "r", encoding="utf-8-sig", errors="ignore") as input_file:

    exception_counter = 0
    for code in input_file.readlines():
        code = code.strip("\n")
        # if the time is 21:00 pause the script for 10 hours, start again in 07:00
        local_time = datetime.now(pytz.timezone('Asia/Jerusalem'))
        current_day = local_time.strftime('%A')
        print("current_day:", current_day)
        local_hour = local_time.hour
        print("Local Hour:", local_hour)
        inactive_hours = [22, 23, 0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16]
        inactive_days = ["Friday", "Saturday"]
        
        if current_day in inactive_days:
            time.sleep(86400)
            
        if local_hour in inactive_hours:
            time.sleep(3600)

        if code == 0 or code == "0":
            continue

        code = keep_numbers_and_dash(code)
        # first attempt
        result = Government(code, driver, output_folder, exception_counter)

        if result["step"] != "None":
            with open(
                output_folder + r"/output.csv", "a", encoding="utf-8", newline=""
            ) as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        result["code"],
                        result["step"],
                        result["step_title"],
                        result["text"],
                        result["station"],
                        result["number"],
                        result["name"],      
                    ]
                )
            api(result)
        else:
            # second attempt
            second_result = Government(code, driver, output_folder, exception_counter)
            if result["step"] != "None":
                with open(
                    output_folder + r"/output.csv", "a", encoding="utf-8", newline=""
                ) as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [
                            result["code"],
                            result["step"],
                            result["step_title"],
                            result["text"],
                            result["station"],
                            result["number"],
                            result["name"],
                        ]
                    )
                api(result)

            else:
                # an error has accrued, send email and write new line with error.
                if exception_counter == 20:
                    msg = MIMEMultipart()

                    msg["From"] = "pythongovernmentscript@gmail.com"
                    toaddr = ["danat@passportogo.co.il", "kfirn@passportogo.co.il"]
                    msg["To"] = ', '.join(toaddr)
                    msg["Subject"] = "something is wrong with the Portuguese government website☹️"

                    body = "20 קודי ממשלה לא נסרקו ברצף. כנראה שאתר הממשלה נפל ☹️"
                    msg.attach(MIMEText(body, "plain"))
                    server.sendmail(
                        "pythongovernmentscript@gmail.com",
                        ["danat@passportogo.co.il", "kfirn@passportogo.co.il"],
                        msg.as_string(),
                    )
                    sys.exit("stopping script...")
                    
                try:
                    with open(
                        output_folder + r"/output.csv",
                        "a",
                        encoding="utf-8",
                        newline="",
                    ) as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            [
                                result["code"],
                                result["step"],
                                result["step_title"],
                                result["text"],
                                result["station"],
                                result["number"],
                                result["name"],
                            ]
                        )


                except Exception as e:
                    print("error with fetching data for status code: " + code)
                    print("error with sending email")
                continue
