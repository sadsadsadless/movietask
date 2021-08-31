import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.kinopoisk.ru/lists/top500/'
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/92.0.4515.159 Safari/537.36",
           "accept": "*/*",
           }
FILE = 'gj.csv'
PARAMS = {"page": 1, "tab": "all"}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='desktop-rating-selection-film-item')

    movies = []
    for item in items:
        additional = item.find_all(
            "span", {"class": "selection-film-item-meta__meta-additional-item"}
        )
        movies.append({
            'title': item.find('p', class_='selection-film-item-meta__name').get_text(),
            'genre': additional[1].get_text(strip=True),
        })
    return movies

    print(movies)


def save_genres(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["title", "genre"])
        for item in items:
            writer.writerow([item["title"], item["genre"]])


def save_genres(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["title", "genre"])
        for item in items:
            writer.writerow([item["title"], item["genre"]])


def parser():
    genres = []
    for page in range(1, 10):
        print("Parsing page {}...".format(page))
        PARAMS["page"] = page
        html = get_html(URL, PARAMS)
        if html.status_code == 200:
            genres.extend(get_content(html.text))
        else:
            print("Non_available")
    save_genres(genres, FILE)


parser()
