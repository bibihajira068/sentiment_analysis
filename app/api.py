import sqlite3
from flask import Flask, request, jsonify
from textblob import TextBlob
from sqlalchemy import create_engine, text
import pandas as pd

app = Flask(__name__)

# Database connection
def get_db_connection():
    engine = create_engine("sqlite:///amazon_reviews.db")
    return engine

def analyze_sentiment(text):
    """
    Analyze sentiment of a given text
    Returns: 'positive', 'negative', or 'neutral'
    """
    if not text:
        return "neutral"
    
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"
    else:
        return "neutral"

@app.route('/sentiment', methods=['POST'])
def sentiment_analysis():
    """
    API Endpoint for Sentiment Analysis
    Expects JSON with 'review' text
    Returns sentiment classification
    """
    data = request.json
    
    # Validate input
    if not data or 'review' not in data:
        return jsonify({
            "error": "Invalid input. 'review' text is required.",
            "status": "failure"
        }), 400
    
    review_text = data['review']
    sentiment = analyze_sentiment(review_text)
    
    return jsonify({
        "review": review_text,
        "sentiment": sentiment,
        "status": "success"
    })

@app.route('/reviews', methods=['GET'])
def retrieve_reviews():
    """
    API Endpoint for Review Retrieval
    Supports filtering by color, storage, and rating
    """
    # Get query parameters
    color = request.args.get('color')
    storage = request.args.get('storage')
    rating = request.args.get('rating')
    
    # Prepare base query
    query = "SELECT * FROM reviews WHERE 1=1"
    params = []
    
    # Add filters if provided
    if color:
        query += " AND color = ?"
        params.append(color)
    
    if storage:
        query += " AND storage = ?"
        params.append(storage)
    
    if rating:
        query += " AND rating = ?"
        params.append(rating)
    
    # Execute query
    engine = get_db_connection()
    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        reviews = [dict(row) for row in result]
    
    # Add sentiment to reviews
    for review in reviews:
        review['sentiment'] = analyze_sentiment(review.get('text', ''))
    
    return jsonify({
        "reviews": reviews,
        "count": len(reviews),
        "status": "success"
    })

# Add preprocessing for existing reviews in database
def preprocess_existing_reviews():
    """
    Add sentiment analysis to existing reviews in database
    """
    engine = get_db_connection()
    
    # Read existing reviews
    df = pd.read_sql("SELECT * FROM reviews", engine)
    
    # Add sentiment column
    df['sentiment'] = df['text'].apply(analyze_sentiment)
    
    # Update database
    df.to_sql('reviews', engine, if_exists='replace', index=False)
    print("Reviews preprocessed with sentiment analysis")

if __name__ == '__main__':
    # Preprocess existing reviews before starting the server
    preprocess_existing_reviews()
    
    # Run the Flask app
    app.run(debug=True, port=5000)