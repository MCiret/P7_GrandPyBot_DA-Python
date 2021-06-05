/*
The object is 1 interaction (i.e 1 user's question + 1 GrandPy Bot answer).

Answer = 1 address (text) + 1 here.com Map with the mark (see map.js) + 1 Wikipedia link (see wiki.js)
for the location extracted from the user's question (if the location has been found by here.com)
*/

'use strict';

class OneDiscuss {
    constructor(question, answer) {
        this.question = question;
        this.answer = answer;
    }

    display_all(chat_div, map_div) {
        /* Chat displaying */
        chat_div.append(this.format_question());
        chat_div.lastElementChild.insertAdjacentHTML('beforeend', this.format_map_answer(map_div));
        chat_div.lastElementChild.insertAdjacentHTML('beforeend', this.format_wiki_answer(map_div));

        chat_div.scrollTop = chat_div.scrollHeight; // to always see the last messages
    }

    format_question() {
        let msg = document.createElement('p');
        msg.id = "msg";
        msg.innerHTML = "Vous : " + this.question + "<br>";
        return msg
    }

    format_map_answer(map_div) {
        if (this.answer.map_resp) {
            map_div.innerHTML = ""; // empty the div to replace with new map
            let map = new Map(this.answer.lat, this.answer.long, map_div);
            map.platform_map_type(this.answer.apikey);
            map.display_map();
            return "GrandPy Bot : j'ai trouvé ! Ce lieu est à l'adresse 📍 "
            + this.answer.address + " 📍 <br>";
        }
        else {
            return "GrandPy Bot : Je ne trouve pas le lieu que vous recherchez...\
            Peut-être pouvez-vous préciser le nom ou éventuellement rajouter le pays, la ville, etc.";
        }
    }

    format_wiki_answer() {
        if (this.answer.wiki_resp) {
            return "GrandPy Bot : mais attendez mon petit, je ne vous ai jamais conté toute l'histoire de cet endroit \
            qui a marqué mon enfance ?! En effet, voyez-vous " + this.answer.extract +
            " <a href="+this.answer.url+">[En savoir plus sur Wikipédia]</a>";
        } else {
            return "";
        }
    }
}
