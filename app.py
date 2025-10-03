from flask import Flask, request, render_template, url_for
import requests

app = Flask(__name__)

# Replace with your Colab ngrok URL
COLAB_API_URL = "https://thievish-unodoriferously-maren.ngrok-free.dev/predict"

# Map numeric class IDs to human-readable labels
CLASS_MAP = {0: "no fire", 1: "fire", 2: "smoke"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    # Send image to Colab API
    files = {"file": (file.filename, file.stream, file.mimetype)}
    try:
        response = requests.post(COLAB_API_URL, files=files)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error from API: {e}", 500

    data = response.json()
    img_base64 = data.get("image_base64")
    predictions = data.get("predictions", [])

    # Map numeric class IDs to human-readable labels
    for p in predictions:
        class_id = p.get("class")
        if class_id is not None:
            p["class"] = CLASS_MAP.get(class_id, str(class_id))

    # Check if fire or smoke is detected
    fire_detected = any(p.get("class") in ["fire", "smoke"] for p in predictions)

    # Optional: simple status message
    status_message = "Fire Detected!" if fire_detected else "No Fire Detected."

    return render_template(
        "index.html",
        img_base64=img_base64,
        predictions=predictions,
        fire_detected=fire_detected,
        status_message=status_message
    )

if __name__ == "__main__":
    app.run(debug=True)
