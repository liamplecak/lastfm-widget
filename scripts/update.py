import json
import os
import urllib.request
from datetime import datetime, timezone

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

images = {}

for img in track["image"]:
    images[img["size"]] = img["#text"]

image = images.get("extralarge") or images.get("large") or ""

music = {
    "track": track["name"],
    "artist": track["artist"]["#text"],
    "album": track["album"]["#text"],

    "cover": image,
    "images": images,

    "playing": "@attr" in track and track["@attr"].get("nowplaying") == "true",

    "timestamp": track.get("date", {}).get("#text", ""),
    "uts": track.get("date", {}).get("uts", ""),

    "url": track["url"],

    "artist_url": track["artist"].get("url", ""),

    "album_url": track["album"].get("url", ""),

    "loved": track.get("loved", "0") == "1",

    "generated": datetime.now(timezone.utc).isoformat(),
}

with open("music.json", "w", encoding="utf-8") as f:
    json.dump(music, f, indent=2)
