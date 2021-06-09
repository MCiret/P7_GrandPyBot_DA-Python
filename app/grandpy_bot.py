import config as cfg
import app.api_requests as api
# from app.parser import Parser


def parse_question(whole_question: str) -> dict:
    parsed_question = Parser(whole_question)
    parsed_question.extract_interesting_tokens()

    if len(parsed_question.interesting_tokens) == 0:
        return None

    return {
        "formated_original_key_words": " ".join(parsed_question.interesting_tokens),
        "singled_key_words": tuple((kw, Parser.word_reverse_case_first_char(kw))
                                   for kw in parsed_question.interesting_tokens)
    }


def maps_position(location: str) -> dict:
    return api.resp_dict_to_location(
                api.api_request_and_get_dict_resp(cfg.HERE_API_URL, apikey=cfg.HERE_API_KEY, q=location))


def wiki_infos(location: str) -> dict:
    return api.resp_dict_to_wiki_infos(
                api.api_request_and_get_dict_resp(cfg.WIKI_API_URL, **cfg.WIKI_API_PARAMS, titles=location))


def try_original_key_words(formated_original_key_words: str) -> dict:
    """
    Requests API using original parsed key words.

    To elevate results accuracy : if more relevant key words could be parsed from map API response parsing then it is
    used for Wikipedia request. Else original parsed key words are also used for Wikipedia request.
    """

    map_api_resp = maps_position(formated_original_key_words)

    if map_api_resp["map_resp"]:
        if map_api_resp["key_words"]:
            wiki_api_resp = wiki_infos(Parser.underscored_joined_words(map_api_resp["key_words"]))
            if not wiki_api_resp["wiki_resp"]:
                wiki_api_resp = wiki_infos(formated_original_key_words)
            return {
                **map_api_resp, **wiki_api_resp  # dicos concatenation
            }
        else:
            wiki_api_resp = wiki_infos(formated_original_key_words)
            return {
                **map_api_resp, **wiki_api_resp  # dicos concatenation
            }
    else:
        return map_api_resp


def try_singled_key_words(singled_key_words: tuple, map_ok: bool = False) -> dict:
    """
    Like a "last chance", if original parsed key words do not get a response from API then each word is tried alone
    and the first positive response is kept.
    """

    key_words_couples = (couple for couple in singled_key_words)

    if map_ok is False:
        for kwc in key_words_couples:
            for kw in kwc:
                map_api_resp = maps_position(kw)
                if map_api_resp["map_resp"]:
                    wiki_api_resp = wiki_infos(kw)
                    if wiki_api_resp["wiki_resp"]:
                        return {
                            **map_api_resp, **wiki_api_resp  # dicos concatenation
                        }
            return map_api_resp
    else:
        for kwc in key_words_couples:
            for kw in kwc:
                wiki_api_resp = wiki_infos(kw)
                if wiki_api_resp["wiki_resp"]:
                    return wiki_api_resp
        return wiki_api_resp


def answer(whole_question: str) -> dict:
    """
    The main controller function : calls parser and api and send back the final response to the ajax view.

    Step by step:
    1) Parses the user question.
    2) If parsing got one or several key words, they are used together to request the API.
        2.1) If API both got a positive response, they are returned.
        2.2) If only map API got a positive response, key words are used separately for requesting Wikipedia API.
            2.2.1) If Wikipedia API still got a negative response, only the API response is returned.
            2.2.2) If Wikipedia API got a positive response, it is returned with the map API response.
        2.3) If map API got a negative response, key words are used separately for requesting it.
            2.3.1) If both API got a positive response, they are returned.
            2.3.2) If only map API got a positive response, a dict with key "error" is returned because results
            using key words separately are relevant only if both API got positive response.
            2.3.3) If both API got a negative response, a dict with key "error" with "Failing map API requesting
            even last chance try..." value.

    """

    parsed_question_dict = parse_question(whole_question)

    if parsed_question_dict is not None:
        final_answer = try_original_key_words(parsed_question_dict["formated_original_key_words"])
        if final_answer["map_resp"] is False:
            final_answer_last_chance = try_singled_key_words(parsed_question_dict["singled_key_words"])
            if final_answer_last_chance["map_resp"]:
                if final_answer_last_chance["wiki_resp"]:
                    return final_answer_last_chance
                else:
                    return {"error": "Failing wiki API requesting even last chance try... "
                            "map API result is probably not pertinent..."}
            else:
                return {"error": "Failing map API requesting even last chance try..."}
        elif "wiki_resp" not in final_answer.keys():
            wiki_last_chance = try_singled_key_words(parsed_question_dict["singled_key_words"], map_ok=True)
            return {
                    **final_answer, **wiki_last_chance
                }
        elif final_answer["wiki_resp"] is False:
            wiki_last_chance = try_singled_key_words(parsed_question_dict["singled_key_words"], map_ok=True)
            if wiki_last_chance["wiki_resp"]:
                final_answer.pop("wiki_resp")
                return {
                    **final_answer, **wiki_last_chance
                }
            else:
                return final_answer

        else:
            return final_answer
    else:
        return {"error": "Parser failed..."}
