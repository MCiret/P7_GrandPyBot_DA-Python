import config as cfg
import app.api_requests as api
from app.parser import Parser


def parse_question(whole_question: str):
    parsed_question = Parser(whole_question)
    parsed_question.extract_interesting_tokens()

    if len(parsed_question.interesting_tokens) == 0:
        return None

    return {
        "formated": {
            "parsed_key_words": "_".join(parsed_question.interesting_tokens),
            "capitalized": "_".join(Parser.capitalize_all_words(parsed_question.interesting_tokens)),
            "decapitalized": "_".join(Parser.decapitalize_all_words(parsed_question.interesting_tokens)),
        },
        "singled": tuple((kw, Parser.word_reverse_case_first_char(kw))
                         for kw in parsed_question.interesting_tokens)
    }


def maps_position(location: str):
    return api.resp_dict_to_location(
                api.api_request_and_get_dict_resp(cfg.HERE_API_URL, apikey=cfg.HERE_API_KEY, q=location))


def wiki_infos(location: str):
    return api.resp_dict_to_wiki_infos(
                api.api_request_and_get_dict_resp(cfg.WIKI_API_URL, **cfg.WIKI_API_PARAMS, titles=location))


def try_formated_key_words(formated_key_words: dict):

    formated_key_words_tuple = (formated_key_words["parsed_key_words"],
                                formated_key_words["capitalized"],
                                formated_key_words["decapitalized"])

    for kw in formated_key_words_tuple:
        map_api_resp = maps_position(kw)
        if map_api_resp["map_resp"]:
            break

    for kw in formated_key_words_tuple:
        wiki_api_resp = wiki_infos(kw)
        if wiki_api_resp["wiki_resp"]:
            break

    return {
        **map_api_resp, **wiki_api_resp  # dicos concatenation
    }


def try_singled_key_words(singled_key_words: tuple):
    key_words_couples = (couple for couple in singled_key_words)

    for kwc in key_words_couples:
        for kw in kwc:
            map_api_resp = maps_position(kw)
            if map_api_resp["map_resp"]:
                wiki_api_resp = wiki_infos(kw)
                if wiki_api_resp["wiki_resp"]:
                    return {
                        **map_api_resp, **wiki_api_resp  # dicos concatenation
                    }
    return {
        **map_api_resp  # dicos concatenation
        }


def answer(whole_question):
    parsed_question_dict = parse_question(whole_question)

    if parsed_question_dict is not None:
        final_answer = try_formated_key_words(parsed_question_dict["formated"])
        if not final_answer["map_resp"]:
            final_answer_last_chance = try_singled_key_words(parsed_question_dict["singled"])
            if final_answer_last_chance["map_resp"] and "wiki_resp" in final_answer_last_chance.keys():
                if final_answer_last_chance["wiki_resp"]:
                    return final_answer_last_chance
                else:
                    return {"error": "Failing wiki API requesting..."}
            else:
                return {"error": "Failing wiki API requesting..."}
        else:
            return final_answer
    else:
        return {"error": "Parser failed..."}
