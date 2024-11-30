# Python Development - Trainee Task

## Prerequisites
- Python 3.8+
- Virtual Environment

## Setup Instructions
1. Clone the repository:
    
    git clone <repository_url>
    cd assignment
    
2. Create and activate a virtual environment:
    
    python -m venv env
    source env/bin/activate  # For Linux/Mac
    env\Scripts\activate     # For Windows
    
3. Install dependencies:
    
    pip install -r requirements.txt
    

## Running the Project
1. Run the scraper to populate the database:
    
    python app/scraper.py
    
2. Start the API server:
    
    python app/api.py
    

## API Endpoints
1. *Sentiment Analysis API*
   - *URL*: /sentiment
   - *Method*: POST
   - *Input*:
     json
     {
       "review": "This is a great product!"
     }
     
   - *Output*:
     json
     {
       "sentiment": "positive"
     }
     

2. *Review Retrieval API*
   - *URL*: /reviews
   - *Method*: GET
   - *Query Parameters*: color, size
   - *Output*:
     A list of reviews in JSON format.