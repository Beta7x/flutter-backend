import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging
import os
import controller
from dotenv import load_dotenv
from cloudinary.utils import cloudinary_url
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

load_dotenv()
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

default_avatar = "https://res.cloudinary.com/beta7x/image/upload/v1668309378/utscrud/file.jpg"

@app.route('/')
def index():
    return jsonify({"message": "Flask app running"})

@app.route('/users/add', methods=['POST'])
@cross_origin()
def create_user():
    app.logger.info("In users route ['POST']")
    
    name = request.form.get('name')
    address = request.form.get('address')
    about = request.form.get('about')
    email = request.form.get('email')
    password = request.form.get('password')
    
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key = os.getenv('API_KEY'),
                      api_secret = os.getenv('API_SECRET'))
    upload_result = None
    
    if request.method == 'POST':
        image_profile = request.files['image']
        
        if image_profile:
            upload_result = cloudinary.uploader.upload(
                image_profile,
                # use_filename = True,
                unique_filename = True,
                folder = "flutter-backend/avatar/"
            )
            # app.logger.info(upload_result)
            result = controller.insert_user(
                name, 
                address,
                about,
                email,
                password,
                upload_result['secure_url']
            )
            return result
            
        else:
            result = controller.insert_user(
                name, 
                address,
                about,
                email,
                password,
                default_avatar
            )
            return result

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    result = controller.login(email, password)
    return result

@app.route('/users')
def get_users():
    return controller.get_users()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)