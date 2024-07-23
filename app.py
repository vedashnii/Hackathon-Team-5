from flask import Flask, render_template, request, redirect, session, url_for, make_response
import career
import os
import string
import random
import requests
import json


from aixplain.factories import PipelineFactory
pipeline = PipelineFactory.get("66a007ce561ded999ac14abf")

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
    chat_id = str(''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10)))
    chats[chat_id] = [{
        "role": "system",
        "content": "This is an interview in which the assistant asks a single question at a time. The assistant's first question was: What language would you like to conduct the interview in?"
    }]

    # AI 
    res = pipeline.run({
        'Text': request.args["language"],
        'History': json.dumps(chats[chat_id]),
    })
    if res["data"][0]["segments"][0]["is_url"]:
        res = str(requests.get(res["data"][0]["segments"][0]["response"]).text)
    else:
        res = str(res["data"][0]["segments"][0]["response"])

    # Add messages
    chats[chat_id].append({
        "role": "user",
        "content": request.args["language"],
    })
    chats[chat_id].append({
        "role": "assistant",
        "content": res
    })
    session["chatid"] = chat_id

    response = make_response(res, 200)
    response.mimetype = "text/plain"
    return response

@app.route("/api/handlechat", methods=["POST"])
def handleChat():
    chat_id = session["chatid"]
    req = request.get_json()
    res = pipeline.run({
        'Text': req["content"],
        'History': json.dumps(chats[chat_id]),
    })
    if res["data"][0]["segments"][0]["is_url"]:
        if not res["data"][0]["segments"][0]["success"]:
            res = str(res["data"][0]["segments"][0]["error"])
        else:
            res = str(requests.get(res["data"][0]["segments"][0]["response"]).text)
    else:
        res = str(res["data"][0]["segments"][0]["response"])

    chats[chat_id].append(req)
    chats[chat_id].append({
        "role": "assistant",
        "content": res
    })
    print(chats)

    response = make_response(res, 200)
    response.mimetype = "text/plain"
    return response

if __name__ == "__main__":
    import os
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)