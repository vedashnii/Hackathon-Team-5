from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")
@app.route("/careerquiz")
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

if __name__ == "__main__":
    import os
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)