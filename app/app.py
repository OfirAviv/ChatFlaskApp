from flask import Flask, request, render_template, redirect, url_for
import datetime
import mysql.connector
import socket
import os

app = Flask(__name__)

# creates a connection to the db container
db = mysql.connector.connect(
  host="db",
  user="root",
  password="password",
  database="chatLogs"
)
# makes a pool configuration so all of the data will be persistent through the 3 containers
pool_config = {
    "pool_name": "mypool",
    "pool_size": 3,
    "host": "db",
    "user": "root",
    "password": "password",
    "database": "chatLogs"
}
pool = mysql.connector.pooling.MySQLConnectionPool(**pool_config)
# creates a root route, by default this room name is 'general'
@app.route("/")
def index():
    return render_template("index.html")

# makes a route to /<room>, this is regarding any name to <room>
@app.route("/<room>")
def room(room):
    return render_template("index.html")

# makes a route to /chat/<room>, this is regarding any name to <room>
@app.route("/chat/<room>")
def get_chat_solo(room):
    # SELECT is selecting the given values in the connected db & table (chatLogs and chat) if the column 'room' is equal to the variable
    connection = pool.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT logged, username, messages FROM chat WHERE room = %s", (room,))
    chat = cursor.fetchall()
    formatted_chat = [f"[{msg[0]}] {msg[1]}: {msg[2]}" for msg in chat]
    connection.close()
    return os.linesep.join(formatted_chat) + '\n'

@app.route("/api/chat/<room>")
def get_chat(room):
    # this is socket, this allows us to see the internal ip of the container, I did this for proving load-balancing
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("8.8.8.8", 80))
    internal_ip_add = s.getsockname()[0]
    # SELECT is selecting said columns if the column 'room' is equal to the variable
    connection = pool.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT logged, username, messages FROM chat WHERE room = %s", (room,))
    chat = cursor.fetchall()
    # formatted_chat is responsible for beautifying the chat, making it our desired format of '<timestamp> <username>: <message>' after the command 'join'
    formatted_chat = [f"[{msg[0]}] {msg[1]}: {msg[2]}" for msg in chat]
    connection.close()
    # returning the internal ip address of the containar AND using 'join' to provide the desired format
    return f'{internal_ip_add}\n' + "\n".join(formatted_chat)

@app.route("/api/chat/<room>", methods=["POST"])
def post_chat(room):
    # user.form["<something>"] is responsible for pulling inputs for HTMLs, in our case 'index.html'
    user = request.form["username"]
    message = request.form["msg"]
    # using the datetime library to get the current time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # INSERT is responsible for inserting given values, by order, to the already connected db & table, in our case chat
    connection = pool.get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO chat (room, logged, username, messages) VALUES(%s, %s, %s, %s)", (room, str(timestamp), user, message))
    connection.commit()
    connection.close()
    return redirect(url_for("get_chat", room=room))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
