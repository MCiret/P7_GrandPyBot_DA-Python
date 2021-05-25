'use strict';

let form = document.querySelector("#user_request");

form.addEventListener("submit", async function(event) {
    event.preventDefault();
    let result = await postData("/", new FormData(form));
    let final_res = await result.json();
    chat_display_one_discuss(final_res.text);
    chat_display_one_discuss("je réfléchis...", false);
})

function postData(url, data) {
    try {
        let response = fetch(url, {
                method: "POST",
                body: data,
            });
        return response;
    } catch (err) {
        console.log(err);
    }
}

function chat_display_one_discuss(text, user=true) {
    if (user) { // if it is user's question, new <p> section is created
        let msg = document.createElement('p');
        msg.id = "msg";
        msg.innerHTML = "Vous : " + text + "<br>";
        chat.append(msg);
    } else {
        chat.lastElementChild.append("GrandPy Bot : ", text);
    }
}