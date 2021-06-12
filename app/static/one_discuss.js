/*
The object is 1 interaction (i.e 1 user's question + 1 GrandPy Bot answer).

Question = The user's input and the animated loader icon.

Answer = 1 address (text) + marked Map (see map.js) + start and link of Wikipedia article.
*/

'use strict';

class OneDiscuss {
    constructor(question, loader_div, answer) {
        this.question = question;
        this.loader_div = loader_div;
        this.answer = answer;
    }

    display_question(chat_div) {
        /* Chat displaying */
        this.format_question();
        chat_div.append(this.msg_div);
        this.loader_div.className = "loader";
        chat_div.append(this.loader_div);
    }

    display_answer(chat_div, map_div) {
        this.msg_div.insertAdjacentHTML('beforeend', this.format_map_answer(map_div));
        this.msg_div.insertAdjacentHTML('beforeend', this.format_wiki_answer(map_div));
        this.loader_div.className = "hide_loader";
        chat_div.scrollTop = chat_div.scrollHeight; // to always see the last messages
    }

    format_question() {
        this.msg_div = document.createElement('p');
        this.msg_div.id = "msg";
        /* Protected against XSS attack */
        this.msg_div.textContent = "Vous : " + this.question;
        this.msg_div.insertAdjacentHTML('beforeend', "<br><br>");
    }

    format_map_answer(map_div) {
        if (this.answer.map_resp) {
            map_div.innerHTML = ""; // empty the div to replace with new map
            let map = new Map(this.answer.lat, this.answer.long, map_div);
            map.platform_map_type(this.answer.apikey);
            map.display_map();
            return "🤖 👴 GrandPy Bot : j'ai trouvé ! Ce lieu est à l'adresse 📍 "
            + this.answer.address + " 📍 <br>";
        }
        else {
            return "🤖 👴 GrandPy Bot : Je ne trouve pas le lieu que vous recherchez...\
            Peut-être pouvez-vous préciser le nom ou éventuellement rajouter le pays, la ville, etc.";
        }
    }

    format_wiki_answer() {
        if (this.answer.wiki_resp) {
            return "🤖 👴 GrandPy Bot : mais attendez mon petit, je ne vous ai jamais conté toute l'histoire de cet endroit \
            qui a marqué mon enfance ?! En effet, voyez-vous " + this.answer.extract +
            " <a href="+this.answer.url+">[En savoir plus sur Wikipédia]</a>";
        } else {
            return "";
        }
    }
}
