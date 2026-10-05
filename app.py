from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MongoDB_URL")

client = MongoClient(mongo_uri)
db = client["todo_db"]
todo_collection = db["todos"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)
@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    todo_collection.insert_one(todo)

    return """
    <h1>To-Do item submitted successfully!</h1>
    <a href="/">Go Back</a>
    """


if __name__ == "__main__":
    app.run(debug=True)
