from textblob import TextBlob

def analyze_sentiment(reviews):
    for review in reviews:
        if review["text"]:
            sentiment = TextBlob(review["text"]).sentiment.polarity
            review["sentiment"] = "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"
    return reviews