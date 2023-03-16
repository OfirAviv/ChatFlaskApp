from flask import Flask, request, render_template, redirect, url_for
import datetime
import mysql.connector
import socket
import os

app = Flask(__name__)

# db = mysql.connector.connect(
#   host="db",
#   user="root",
#   password="password",
#   database="access_log"
# )
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# creates a root route, by default this room name is 'general'
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<room>")
def room(room):
    return render_template("index.html")

@app.route("/chat/<room>")
def get_chat_solo(room):
    with open('/app/rooms/' + room + ".txt", "r") as file:
        chat = file.read()
    return chat, {"Content-Type":"text/plain"}

@app.route("/api/chat/<room>")
def get_chat(room):
    if not os.path.exists('/app/rooms/' + room + ".txt"):
        open('/app/rooms/' + room + ".txt", 'a').close()
    with open('/app/rooms/' + room + ".txt", "r") as file:
        chat = file.read()
    return chat ,{"Content-Type":"text/plain"}

@app.route("/api/chat/<room>", methods=["POST"])
def post_chat(room):
    user = request.form["username"]
    message = request.form["msg"]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('/app/rooms/' + room + ".txt", "w") as file:
        file.write(f'{timestamp} {user}: {message}\n')
    return redirect(url_for("get_chat", room=room))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
