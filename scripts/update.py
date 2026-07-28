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

from urllib.parse import quote

artist = quote(track["artist"]["#text"])
title = quote(track["name"])

info_url = (
    "https://ws.audioscrobbler.com/2.0/"
    f"?method=track.getInfo"
    f"&api_key={API_KEY}"
    f"&username={USERNAME}"
    f"&artist={artist}"
    f"&track={title}"
    "&format=json"
)

with urllib.request.urlopen(info_url) as response:
    info = json.loads(response.read())

track_info = info.get("track", {})

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
    "uts": track.get("date", {}).get("uts", None),

    "url": track["url"],

    "artist_url": track["artist"].get("url", ""),

    "album_url": track["album"].get("url", ""),

    "loved": track_info.get("userloved", "0") == "1",

    "playcount": int(track_info.get("userplaycount", 0)),

    "duration": int(track_info.get("duration", 0)),

    "generated": datetime.now(timezone.utc).isoformat(),
}

with open("music.json", "w", encoding="utf-8") as f:
    json.dump(music, f, indent=2)
