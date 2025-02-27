#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, render_template, redirect, url_for
from data_loader import load_dataset, load_item_data
from data_preprocessor import create_user_item_matrix, map_item_ids_to_names
from recommendation_engine import SVDRecommendationEngine
from user_database import UserDatabase
import json

app = Flask(__name__)

# Load dataset and create user-item matrix
file_path = r"C:\Users\LENOVO\Downloads\ml-100k\u.data"
columns = ["user_id", "item_id", "rating", "timestamp"]
data = load_dataset(file_path, columns)

name_path =  r"C:\Users\LENOVO\Downloads\ml-100k\u.item"
name_data = load_item_data(name_path)
item_id_to_name = map_item_ids_to_names(name_data)

# Create user-item matrix
user_item_matrix = create_user_item_matrix(data)

# Create recommendation engine and user database
recommendation_engine = SVDRecommendationEngine(user_item_matrix)
user_database = UserDatabase("users.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = user_database.get_user(username)
    if user and user["password"] == password:
        return render_template("watchlist.html", username=username, movies=item_id_to_name.values())
    else:
        return "Invalid username or password", 401

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user_database.create_user(username, password):
            return "Account created successfully!"
        else:
            return "Username already exists", 400
    else:
        return render_template("create_account.html")

@app.route("/watchlist/<username>", methods=["GET"])
def watchlist(username):
    user = user_database.get_user(username)
    if user:
        watchlist = user["watchlist"].split(",") if user["watchlist"] else []
        user_watchlist = [movie for movie in watchlist]
        movies = [movie for movie in item_id_to_name.values() if movie not in watchlist]
        return render_template("watchlist.html", 
                                 username=username, 
                                 movies=movies, 
                                 user_watchlist=user_watchlist)
    else:
        return "User not found", 404

@app.route("/update_watchlist", methods=["POST"])
def update_watchlist():
    username = request.form["username"]
    watchlist = request.form.getlist("watchlist")
    watchlist = [json.loads(movie) for movie in watchlist if movie]
    if watchlist:  # Check if the list is not empty
        movie_names = [movie["movie"] for movie in watchlist]
        user_database.update_watchlist(username, movie_names)
    return redirect(url_for('watchlist', username=username))

@app.route("/recommendations", methods=["POST"])
def get_recommendations():
    username = request.form["username"]
    user = user_database.get_user(username)
    if user:
        user_id = user["id"]
        recommendations = recommendation_engine.generate_recommendations(user_id - 1, item_id_to_name)
        return render_template("recommendations.html", recommendations=recommendations)
    else:
        return "User not found", 404

if __name__ == "__main__":
    app.run(debug=True)

