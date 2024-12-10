from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
import urllib.request

app = Flask(__name__)

# File upload path
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Refined color detection logic
def detect_color(bgr):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    # Define HSV ranges for each color
    color_ranges = {
        'Red': [(0, 50, 50), (10, 255, 255)],       # Lower red range
        'Green': [(35, 50, 50), (85, 255, 255)],    # Green range
        'Blue': [(100, 50, 50), (130, 255, 255)],   # Blue range
        'Yellow': [(20, 50, 50), (30, 255, 255)],   # Yellow range
        'Cyan': [(85, 50, 50), (95, 255, 255)],     # Cyan range
        'Magenta': [(140, 50, 50), (160, 255, 255)],# Magenta range
        'Black': [(0, 0, 0), (180, 255, 50)],       # Black range
        'White': [(0, 0, 200), (180, 55, 255)],     # White range
        'Gray': [(0, 0, 50), (180, 50, 200)]        # Gray range
    }

    # Check which range the HSV value falls into
    for color, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)
        if cv2.inRange(np.uint8([[hsv]]), lower_bound, upper_bound).any():
            return color

    return "Unknown"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect-color', methods=['POST'])
def detect_color_api():
    # Handle image upload or URL input
    if 'file' in request.files:
        # If the user uploads a file
        image_file = request.files['file']
        image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)
    elif 'url' in request.form:
        # If the user provides an image URL
        image_url = request.form['url']
        image_path = os.path.join(UPLOAD_FOLDER, 'image_from_url.jpg')
        urllib.request.urlretrieve(image_url, image_path)
    else:
        return jsonify({'error': 'No file or URL provided'}), 400

    # Process the image
    image = cv2.imread(image_path)
    x = int(request.form['x'])
    y = int(request.form['y'])
    bgr = image[y, x]  # Get pixel at (x, y)
    color = detect_color(bgr)
    return jsonify({'color': color})

if __name__ == '__main__':
    app.run(debug=True)
