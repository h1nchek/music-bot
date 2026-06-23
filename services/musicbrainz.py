import requests

def search_musicbrainz(query):

    url = "https://musicbrainz.org/ws/2/recording"

    params = {
        "query": query,
        "fmt": "json",
        "limit": 5
    }

    headers = {
        "User-Agent": "MusicBot/1.0"
    }

    r = requests.get(url, params=params, headers=headers, timeout=10)
    data = r.json()

    results = []

    for item in data.get("recordings", []):

        artist = "Unknown"
        if item.get("artist-credit"):
            artist = item["artist-credit"][0]["name"]

        results.append({
            "title": item.get("title"),
            "artist": artist
        })

    return results