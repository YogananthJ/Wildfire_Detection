from flask import Flask, render_template, request, jsonify
import numpy as np
import base64
import io
from PIL import Image
import requests
from ultralytics import YOLO 

# ================================
# Load Pretrained YOLOv8 Model 
# ================================
MODEL_PATH = "wildfire_yolov8.pt"  
yolo_model = YOLO(MODEL_PATH)
print("✅ YOLOv8 model loaded successfully.")

# ================================
# Roboflow API Setup
# ================================
API_KEY = "PJuwD4ncNkCOpzYHajI5"
WORKSPACE = "test0-sbyyu"
PROJECT = "wildfire-soeq8"
VERSION = 10

# Roboflow infer URL
INFER_URL = f"https://detect.roboflow.com/{PROJECT}/{VERSION}?api_key={API_KEY}"

app = Flask(__name__)

# ================================
# Helper: Send Image to Roboflow
# ================================
def predict_with_roboflow(image: Image.Image):
    # Convert PIL image to bytes (JPEG)
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    # Send to Roboflow API
    resp = requests.post(
        INFER_URL,
        files={"file": ("image.jpg", byte_im, "image/jpeg")}
    )
    return resp.json()

# ================================
# Routes
# ================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_image", methods=["POST"])
def upload_image():
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({"error": "No file selected."}), 400

    file = request.files['file']
    image = Image.open(file).convert("RGB")

    try:
        # Run prediction
        result = predict_with_roboflow(image)

        # Optionally draw boxes (if needed)
        detections = []
        status = "✅ Normal (No fire/smoke)"
        labels = []

        if "predictions" in result:
            for pred in result["predictions"]:
                label = pred["class"]
                conf = pred["confidence"]
                detections.append({
                    "name": label,
                    "confidence": round(conf * 100, 2),
                    "box": [pred["x"], pred["y"], pred["width"], pred["height"]]
                })
                labels.append(label)

        # Status summary
        if "wildfire" in labels and "smoke" in labels:
            status = "🔥 Fire and 💨 Smoke detected - CRITICAL ALERT 🔥"
        elif "wildfire" in labels:
            status = "🔥 Fire detected - ALERT"
        elif "smoke" in labels:
            status = "💨 Smoke detected - WARNING"

        return jsonify({
            "detections": detections,
            "status": status
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================================
# Run
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
