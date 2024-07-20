from flask import Flask, render_template, request, redirect, session, url_for
import career

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")
@app.route("/careerquiz")
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/careerinit")
def careerFirstPage():
    new_career = career.init()
    return render_template("career.html", job=new_career[0], desc=new_career[1])
@app.route("/careernotforme")
def careerRejectPage():
    new_career = career.newCareer(prevReject=True)
    if (new_career != "END"):
        return render_template("career.html", job=new_career[0], desc=new_career[1])
    else:
        return redirect(url_for("buildResume"))
@app.route("/careerfavorite")
def careerFavoritePage():
    new_career = career.newCareer(prevReject=False)
    if (new_career != "END"):
        return render_template("career.html", job=new_career[0], desc=new_career[1])
    else:
        return redirect(url_for("buildResume"))

@app.route("/resumebuilder")
def buildResume():
    return render_template("resumebuilder.html")

if __name__ == "__main__":
    import os
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)