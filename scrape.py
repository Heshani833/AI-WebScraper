import shutil
import time
import os
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape_website(website: str,
                   chrome_driver_path: str | None = None,
                   wait_for_css: str | None = None,
                   timeout: int = 15,
                   headless: bool = True) -> str:
    """
    Return the HTML of `website`. If wait_for_css is provided, wait up to `timeout`
    seconds for that CSS selector to be present before returning page_source.
    """
    if not website:
        raise ValueError("website must be a non-empty URL")

    options = webdriver.ChromeOptions()
    if headless:
        # modern chrome uses '--headless=new'; older chrome might use '--headless'
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')

    # Use webdriver-manager to automatically download and manage ChromeDriver
    # or use the provided chrome_driver_path if specified
    if chrome_driver_path:
        driver_path = chrome_driver_path
        # On Windows ensure the driver path points to a valid executable
        if driver_path and not driver_path.lower().endswith('.exe'):
            alt = f"{driver_path}.exe"
            if os.path.exists(alt):
                driver_path = alt
        
        if not os.path.exists(driver_path):
            raise RuntimeError(f"chromedriver not found at: {driver_path}")
        
        driver = webdriver.Chrome(service=Service(driver_path), options=options)
    else:
        # Use webdriver-manager to automatically download and install the correct ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(website)
        if wait_for_css:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_css)))
        else:
            # small pause to let JS run (prefer a specific wait_for_css)
            time.sleep(2)
        return driver.page_source
    finally:
        driver.quit()


if __name__ == "__main__":
    # Demo code: keep credentials out of source control; prefer env vars
    import os, urllib.request

    proxy = os.getenv("SCRAPER_PROXY")  # e.g. http://user:pass@host:port
    handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy}) if proxy else None
    opener = urllib.request.build_opener(handler) if handler else urllib.request.build_opener()
    resp = opener.open('https://geo.brdtest.com/mygeo.json')
    print(resp.read().decode('utf-8'))


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator='\n ')
    cleaned_content = '\n '.join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return[
        dom_content[i: i+max_length] for i in range(0, len(dom_content), max_length)
    ]


# Compatibility alias: earlier code (main.py) imports `splite_dom_content` (typo).
# Provide the alias so importing the old name works.
def splite_dom_content(dom_content, max_length=6000):
    return split_dom_content(dom_content, max_length)


# Explicitly set __all__ to help from x import * and clarify public API
__all__ = [
    'scrape_website',
    'extract_body_content',
    'clean_body_content',
    'split_dom_content',
    'splite_dom_content',
]

