# services/extraction.py

from bs4 import BeautifulSoup
import os

class DataExtraction:

    def __init__(self, raw_dir="data/raw", processed_dir="data/processed"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def extract_data(self):
        for file_name in os.listdir(self.raw_dir):
            raw_file = os.path.join(self.raw_dir, file_name)
            with open(raw_file, "r", encoding='utf-8') as file:
                soup = BeautifulSoup(file, "lxml")

                # Extracting article data (you would need to adapt this to your needs)
                articles = soup.find_all("article")
                extracted_data = []

                for article in articles:
                    title = article.find("h1").get_text() if article.find("h1") else "No Title"
                    date = article.find("time").get("datetime") if article.find("time") else "No Date"
                    author = article.find("span", class_="author").get_text() if article.find("span", class_="author") else "No Author"
                    content = article.find("div", class_="content").get_text() if article.find("div", class_="content") else "No Content"

                    extracted_data.append({
                        "title": title,
                        "date": date,
                        "author": author,
                        "content": content
                    })

                processed_file = os.path.join(self.processed_dir, f"{file_name}.json")
                with open(processed_file, "w", encoding='utf-8') as file:
                    json.dump(extracted_data, file, indent=4)
                print(f"Processed and extracted data from {file_name}")

# Example usage
extraction = DataExtraction()
extraction.extract_data()
