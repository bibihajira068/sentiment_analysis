# Amazon Review Sentiment Analysis API

## Overview
This application scrapes Amazon product reviews, performs sentiment analysis, and provides an API for retrieving and analyzing reviews.

## Prerequisites
- Python 3.8+
- Google Chrome
- pip package manager

## Installation

1. Clone the repository:
bash
git clone https://github.com/bibihajira068/sentiment_analysis.git
cd amazon-reviews-sentiment-api


2. Install required packages:
bash
pip install selenium webdriver_manager flask textblob pandas sqlalchemy


## Components
- scraper.py: Web scrapes Amazon product reviews
- api.py: Flask API for sentiment analysis and review retrieval

## Usage

### 1. Scrape Reviews
bash
python app/scraper.py

- Scrapes reviews from the specified Amazon product page
- Saves reviews to SQLite database amazon_reviews.db

### 2. Start API Server
bash
python app/api.py

- Runs on http://localhost:5000

### 3. API Endpoints

#### Sentiment Analysis
- *Endpoint*: /sentiment
- *Method*: POST
- *Request Body*: {"review": "Your review text"}
- *Response*: Sentiment classification (positive/negative/neutral)

#### Review Retrieval
- *Endpoint*: /reviews
- *Method*: GET
- *Query Parameters*: 
  - color: Product color
  - storage: Storage size
  - rating: Review rating

## Example Curl Commands

1. Sentiment Analysis:
bash
curl -X POST http://localhost:5000/sentiment \
     -H "Content-Type: application/json" \
     -d '{"review": "This phone is amazing!"}'


2. Review Retrieval:
bash
curl "http://localhost:5000/reviews?color=blue&storage=128GB&rating=5"


## Notes
- Requires Google Chrome
- Respects web scraping ethics
- For educational and personal use only