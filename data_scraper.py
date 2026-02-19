import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


BASE_URL = "http://quotes.toscrape.com/page/{}/"


def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes_data = []

    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]

        quotes_data.append({
            "text": text,
            "author": author,
            "tags": ", ".join(tags),
            "scraped_at": datetime.now().isoformat()
        })

    return quotes_data


def save_to_csv(data, filename="quotes.csv"):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} quotes to {filename}")


def main():
    all_quotes = []
    page = 1

    while True:
        url = BASE_URL.format(page)
        html = fetch_page(url)

        if not html:
            break

        data = parse_quotes(html)

        if not data:
            break

        all_quotes.extend(data)
        print(f"Scraped page {page}")
        page += 1

    save_to_csv(all_quotes)


if __name__ == "__main__":
    main()
