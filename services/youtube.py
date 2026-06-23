from ytmusicapi import YTMusic

yt = YTMusic()

def search_youtube(query):
    results = yt.search(query, limit=5)

    tracks = []

    for r in results:
        if r.get("resultType") == "song":

            tracks.append({
                "title": r["title"],
                "artist": r["artists"][0]["name"] if r.get("artists") else "Unknown",
                "url": f"https://music.youtube.com/watch?v={r['videoId']}"
            })

    return tracks