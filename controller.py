from deta import Deta
from flask import jsonify

deta = Deta("a0w75vy2_WqxibULeGjATvRgcu3mRwLYRKuCfpaye")
users = deta.Base('users')
articles = deta.Base('articles')
visitors = deta.Base('visitors')

# function for add users
def insert_user(name, address, about, email, password, imageUrl):
    user = users.put({
        "name": name,
        "address": address,
        "about": about,
        "email": email,
        "password": password,
        "imageUrl": imageUrl
    })
    
    return jsonify(user, 201)

# function for login
def login(email, password):
    query = users.fetch({
        "email": email,
        "password": password
    })._items
    # print(query)
    if query:
        return jsonify({"success": True, "message":"Login Successfully", "key": query[0]['key']})
    else:
        return (jsonify({"success": False, "message": "Invalid email/password"}), 404)

# function for display user details
def user_detail(key):
    user = users.get(key)
    return user if user else (jsonify({"message":"Not Found"}), 404)

# function for fetch all data
def get_users():
    all_user = users.fetch()._items
    return jsonify(all_user)

# function for insert new article
def insert_article(title, content, urlToImage, created_at):
    article = articles.put({
        "title": title,
        "content": content,
        "urlToImage": urlToImage,
        "created_at": created_at
    })
    return article

# def get_articles()
def get_all_article():
    all_article = articles.fetch()._items
    return all_article

# def get_article_by_key()

# def delete_article_by_key()

# function for add vistor
def insert_visitor(name, address, phone, message, visiting_time):
    visitor = visitors.put({
        "name": name,
        "address": address,
        "phone": phone,
        "message": message,
        "visiting_time": visiting_time
    })
    
    return (visitor, 201)

# function for get all vistor
def get_visitors():
    return jsonify({"items" : visitors.fetch()._items})

# function for handling error when response 500
def internalServerError():
    return jsonify({"message": "Internal Server Error"})

# function for handling error when respin
def badRequest():
    return jsonify({"message": "Bad Request"})