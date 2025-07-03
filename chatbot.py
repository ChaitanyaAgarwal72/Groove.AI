import google.generativeai as genai
from dotenv import load_dotenv
from spotify_client import search_track

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_chatbot_response(user_text):
    prompt = f"""
        You are a music recommendation expert. Based on the user's input below, provide a list of 5 popular songs (with artist names)
        that fit the mood/emotions or the activity of the user.
        
        User Input: "{user_text}"

        Respond in this format:
        1. Song Title - Artist Name
        2. Song Title - Artist Name
        ...
        """
    
    response = model.generate_content(prompt)
    return response.text

def parse_fetch_spotify_tracks(gemini_output):
    songs = []
    for line in gemini_output.split('\n'):
        if " - " in line:
            parts = line.split(" - ", 1)
            if parts and len(parts) == 2:
                song_name = parts[0].split('. ', 1)[-1].strip() 
                artist_name = parts[1].strip()
                track_info = search_track(song_name, artist_name)
                if track_info:
                    songs.append(track_info)
    return songs