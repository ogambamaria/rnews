# services/data_acquisition.py 

import requests
from sqlalchemy.orm import Session
from app.models.article import Article
from datetime import datetime
from textblob import TextBlob

class DataAcquisition:
    def __init__(self, api_key, search_terms):
        self.api_key = api_key
        self.search_terms = search_terms
        self.url = "https://api.thenewsapi.com/v1/news/all"

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity

    def fetch_and_save_articles(self, db: Session):
        for term in self.search_terms:
            try:
                params = {
                    "api_token": self.api_key,
                    "search": term,
                    "language": "en",
                }
                response = requests.get(self.url, params=params)
                
                if response.status_code == 200:
                    articles = response.json().get('data', [])
                    for article_data in articles:
                        title = article_data.get('title', 'No Title')
                        description = article_data.get('description', '')
                        url = article_data.get('url', '')
                        summary = article_data.get('snippet', '')
                        categories = article_data.get('categories', [])
                        category = categories[0] if categories else "general"
                        sentiment = self.analyze_sentiment(description)
                        date_str = article_data.get('published_at', None)
                        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ') if date_str else datetime.now()

                        article = Article(
                            title=title,
                            description=description,
                            url=url,
                            summary=summary,
                            category=category,
                            sentiment=sentiment,
                            date=date
                        )
                        db.add(article)
                        db.commit()
                        print(f"Article saved: {title}")
                else:
                    print(f"Failed to fetch articles for term '{term}' with status code: {response.status_code}")
                    print(f"Error details: {response.text}")
            except Exception as e:
                print(f"Error fetching articles for term '{term}': {str(e)}")