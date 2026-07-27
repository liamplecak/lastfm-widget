import json
import os
import urllib.request

API_KEY = os.environ["LASTFM_API_KEY"]
USERNAME = os.environ["LASTFM_USERNAME"]

url = (
    "https://ws.audioscrobbler.com/2.0/"
    f"?method=user.getrecenttracks"
    f"&user={USERNAME}"
    f"&api_key={API_KEY}"
    "&format=json"
    "&limit=1"
)

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())

track = data["recenttracks"]["track"][0]

image = ""
if len(track["image"]) > 0:
    image = track["image"][-1]["#text"]

music = {
    "track": track["name"],
    "artist": track["artist"]["#text"],
    "album": track["album"]["#text"],
    "cover": image,
    "playing": "@attr" in track and track["@attr"].get("nowplaying") == "true",
    "timestamp": track.get("date", {}).get("#text", "")
}

with open("music.json", "w", encoding="utf-8") as f:
    json.dump(music, f, indent=2)
