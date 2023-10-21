import os
import cv2
from datetime import datetime
from flask import Flask, jsonify

# Set the default directory to "/camera_module/image_output/"
DEFAULT_OUTPUT_DIR = 'image_output/'

def ensure_dir_exists(dir_path):
    """Ensure the specified directory exists. If it doesn't, create it."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

class Camera:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id)
        # Check if the camera is opened successfully
        if not self.cap.isOpened():
            raise ValueError("Could not open video device")

    def capture_still(self, output_dir=DEFAULT_OUTPUT_DIR):
        ret, frame = self.cap.read()
        if not ret:
            return None
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/capture_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        return filename

    def release(self):
        self.cap.release()

app = Flask(__name__)
camera = None

@app.route('/capture', methods=['POST'])
def flask_capture_image():
    file_path = camera.capture_still()
    if file_path:
        return jsonify(status='success', path=file_path)
    return jsonify(status='failure'), 500

@app.before_first_request
def initialize():
    global camera
    camera = Camera()

@app.teardown_appcontext
def cleanup(exception):
    camera.release()

if __name__ == "__main__":
    app.run(debug=True)
