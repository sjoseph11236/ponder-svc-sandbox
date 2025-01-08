from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Ponder App"

@app.route("/test")
def test():
    with open("seed.json") as seed_data:
        data = json.load(seed_data)
    return jsonify(data)
    

@app.route("/playlists")
def get_playlists():
    results = []    
    next_page_token = None

    try:
        youtube_api_key = os.environ.get("YOUTUBE_API_KEY")
        channel_id = os.environ.get("CHANNEL_ID")
        
        req = requests.get(f"https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&key={youtube_api_key}&channelId={channel_id}")

        data = req.json()

        next_page_token = data["nextPageToken"]
        items = data["items"]
        total_results = data["pageInfo"]["totalResults"]
        results.extend(items)
    except Exception as e :
        print(f"An issue has occurred! {e}")
    
    while True:
        try:
            if next_page_token:
                req = requests.get(f"https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&key={youtube_api_key}&channelId=UCCj88q3bb5OnVznn7hUY_9Q&maxResults=50&pageToken={next_page_token}")
                data = req.json()
                items = data["items"]
                results.extend(items)
                next_page_token = data["nextPageToken"]
        except KeyError: 
            print(f"Fetched all {len(results)} playlists out of {total_results}")
            break
        except Exception as e :
            print(f"An issue has occurred while fetching playlist! {e}")
    return results

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)