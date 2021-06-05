/* This is the "main" JavaScript script :
    - Event listening
    - Event reaction : fetch data to backend and then format + display the response
*/


'use strict';

let form = document.querySelector("#user_request");
let chat_div = document.querySelector("#chat");
let map_div = document.querySelector("#map");

form.addEventListener("submit", async function(event) {
    event.preventDefault();
    const RESULT = await postData("/", new FormData(form));
    const FINAL_RES = await RESULT.json();
    const DISCUSS = new OneDiscuss(form["question"].value, FINAL_RES);
    DISCUSS.display_all(chat_div, map_div);
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
