from deta import Deta
import os
from flask import jsonify, Response

deta = Deta("a0w75vy2_WqxibULeGjATvRgcu3mRwLYRKuCfpaye")
users = deta.Base('users')
articles = deta.Base('articles')

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
    query = users.fetch(query={
        "email": email,
        "password": password
    })._items
    # print(query)
    if query:
        return jsonify({"success": True, "message":""})
    else:
        return jsonify({"success": False, "message": "Invalid email/password"})

# function for fetch all data
def get_users():
    all_user = users.fetch()._items
    return jsonify(all_user)

# def insert_article()
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

# def get_article_by_id()

# def delete_article_by_id()

