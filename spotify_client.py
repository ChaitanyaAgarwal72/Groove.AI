import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

def search_track(song_name, artist_name):
    query = f"{song_name} {artist_name}"
    result = sp.search(q=query, type='track', limit=1)
    try:
        if result['tracks']['items']:
            track = result['tracks']['items'][0]
            return {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'url': track['external_urls']['spotify']
            }
    except Exception as e:
        print(f"Spotify search failed for {song_name} by {artist_name}: {e}")
    return None

def recommend_songs(fav_songs, mood=None):
    recommendations = []
    for song in fav_songs:
        try:
            result = sp.search(q=song, type='track', limit=1)
            if result['tracks']['items']:
                track = result['tracks']['items'][0]
                name = track['name']
                artist = track['artists'][0]['name']
                url = track['external_urls']['spotify']
                recommendations.append(f"{name} by {artist} → <a href='{url}' target='_blank'>Listen</a>")
            else:
                recommendations.append(f"No match found for '{song}'")
        except Exception as e:
            print(f"[ERROR] Failed for '{song}': {e}")
            recommendations.append(f"Error fetching '{song}'")
    return recommendations