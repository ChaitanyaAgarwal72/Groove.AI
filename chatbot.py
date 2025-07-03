import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_song_recommendations(user_text):
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

            