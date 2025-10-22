from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")


def scrape_website(website):
    """
    Scrape a website using remote browser if configured, otherwise use local Chrome.
    """
    if SBR_WEBDRIVER:
        print("Connecting to Remote Scraping Browser...")
        try:
            sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
            with Remote(sbr_connection, options=ChromeOptions()) as driver:
                driver.get(website)
                print("Waiting for captcha to solve...")
                solve_res = driver.execute(
                    "executeCdpCommand",
                    {
                        "cmd": "Captcha.waitForSolve",
                        "params": {"detectTimeout": 10000},
                    },
                )
                print("Captcha solve status:", solve_res["value"]["status"])
                print("Navigated! Scraping page content...")
                html = driver.page_source
                return html
        except Exception as e:
            print(f"Remote browser failed: {e}. Falling back to local Chrome...")
    
    print("Using local Chrome browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.page_load_strategy = 'eager'
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        driver.get(website)
        time.sleep(3)
        html = driver.page_source
        
        if not html or len(html) < 100:
            raise Exception("Retrieved HTML is too short or empty")
        
        return html
        
    except Exception as e:
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            raise Exception(f"Page took too long to load (>30s). Try a simpler website or increase timeout.")
        elif "net::" in error_msg.lower():
            raise Exception(f"Network error: Cannot reach {website}. Check your internet connection.")
        else:
            raise Exception(f"Failed to scrape website: {error_msg}")
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


splite_dom_content = split_dom_content
