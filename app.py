from flask import Flask, render_template, request, send_from_directory, url_for
import tensorflow as tf
import numpy as np
import os
from werkzeug.utils import secure_filename

# Load model
MODEL_PATH = r"E:\Personal_Projects\cv\wildfire_detection_model (2).h5"
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

# Create Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Preprocessing function
def preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))  # change size if needed
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    probability = None
    filename = None
    play_sound = False   # Default: no sound

    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            return render_template('index.html', error="No file selected")

        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess and predict
        img_array = preprocess_image(filepath)
        predictions = model.predict(img_array)[0][0]  # adjust indexing based on model output
        probability = round(float(predictions) * 100, 2)

        if predictions >= 0.5:
            result = "🔥 Fire Detected"
            play_sound = True   # Play alarm if fire is detected
        else:
            result = "✅ No Fire"

    return render_template(
        'index.html',
        result=result,
        probability=probability,
        filename=filename,
        play_sound=play_sound
    )

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

