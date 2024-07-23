from flask import Flask, render_template, request, redirect, session, url_for
import career
from openai import OpenAI
import os
import string
import random

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_KEY"),
)

app = Flask(__name__)
app.secret_key = "abcdefg"

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")
@app.route("/careerquiz")
@app.route("/quiz")
def quiz():
    return render_template("startquiz.html")

@app.route("/careerinit")
def careerFirstPage():
    new_career = career.init()
    return render_template("career.html", job=new_career.get("name"), desc=new_career.get("description"), salary=new_career.get("salary"), category=new_career.get("category"), degree=new_career.get("degree"))
@app.route("/careernotforme")
def careerRejectPage():
    new_career = career.newCareer(prevReject=True)
    if (new_career != "END"):
        return render_template("career.html", job=new_career.get("name"), desc=new_career.get("description"), salary=new_career.get("salary"), category=new_career.get("category"), degree=new_career.get("degree"))
    else:
        return redirect(url_for("buildResume"))
@app.route("/careerfavorite")
def careerFavoritePage():
    new_career = career.newCareer(prevReject=False)
    if (new_career != "END"):
        return render_template("career.html", job=new_career.get("name"), desc=new_career.get("description"), salary=new_career.get("salary"), category=new_career.get("category"), degree=new_career.get("degree"))
    else:
        return redirect(url_for("buildResume"))

@app.route("/resumebuilder")
def buildResume():
    return render_template("resumebuilder.html")

@app.route("/aiinterviewer")
def aiInterviewer():
    return render_template("aiinterviewer.html")


# CHATGPT
chats = {}
@app.route("/api/newchat", methods=["GET"])
def newChat():
    chat_id = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10))
    chats[chat_id] = [{
        "role": "system",
        "content": "You are interviewing me. First, ask me what language you would like to interview me in."
    }]
    res = client.chat.completions.create( 
        model="gpt-3.5-turbo", messages=chats[chat_id] 
    ) 
    session["chatid"] = id
    return res

@app.route("/api/handlechat", methods=["POST"])
def handleChat():
    chat_id = session["chatid"]
    chats[chat_id].append(request.get_json())
    res = client.chat.completions.create( 
        model="gpt-3.5-turbo", messages=chats[chat_id] 
    )
    return res

if __name__ == "__main__":
    import os
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)