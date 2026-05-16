from playwright.sync_api import sync_playwright
import time
import os

os.makedirs('assets', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1200})
    
    print("Navigating to http://127.0.0.1:5000 ...")
    page.goto('http://127.0.0.1:5000')
    
    # Wait for page to load
    page.wait_for_selector('.landing-title')
    time.sleep(2)
    
    # Take screenshot of the landing page
    print("Capturing Landing Page...")
    page.screenshot(path='assets/landing.png', full_page=True)
    
    # Execute analysis for AAPL
    print("Executing Analysis for AAPL...")
    page.fill('#company', 'Apple Inc.')
    page.fill('#ticker', 'AAPL')
    page.click('#analyzeBtn')
    
    # Wait for dashboard to become visible
    page.wait_for_selector('.company-title', state='visible', timeout=60000)
    
    # Wait for charts to render and animations to finish
    time.sleep(5)
    
    print("Capturing Dashboard...")
    page.screenshot(path='assets/dashboard.png', full_page=True)
    
    browser.close()
    print("Done!")
