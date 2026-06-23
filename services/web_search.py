import requests
from bs4 import BeautifulSoup


def search_web(query, site):

    url = f"https://duckduckgo.com/html/?q={query}+site:{site}"

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")

    results = []

    for a in soup.find_all("a", class_="result__a")[:3]:
        results.append({
            "title": a.text,
            "url": a["href"]
        })

    return results


def search_soundcloud(query):
    return search_web(query, "soundcloud.com")


def search_bandcamp(query):
    return search_web(query, "bandcamp.com")