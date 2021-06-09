/* This is the "main" JavaScript script :
    - Event listening
    - Event reaction : fetch data to backend and then format + display the response
*/


'use strict';

let form = document.querySelector("#user_request");
let user_text = document.querySelector("#question");
let loader_div = document.createElement('img');
loader_div.src = '../static/refresh.svg';
loader_div.alt = 'icone loader';
loader_div.className = 'hide_loader';
let chat_div = document.querySelector("#chat");
let map_div = document.querySelector("#map");

form.addEventListener("submit", async function(event) {
    event.preventDefault();
    let DISCUSS = new OneDiscuss(form["question"].value, loader_div);
    DISCUSS.display_question(chat_div);
    const RESULT = await postData("/", new FormData(form));
    const FINAL_RES = await RESULT.json();
    DISCUSS.answer = FINAL_RES;
    DISCUSS.display_answer(chat_div, map_div);
})

function postData(url, data) {
    try {
        return fetch(url, {
                method: "POST",
                body: data,
            });
    } catch (err) {
        console.log(err);
    }
}
