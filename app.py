from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")  # store in .env or set in environment

@app.route("/image", methods=["POST"])
def get_image():
    data = request.json
    query = data.get("prompt")
    
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
    app.run(debug=True)
