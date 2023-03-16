from flask import Flask, request, render_template, redirect, url_for
import datetime
import mysql.connector
import socket
import os

app = Flask(__name__)

db = mysql.connector.connect(
  host="db",
  user="root",
  password="password",
  database="chatLogs"
)
# creates a root route, by default this room name is 'general'
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<room>")
def room(room):
    return render_template("index.html")

@app.route("/chat/<room>")
def get_chat_solo(room):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("8.8.8.8", 80))
    internal_ip_add = s.getsockname()[0]
    cursor = db.cursor()
    cursor.execute("SELECT logged, username, messages FROM chat WHERE room = %s", (room,))
    chat = cursor.fetchall()
    formatted_chat = [f"[{msg[0]}] {msg[1]}: {msg[2]}" for msg in chat]
    cursor.close()
    return os.linesep.join(formatted_chat) + '\n'

@app.route("/api/chat/<room>")
def get_chat(room):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("8.8.8.8", 80))
    internal_ip_add = s.getsockname()[0]
    cursor = db.cursor()
    cursor.execute("SELECT logged, username, messages FROM chat WHERE room = %s", (room,))
    chat = cursor.fetchall()
    formatted_chat = [f"[{msg[0]}] {msg[1]}: {msg[2]}" for msg in chat]
    cursor.close()
    return f'{internal_ip_add}\n' + "\n".join(formatted_chat)

@app.route("/api/chat/<room>", methods=["POST"])
def post_chat(room):
    user = request.form["username"]
    message = request.form["msg"]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = db.cursor()
    cursor.execute("INSERT INTO chat (room, logged, username, messages) VALUES(%s, %s, %s, %s)", (room, str(timestamp), user, message))
    db.commit()
    cursor.close()
    return redirect(url_for("get_chat", room=room))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
