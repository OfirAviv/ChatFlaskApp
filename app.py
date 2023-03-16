from flask import Flask, request, render_template, redirect, url_for
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<room>")
def room(room):
    return render_template("index.html")

@app.route("/chat/<room>")
def get_chat_solo(room):
    with open('C:/Users/ofir8/Desktop/chat/rooms/' + room + ".txt", "r") as file:
        chat = file.read()
        # with open("C:\Users\ofir8\Desktop\chat\rooms" + room + ".txt", "a" ) as file:
        #     file.write(formatted_chat)
    return chat, {"Content-Type":"text/plain"}

@app.route("/api/chat/<room>")
def get_chat(room):
    with open('C:/Users/ofir8/Desktop/chat/rooms/' + room + ".txt", "r") as file:
        chat = file.read()
        # with open("C:\Users\ofir8\Desktop\chat\rooms" + room + ".txt", "a" ) as file:
        #     file.write(formatted_chat)
    return chat, {"Content-Type":"text/plain"}

@app.route("/api/chat/<room>", methods=["POST"])
def post_chat(room):
    user = request.form["username"]
    message = request.form["msg"]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('C:/Users/ofir8/Desktop/chat/rooms/' + room + ".txt", "a+") as file:
        file.write(f'{timestamp} {user}: {message}\n')
    return redirect(url_for("get_chat"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
