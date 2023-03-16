from flask import Flask, request, render_template, redirect, url_for
import datetime


app = Flask(__name__)

chats = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<room>")
def room(room):
    return render_template("index.html")

@app.route("/chat/<room>")
def get_chat_solo(room):
    if room in chats:
        chat = chats.get(room, [])
        formatted_chat = "\n".join(f"[{msg['timestamp']}] {msg['username']}: {msg['message']}" for msg in chat)
        return formatted_chat, {"Content-Type":"text/plain"}
    else:
        return "Error: Chat Not Found"

@app.route("/api/chat/<room>")
def get_chat(room):
    if room in chats:
        chat = chats.get(room, [])
        formatted_chat = "\n".join(f"[{msg['timestamp']}] {msg['username']}: {msg['message']}" for msg in chat)
        with open("C:\Users\ofir8\Desktop\chat\rooms" + room + ".txt", "a" ) as file:
            file.write(formatted_chat)
        return formatted_chat, {"Content-Type":"text/plain"}
    else:
        return "Error: Chat Not Found"

@app.route("/api/chat/<room>", methods=["POST"])
def post_chat(room):
    user = request.form["username"]
    message = request.form["msg"]
    chats.setdefault(room, [])
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chats[room].append({"username":user, "message":message,"timestamp":timestamp})
    return redirect(url_for("get_chat"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
