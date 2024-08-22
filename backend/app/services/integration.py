# services/integration.py

import json
import os
from hashlib import sha256

class DataIntegration:

    def __init__(self, processed_dir="data/processed", integrated_dir="data/integrated"):
        self.processed_dir = processed_dir
        self.integrated_dir = integrated_dir

        if not os.path.exists(self.integrated_dir):
            os.makedirs(self.integrated_dir)

    def generate_id(self, data):
        unique_string = f"{data['title']}_{data['date']}_{data['author']}"
        return sha256(unique_string.encode()).hexdigest()

    def integrate_data(self):
        all_articles = {}
        for file_name in os.listdir(self.processed_dir):
            processed_file = os.path.join(self.processed_dir, file_name)
            with open(processed_file, "r", encoding='utf-8') as file:
                articles = json.load(file)
                for article in articles:
                    article_id = self.generate_id(article)
                    if article_id not in all_articles:
                        all_articles[article_id] = article

        integrated_file = os.path.join(self.integrated_dir, "integrated_articles.json")
        with open(integrated_file, "w", encoding='utf-8') as file:
            json.dump(all_articles, file, indent=4)
        print("Data integrated and deduplicated")

# Example usage
integration = DataIntegration()
integration.integrate_data()
