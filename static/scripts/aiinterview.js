let started = false;

async function send(event) {
    event.preventDefault();

    if (!started) {
        document.getElementById("input").disabled = true;
        let res = await (await fetch("/api/newchat?language=" + document.getElementById("input").value)).text();
        let responseEl = document.createElement("div");
        responseEl.className = "msg aimsg";
        responseEl.innerHTML = res;
        console.log(res);

        document.getElementsByClassName("msg-box").appendChild(responseEl);
        document.getElementById("input").disabled = false;
        started = true;
        return;
    }

    let text = document.getElementById("input").value;
    let el = document.createElement("div");
    el.className = "msg usermsg";
    el.innerHTML = text;
    document.getElementsByClassName("msg-box").appendChild(el);
    document.getElementById("input").value = "";
    document.getElementById("input").disabled = true;

    let res = await (await fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ "role": "user", "content": text }),
    })).text();
    let responseEl = document.createElement("div");
    responseEl.className = "msg aimsg";
    responseEl.innerHTML = res;
    document.getElementsByClassName("msg-box").appendChild(responseEl);
    document.getElementById("input").disabled = false;
}