# services/cleaning.py

import json
import os
import re

class DataCleaning:

    def __init__(self, integrated_dir="data/integrated", cleaned_dir="data/cleaned"):
        self.integrated_dir = integrated_dir
        self.cleaned_dir = cleaned_dir

        if not os.path.exists(self.cleaned_dir):
            os.makedirs(self.cleaned_dir)

    def clean_text(self, text):
        # Remove unwanted characters and normalize text
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def clean_data(self):
        integrated_file = os.path.join(self.integrated_dir, "integrated_articles.json")
        with open(integrated_file, "r", encoding='utf-8') as file:
            articles = json.load(file)

        cleaned_articles = {}
        for article_id, article in articles.items():
            article["title"] = self.clean_text(article["title"])
            article["content"] = self.clean_text(article["content"])
            cleaned_articles[article_id] = article

        cleaned_file = os.path.join(self.cleaned_dir, "cleaned_articles.json")
        with open(cleaned_file, "w", encoding='utf-8') as file:
            json.dump(cleaned_articles, file, indent=4)
        print("Data cleaned")

# Example usage
cleaning = DataCleaning()
cleaning.clean_data()
