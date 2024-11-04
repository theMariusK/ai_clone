# backend/app.py
from flask import Flask, jsonify, request
from api_gateway.gateway import api_gateway
from database.mongo_connection import initialize_db

app = Flask(__name__)

# Initialize MongoDB connection
initialize_db()

# Register API Gateway
app.register_blueprint(api_gateway, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the API Gateway!'})

if __name__ == "__main__":
    app.run(debug=True)
