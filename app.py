from flask import Flask, render_template, request
from spotify_client import recommend_songs, search_track
from chatbot import get_chatbot_response, parse_fetch_spotify_tracks

app = Flask(__name__)

@app.route("/" , methods=["GET", "POST"])
def home():
        recommendations = []
        if request.method == "POST":
            songs_input = request.form.get("songs")
            mood = request.form.get("mood")
            fav_songs = [song.strip() for song in songs_input.split(",") if song.strip()]
            recommendations = recommend_songs(fav_songs, mood)
        return render_template("index.html", recommendations=recommendations, chatbot=False)

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot_recommend():
    chatbot_recommendations = []
    prompt = ""
    if request.method == "POST":
        prompt = request.form.get("chatbot_input")
        if prompt:
            llm_output = get_chatbot_response(prompt)
            chatbot_recommendations = parse_fetch_spotify_tracks(llm_output)
    return render_template("index.html", recommendations=chatbot_recommendations, chatbot=True, prompt=prompt)

if __name__ == "__main__":
    app.run(debug=True)
