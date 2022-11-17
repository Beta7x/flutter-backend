import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging
import os
import json
import controller
from werkzeug import exceptions
from datetime import datetime as dt
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

load_dotenv()
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

default_avatar = "https://res.cloudinary.com/beta7x/image/upload/v1668309378/utscrud/file.jpg"
default_article_image = "https://res.cloudinary.com/beta7x/image/upload/v1668353094/flutter-backend/6_nyvwcv.jpg"

current_time = json.dumps(dt.now().strftime('%A, %d %B %Y %H:%M:%S'))


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

@app.route('/users/<key>', methods=['GET'])
def user_details(key):
    result = controller.user_detail(key)
    return result

@app.route('/users')
def get_users():
    return controller.get_users()

@app.route('/articles/add', methods=['POST'])
def add_article():
    app.logger.info("In article route ['POST']")
    
    title = request.form.get('title')
    content = request.form.get('content')
    
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key = os.getenv('API_KEY'),
                      api_secret = os.getenv('API_SECRET'))
    upload_result = None
    
    if request.method == 'POST':
        image_article = request.files['image']
        if image_article:
            upload_result = cloudinary.uploader.upload(
                image_article,
                unique_filename = True,
                folder = "flutter-backend/articles"
            )
            return controller.insert_article(
                title, content, upload_result['secure_url'], current_time
            )
        else:
            return controller.insert_article(
                title, content, default_article_image, current_time
            )
    
@app.route('/articles')
def get_articles():
    return controller.get_all_article()

@app.route('/visitors/add', methods=['POST'])
def add_visitor():
    visitor_details = request.get_json()
    name = visitor_details['name']
    address = visitor_details['address']
    phone = visitor_details['phone']
    message = visitor_details['message']
    
    result = controller.insert_visitor(name, address, phone, message, current_time)
    
    return result

@app.route('/visitors')
def get_visitors():
    return controller.get_visitors()

@app.route('/visitors/<key>', methods=['DELETE'])
def remove_visitor(key):
    return controller.delete_visitor(key)

#Error handling Bad Request
@app.errorhandler(exceptions.BadRequest)
def handle_bad_request():
    return controller.badRequest() 

# Error Handling Internal Server Error
@app.errorhandler(exceptions.InternalServerError)
def handle_interna_server_error():
    return controller.internalServerError()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)