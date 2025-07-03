from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

app = Flask(__name__)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

def recommend_songs(fav_songs, mood):
    recommendations = []

    for song in fav_songs:
        result = sp.search(q=song, type='track', limit=1)
        if result['tracks']['items']:
            track = result['tracks']['items'][0]
            name = track['name']
            artist = track['artists'][0]['name']
            url = track['external_urls']['spotify']
            recommendations.append(f"{name} by {artist} → <a href='{url}' target='_blank'>Listen</a>")
        else:
            recommendations.append(f"No match found for '{song}'")
    
    return recommendations

@app.route("/" , methods=["GET", "POST"])
def home():
        recommendations = []
        if request.method == "POST":
            songs_input = request.form.get("songs")
            mood = request.form.get("mood")
            fav_songs = [song.strip() for song in songs_input.split(",")]
            recommendations = recommend_songs(fav_songs, mood)
        return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
