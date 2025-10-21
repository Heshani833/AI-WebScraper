import streamlit as st
from scrape import scrape_website, splite_dom_content, extract_body_content, clean_body_content

st.title("AI Web Scraper")
url = st.text_input("Enter the URL of the website to scrape:")

# Ensure a session state key exists so we always have a defined value to display
if 'dom_content' not in st.session_state:
    st.session_state['dom_content'] = ""

if st.button("Scrape Website"):
    st.write(f"Scraping {url}...")

    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

# Use the session-stored value (empty string if nothing scraped yet)
cleaned_content = st.session_state.get('dom_content', "")

with st.expander("View DOM Content"):
    st.text_area("DOM Content", cleaned_content, height=400)
    

