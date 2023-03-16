from flask import Flask, request
import datetime

app = Flask(__name__, static_url_path="", static_folder=".")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/<room>")
def room(room):
    return app.send_static_file("index.html")

@app.route("/chat/<room>")
def get_chat(room):
    return 

@app.route("/api/chat/<room>", methods=["POST"])
def post_chat(room):
    return 

if __name__ == "__main__":
    app.run(host="0.0.0.0")
