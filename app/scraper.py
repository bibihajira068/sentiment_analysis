import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from sqlalchemy import create_engine
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def setup_driver():
    """Set up Chrome WebDriver with options to prevent detection"""
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_product_details(driver):
    """
    Extract product-specific details like color, storage, model
    """
    try:
        # Try to find product details from various possible locations
        details_section = driver.find_elements(By.CSS_SELECTOR, "#productDetails_techSpec_section_1")
        
        if details_section:
            # Look for color and storage information
            details_text = details_section[0].text
            return {
                'color': extract_color(details_text),
                'storage': extract_storage(details_text)
            }
        
        # Fallback to checking other possible locations
        about_section = driver.find_elements(By.CSS_SELECTOR, "#feature-bullets")
        if about_section:
            details_text = about_section[0].text
            return {
                'color': extract_color(details_text),
                'storage': extract_storage(details_text)
            }
    except Exception as e:
        print(f"Error extracting product details: {e}")
    
    # Default if no details found
    return {
        'color': 'Unknown',
        'storage': 'Unknown'
    }

def extract_color(text):
    """
    Extract color from text
    """
    color_keywords = ['black', 'white', 'blue', 'red', 'green', 'purple', 'silver', 'gold']
    text_lower = text.lower()
    
    for color in color_keywords:
        if color in text_lower:
            return color
    
    return 'Unknown'

def extract_storage(text):
    """
    Extract storage size from text
    """
    storage_options = ['128GB', '256GB', '512GB', '64GB', '1TB']
    text_lower = text.lower()
    
    for storage in storage_options:
        if storage.lower() in text_lower:
            return storage
    
    return 'Unknown'

def scrape_amazon_reviews(url, max_pages=3):
    driver = setup_driver()
    all_reviews = []

    try:
        driver.get(url)
        
        # Extract product details before scraping reviews
        product_details = extract_product_details(driver)
        
        for page in range(max_pages):
            # Wait for reviews to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-hook='review']"))
            )
            
            # Find all reviews on the page
            reviews = driver.find_elements(By.CSS_SELECTOR, "div[data-hook='review']")
            
            for review in reviews:
                try:
                    title = review.find_element(By.CSS_SELECTOR, "a[data-hook='review-title']").text
                    text = review.find_element(By.CSS_SELECTOR, "span[data-hook='review-body']").text
                    rating = review.find_element(By.CSS_SELECTOR, "i[data-hook='review-star-rating']").text
                    date = review.find_element(By.CSS_SELECTOR, "span[data-hook='review-date']").text
                    verified = "Verified Purchase" in review.text
                    
                    # Combine review data with product details
                    review_data = {
                        'title': title,
                        'text': text,
                        'rating': rating,
                        'date': date,
                        'verified': verified,
                        'color': product_details['color'],
                        'storage': product_details['storage']
                    }
                    
                    all_reviews.append(review_data)
                except Exception as e:
                    print(f"Error extracting review: {e}")
            
            # Try to click next page, break if no more pages
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.a-last a")
                next_button.click()
                time.sleep(2)  # Wait for page to load
            except:
                break

    except Exception as e:
        print(f"Error during scraping: {e}")
    
    finally:
        driver.quit()
    
    return all_reviews

def save_to_database(data):
    df = pd.DataFrame(data)
    engine = create_engine("sqlite:///amazon_reviews.db")
    df.to_sql("reviews", con=engine, if_exists="replace", index=False)
    print(f"Saved {len(data)} reviews to database")

def main():
    url = "https://www.amazon.in/Apple-New-iPhone-12-128GB/dp/B08L5TNJHG/"
    reviews = scrape_amazon_reviews(url)
    save_to_database(reviews)

if __name__ == "__main__":
    main()