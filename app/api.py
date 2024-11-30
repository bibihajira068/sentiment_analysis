from flask import Flask, request, jsonify
from database import load_reviews
from sentiment import analyze_sentiment
import pandas as pd
from sqlalchemy import create_engine



app = Flask(__name__)

# Sentiment Analysis API
@app.route('/sentiment', methods=['POST'])
def sentiment_analysis():
    data = request.json
    review_text = data.get("review", "")
    sentiment = analyze_sentiment([{"text": review_text}])
    return jsonify(sentiment[0])

# Review Retrieval API
@app.route('/reviews', methods=['GET'])
def get_reviews():
    color = request.args.get("color")
    size = request.args.get("size")
    engine = create_engine("sqlite:///reviews.db")
    query = f"SELECT * FROM reviews WHERE color='{color}' AND style='{size}'"
    result = pd.read_sql(query, con=engine)
    return result.to_json(orient="records")

if __name__ == "_main_":
    app.run(debug=True)