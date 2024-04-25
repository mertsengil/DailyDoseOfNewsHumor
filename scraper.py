import requests
from bs4 import BeautifulSoup
import json

#scrape the given website and fetch the 10 most recent news
#create a json file
#save it in local


class Scraper:
    def __init__(self, base_url, output_path):
        self.base_url = base_url
        self.output_path = output_path

    def find_rss_feed(self):
        response = requests.get(self.base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('link', type='application/rss+xml')
        return [link.get('href') for link in links if link.get('href')]

    def extract_links_from_rss(self, rss_url):
        response = requests.get(rss_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features='xml')
        items = soup.find_all('item')
        return [item.find('link').text for item in items]

    def clean_text(self, text):
        remove_patterns = [
            "Tam Boyutta Gör",
            "Bu haberi,mobil uygulamamızıkullanarak indirip,istediğiniz zaman (çevrim dışı bile) okuyabilirsiniz:"
        ]
        for pattern in remove_patterns:
            text = text.replace(pattern, " ")
        return text

    def fetch_content(self, url):
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        section = soup.find('section', class_='kolon yazi')
        title = soup.find('div', class_='baslik-content').find('h1', class_='post-baslik').get_text(strip=True) if soup.find('div', class_='baslik-content') else "No title found"
        content = self.clean_text(section.get_text(strip=True)) if section else "No content found"
        return {"title": title, "content": content, "url": str(url)}

    def scrape(self):
        rss_urls = self.find_rss_feed()
        all_links = []
        for rss_url in rss_urls:
            links = self.extract_links_from_rss(rss_url)
            all_links.extend(links)
        articles = []
        for link in all_links:
            article = self.fetch_content(link)
            articles.append(article)
        with open(self.output_path, 'w', encoding='utf-8') as file:
            json.dump(articles, file, indent=2, ensure_ascii=False)

# EXAMPLE USAGE:
# scraper = Scraper("https://www.donanimhaber.com/", "/path/to/your/articles.json")
# scraper.scrape()
