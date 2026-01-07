from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load local .env if exists (for testing locally)
load_dotenv()

app = Flask(__name__)
CORS(app)  # allow all origins

# Get Pexels API key from environment
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

if not PEXELS_API_KEY:
    raise ValueError("PEXELS_API_KEY environment variable not set")

@app.route("/image", methods=["POST"])
def get_image():
    data = request.json
    query = data.get("prompt")

    if not query:
        return jsonify({"image": None, "message": "No prompt provided"}), 400

    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(
        f"https://api.pexels.com/v1/search?query={query}&per_page=1",
        headers=headers
    )

    if response.status_code == 200:
        results = response.json()
        if results["photos"]:
            image_url = results["photos"][0]["src"]["medium"]
            return jsonify({"image": image_url})
        else:
            return jsonify({"image": None, "message": "No image found"})
    else:
        return jsonify({"image": None, "message": "API request failed"})

if __name__ == "__main__":
    # Railway sets PORT automatically; default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
