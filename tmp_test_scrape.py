from scrape import scrape_website
print('ok import')
try:
    scrape_website('https://example.com', headless=True, timeout=2)
except Exception as e:
    print('ERR:', type(e).__name__, e)
