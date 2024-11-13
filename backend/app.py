from flask import Flask, request, jsonify
from api_gateway.config import API_VERSION
from database.storage import initialize_storage, store_video, get_file, delete_file

app = Flask(__name__)



# Video routes

@app.route(f"/{API_VERSION}/video", methods=['POST'])
def upload_video_route():
    print("upload_video")
    
    video_file = request.files['file']
    
    result = store_video(video_file)

    return jsonify({"message": "Video uploaded successfully", "video_id": str(result)})

@app.route(f"/{API_VERSION}/video/<video_id>", methods=['GET'])
def get_video_route(video_id):
    video_data = get_file(video_id)
    if video_data:
        return jsonify({"video_id": video_id, "video_data": video_data}), 200
    else:
        return jsonify({"message": "Video not found"}), 404



# Common routes

@app.route(f"/{API_VERSION}/<file_id>", methods=['DELETE'])
def delete_file_route(file_id):
    result = delete_file(file_id)
    if result:
        return jsonify({"message": "File deleted successfully"}), 200
    else:
        return jsonify({"message": "File not found"}), 404

@app.route(f"/{API_VERSION}/test", methods=["GET"])
def test_route():
    print("test")
    return jsonify({"message": "Test route is working"}), 200



# Run
 
if __name__ == "__main__":
    initialize_storage()
    app.run(host='0.0.0.0', port=5000)
