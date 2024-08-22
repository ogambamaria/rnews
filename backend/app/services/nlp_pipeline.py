# services/nlp_pipeline.py

import json
import os
import spacy
from textblob import TextBlob

class NLPipeline:

    def __init__(self, cleaned_dir="data/cleaned", enriched_dir="data/enriched"):
        self.cleaned_dir = cleaned_dir
        self.enriched_dir = enriched_dir

        if not os.path.exists(self.enriched_dir):
            os.makedirs(self.enriched_dir)

        self.nlp = spacy.load("en_core_web_sm")

    def summarize(self, content):
        # Simplified summarization using Spacy sentences (custom implementation needed for more advanced summarization)
        doc = self.nlp(content)
        return " ".join([sent.text for sent in doc.sents][:2])  # Taking first 2 sentences as a summary

    def classify(self, content):
        # Dummy classification (implement a more sophisticated model as needed)
        if "politics" in content.lower():
            return "Politics"
        elif "sports" in content.lower():
            return "Sports"
        else:
            return "General"

    def sentiment_analysis(self, content):
        blob = TextBlob(content)
        return blob.sentiment.polarity

    def process_articles(self):
        cleaned_file = os.path.join(self.cleaned_dir, "cleaned_articles.json")
        with open(cleaned_file, "r", encoding='utf-8') as file:
            articles = json.load(file)

        enriched_articles = {}
        for article_id, article in articles.items():
            article["summary"] = self.summarize(article["content"])
            article["category"] = self.classify(article["content"])
            article["sentiment"] = self.sentiment_analysis(article["content"])
            enriched_articles[article_id] = article

        enriched_file = os.path.join(self.enriched_dir, "enriched_articles.json")
        with open(enriched_file, "w", encoding='utf-8') as file:
            json.dump(enriched_articles, file, indent=4)
        print("NLP processing completed")

# Example usage
nlp_pipeline = NLPipeline()
nlp_pipeline.process_articles()
