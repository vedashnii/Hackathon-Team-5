let started = false;

async function send(event) {
    event.preventDefault();

    if (!started) {
        let text = document.getElementById("input").value;
        let el = document.createElement("div");
        el.className = "msg usermsg";
        el.innerHTML = text;
        document.getElementById("msg-box").prepend(el);
        document.getElementById("input").value = "";
        document.getElementById("input").disabled = true;

        let res = await (await fetch("/api/newchat?language=" + text)).text();
        let responseEl = document.createElement("div");
        responseEl.className = "msg aimsg";
        responseEl.innerHTML = res;

        document.getElementById("msg-box").prepend(responseEl);
        document.getElementById("input").disabled = false;
        started = true;
        return;
    }

    let text = document.getElementById("input").value;
    let el = document.createElement("div");
    el.className = "msg usermsg";
    el.innerHTML = text;
    document.getElementById("msg-box").prepend(el);
    document.getElementById("input").value = "";
    document.getElementById("input").disabled = true;

    let res = await (await fetch("/api/handlechat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ "role": "user", "content": text }),
    })).text();
    let responseEl = document.createElement("div");
    responseEl.className = "msg aimsg";
    responseEl.innerHTML = res;
    document.getElementById("msg-box").prepend(responseEl);
    document.getElementById("input").disabled = false;
}