import pandas as pd
from sqlalchemy import create_engine

def save_to_database(data):
    df = pd.DataFrame(data)
    engine = create_engine("sqlite:///reviews.db")  # SQLite database
    df.to_sql("reviews", con=engine, if_exists="replace", index=False)

def load_reviews():
    engine = create_engine("sqlite:///reviews.db")
    return pd.read_sql("SELECT * FROM reviews", con=engine)