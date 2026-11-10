# ********************************************************************
## app.py       Author: Llewellyn (Cassie) VanDelinder
## Module 4: Assignment 1
# Build a RESTful application that talks to an external API with Async Fetch
# ********************************************************************

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


# ------------------------------------------------------------------
# 1️⃣  GET endpoint that fetches data from a remote API
@app.route("/items", methods=["GET"])
def get_items():
    """

            Calls an external REST API (e.g., https://data.cms.gov/data-api/v1/dataset/7171ef6c-a2cf-43d4-b8ab-774b0de9b90a/data)
    Check https://data.cms.gov/api-docs for an updated url link if this one fails.
        and returns the JSON array to the client. The function demonstrates:
          • Making a GET request with `requests`.
          • Parsing JSON.
          • Basic error handling.
    """
    url = "https://data.cms.gov/data-api/v1/dataset/2457ea29-fc82-48b0-86ec-3b0755de7515/data"
    try:
        resp = requests.get(url, timeout=5)  # 5‑second timeout
        resp.raise_for_status()  # raise for HTTP errors
        data = resp.json()  # parse JSON into Python list/dict

        # Example: filter only posts with PROVIDER_TYPE_DESC == "PRACTITIONER - INTERNAL MEDICINE"
        filtered = [
            item
            for item in data
            if item["PROVIDER_TYPE_DESC"] == "PRACTITIONER - INTERNAL MEDICINE"
        ]

        return jsonify(filtered), 200  # Flask will set Content‑Type: application/json
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error: {http_err}"}), resp.status_code
    except requests.exceptions.RequestException as err:
        return jsonify({"error": f"Network error: {err}"}), 503


# ------------------------------------------------------------------
# 2️⃣  POST endpoint that forwards data to a remote API
@app.route("/items", methods=["POST"])
def create_item():
    """
    Accepts JSON from the client, forwards it to an external API,
    and returns the response. Demonstrates:
      • Reading JSON body (`request.get_json()`).
      • Sending JSON payload with `json=` argument.
      • Handling non‑200 responses.
    """
    payload = request.get_json() or {}
    url = "https://data.cms.gov/data-api/v1/dataset/7171ef6c-a2cf-43d4-b8ab-774b0de9b90a/data"

    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        return jsonify(resp.json()), 201
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error: {http_err}"}), resp.status_code
    except requests.exceptions.RequestException as err:
        return jsonify({"error": f"Network error: {err}"}), 503


# ------------------------------------------------------------------
if __name__ == "__main__":
    # Run the Flask development server on http://localhost:5000
    app.run(debug=True, port=5000)
