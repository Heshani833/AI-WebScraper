import os
import streamlit as st
from scrape import scrape_website
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables (optional; sample.env exists)
load_dotenv()

st.title("AI Web Scraper")

url = st.text_input("Enter the URL of the webpage to scrape:")

if st.button("Scrape"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Scraping..."):
            try:
                result = scrape_website(url)
                # Choose appropriate display depending on result type
                st.write(result)
            except Exception as e:
                st.error("An error occurred while scraping.")
                st.exception(e)

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