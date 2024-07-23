(async () => {
    let res = await fetch("/api/newchat");
    let responseEl = document.createElement("div");
    responseEl.className = "msg aimsg";
    responseEl.innerHTML = await res.text();
    document.getElementById("msgbox").appendChild(responseEl);

    document.getElementById("input").disabled = false;

})();

async function send(event) {
    event.preventDefault();

    let text = document.getElementById("input").value;
    let el = document.createElement("div");
    el.className = "msg usermsg";
    el.innerHTML = text;
    document.getElementById("msgbox").appendChild(el);
    document.getElementById("input").value = "";
    document.getElementById("input").disabled = true;

    let res = await fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ "role": "user", "content": text }),
    });
    let response = await chatgpt.getLastResponse();
    let responseEl = document.createElement("div");
    responseEl.className = "msg aimsg";
    responseEl.innerHTML = response;
    document.getElementById("msgbox").appendChild(responseEl);
    document.getElementById("input").disabled = false;
}