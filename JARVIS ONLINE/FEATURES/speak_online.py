import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging to suppress console logs
logging.getLogger('selenium').setLevel(logging.WARNING)

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment this line to run in headless mode
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Create a Service object with WebDriverManager to automatically manage the ChromeDriver binary
chrome_service = Service(ChromeDriverManager().install())

# Create a Chrome driver instance with the specified options and service
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Navigate to the website
driver.get("https://ttsmp3.com/ai")


def speak(text):
    try:
        # Wait for the text input element to be present and clickable
        text_area = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'voicetext'))
        )

        # Clear any existing text
        text_area.clear()

        # Input text into the element
        text_area.send_keys(text)
        print(f"Text input: {text}")

        # Wait for the "Read" button to be present and clickable
        read_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'vorlesenbutton'))
        )

        # Click the "Read" button using JavaScript to avoid interception
        driver.execute_script("arguments[0].click();", read_button)

        # Wait for the play button to appear after the conversion
        play_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "glyphicon-play")]'))
        )

        # Click the play button to hear the TTS output
        driver.execute_script("arguments[0].click();", play_button)

        # Sleep to allow the audio to play
        time.sleep(len(text) * 2)  # Adjust this sleep duration as needed
        driver.quit()

    except Exception as e:
        print("An error occurred:", e)

speak("hello,how are you.because i a fine i think you are also fine.thank you bye-bye.")

