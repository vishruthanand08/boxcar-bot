import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

SEND_SMS = True                          # ✅ Toggle this to False during testing
HEADLESS = False                          # ✅ Set to False to open Chrome for debugging
WAIT_SECONDS = 5                          # Time to wait for JavaScript to load

def send_sms(body):
    if not SEND_SMS:
        print("📩 SMS not sent (SEND_SMS = False):", body)
        return
    client = Client(TWILIO_SID, TWILIO_AUTH)
    message = client.messages.create(
        body=body,
        from_=TWILIO_FROM,
        to=TWILIO_TO
    )
    print("✅ SMS Sent:", message.sid)

def check_units():
    url = "https://boxcar.tarragon.com/floorplans"

    # Setup Chrome
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(WAIT_SECONDS)

    containers = driver.find_elements(By.CSS_SELECTOR, "div[id^='fp-container-']")

    print(f"📦 Scanning {len(containers)} floorplans...")

    for container in containers:
        try:
            # Skip MFTE units
            mfte = container.find_elements(By.CLASS_NAME, "mfte-inserted-overtext")
            if mfte:
                continue

            # Look for buttons with the text "AVAILABILITY"
            buttons = container.find_elements(By.TAG_NAME, "button")
            availability_buttons = [
                btn for btn in buttons if btn.text.strip().upper() == "AVAILABILITY"
            ]

            if availability_buttons:
                unit_info = container.text.strip().split("\n")[0]
                send_sms(f"🎉 Non-MFTE unit AVAILABLE: {unit_info}")
                print(f"✅ Non-MFTE AVAILABLE: {unit_info}")
                break  # Stop after finding one match

        except Exception as e:
            print("⚠️ Error checking a container:", e)

    driver.quit()
if __name__ == "__main__":
    while True:
        print("🔍 Running non-MFTE Boxcar checker...")
        check_units()
        print("🕒 Sleeping for 30 minutes...\n")
        time.sleep(1800) 
