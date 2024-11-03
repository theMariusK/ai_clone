from flask import Flask, request, jsonify
from services.image_service import store_image_in_mongodb
from services.video_service import store_video_locally
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi'}

# Helper function to check if the file extension is allowed
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Route to upload images to MongoDB
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    
    if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename = secure_filename(file.filename)
        # Call the service function to store the image in MongoDB
        store_image_in_mongodb(file, filename)
        return jsonify({'message': f'Image {filename} uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

# Route to upload videos to local storage
@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    
    if file and allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
        filename = secure_filename(file.filename)
        # Call the service function to store the video locally
        store_video_locally(file, filename)
        return jsonify({'message': f'Video {filename} uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(debug=True)
