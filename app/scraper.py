import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine


def scrape_reviews():
    url = "https://www.amazon.in/Apple-New-iPhone-12-128GB/dp/B08L5TNJHG/"
    print (url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    review_data = []

    for page in range(1, 3):  # Adjust range to scrape more pages
        response = requests.get(url + f"?pageNumber={page}", headers=headers)
        print("res",response)
        soup = BeautifulSoup(response.content, "html.parser")
        print("soup",soup)

        reviews = soup.find_all("div", class_="a-section review aok-relative")
        print("reviews",reviews)
        for review in reviews:
            title = review.find("a", class_="review-title").text.strip() if review.find("a", class_="review-title") else None
            text = review.find("span", class_="review-text-content").text.strip() if review.find("span", class_="review-text-content") else None
            style = review.find("a", class_="a-size-mini a-link-normal a-color-secondary").text.strip() if review.find("a", class_="a-size-mini a-link-normal a-color-secondary") else None
            color = review.find("span", class_="a-size-mini a-color-base").text.strip() if review.find("span", class_="a-size-mini a-color-base") else None
            verified = "Verified Purchase" in review.text

            review_data.append({
                "title": title,
                "text": text,
                "style": style,
                "color": color,
                "verified": verified
            })
    return review_data

def save_to_database(data):
    df = pd.DataFrame(data)
    engine = create_engine("sqlite:///reviews.db")  # SQLite database
    df.to_sql("reviews", con=engine, if_exists="replace", index=False)

if __name__ == "__main__":
    scraped_data = scrape_reviews()
    print(scraped_data)
    save_to_database(scraped_data)

    