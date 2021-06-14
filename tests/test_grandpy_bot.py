import app.grandpy_bot as gpy


def test_parse_question_return_none_if_failure(monkeypatch):
    def mock_extract_interesting_tokens(parser):
        mock_extract_interesting_tokens.called = True
        parser.interesting_tokens = []

    monkeypatch.setattr('app.parser.Parser.extract_interesting_tokens', mock_extract_interesting_tokens)

    mock_extract_interesting_tokens.called = False
    gpy.parse_question("qu") is None

    assert mock_extract_interesting_tokens.called


def test_parse_question_return_dict_if_success(monkeypatch):
    def mock_extract_interesting_tokens(parser):
        mock_extract_interesting_tokens.called = True
        parser.interesting_tokens = ["some", "tokens"]

    def mock_word_reverse_case_first_char(word):
        mock_word_reverse_case_first_char.called = True
        return "reversed_case"

    monkeypatch.setattr('app.parser.Parser.extract_interesting_tokens', mock_extract_interesting_tokens)
    monkeypatch.setattr('app.parser.Parser.word_reverse_case_first_char', mock_word_reverse_case_first_char)

    mock_extract_interesting_tokens.called = False
    mock_word_reverse_case_first_char.called = False
    parse_question_result = {
        'formated_original_key_words': "Some Tokens",
        'singled_key_words': (("some", "Some"), ("tokens", "Tokens"),)
    }

    gpy.parse_question("qu") == parse_question_result
    assert mock_extract_interesting_tokens.called
    assert mock_word_reverse_case_first_char.called


def test_maps_position_is_using_passed_argument(monkeypatch):
    def mock_api_request_and_get_dict_resp(url, apikey, q):
        mock_api_request_and_get_dict_resp.called = True
        mock_api_request_and_get_dict_resp.params = {
            "url": url,
            "apikey": apikey,
            "q": q,
        }
        return "here_api_request_resp_dict"

    def mock_resp_dict_to_location(here_api_resp_dict):
        mock_resp_dict_to_location.called = True
        mock_resp_dict_to_location.params = {
            "resp_dict": here_api_resp_dict
        }
        return "location"

    monkeypatch.setattr('app.api_requests.api_request_and_get_dict_resp', mock_api_request_and_get_dict_resp)
    monkeypatch.setattr('app.api_requests.resp_dict_to_location', mock_resp_dict_to_location)

    mock_api_request_and_get_dict_resp.called = False
    mock_resp_dict_to_location.called = False

    assert gpy.maps_position("where") == "location"
    assert mock_api_request_and_get_dict_resp.called
    assert mock_resp_dict_to_location.called
    assert mock_api_request_and_get_dict_resp.params["q"] == "where"
    assert mock_resp_dict_to_location.params["resp_dict"] == "here_api_request_resp_dict"


def test_wiki_infos_is_using_passed_argument(monkeypatch):
    def mock_api_request_and_get_dict_resp(url, action, prop, exchars, inprop, explaintext, format, titles):
        mock_api_request_and_get_dict_resp.called = True
        mock_api_request_and_get_dict_resp.params = {
            "url": url,
            "wiki_params": {action, prop, exchars, inprop, explaintext, format},
            "titles": titles,
        }
        return "wiki_api_request_resp_dict"

    def mock_resp_dict_to_wiki_infos(wiki_api_resp_dict):
        mock_resp_dict_to_wiki_infos.called = True
        mock_resp_dict_to_wiki_infos.params = {
            "resp_dict": wiki_api_resp_dict
        }
        return "wiki_infos"

    monkeypatch.setattr('app.api_requests.api_request_and_get_dict_resp', mock_api_request_and_get_dict_resp)
    monkeypatch.setattr('app.api_requests.resp_dict_to_wiki_infos', mock_resp_dict_to_wiki_infos)

    mock_api_request_and_get_dict_resp.called = False
    mock_resp_dict_to_wiki_infos.called = False

    assert gpy.wiki_infos("what") == "wiki_infos"
    assert mock_api_request_and_get_dict_resp.called
    assert mock_resp_dict_to_wiki_infos.called
    assert mock_api_request_and_get_dict_resp.params["titles"] == "what"
    assert mock_resp_dict_to_wiki_infos.params["resp_dict"] == "wiki_api_request_resp_dict"


def test_try_original_key_words_when_both_api_succeed_but_using_map_api_key_words_for_wiki_api(monkeypatch):
    def mock_maps_position(key_word):
        mock_maps_position.called = True
        return {
            "key_words": "wiki key words",
            "map_resp": True}

    def mock_wiki_infos(key_word):
        mock_wiki_infos.called = True
        mock_wiki_infos.params = {"kw": key_word}
        return {"wiki_resp": True}

    monkeypatch.setattr('app.grandpy_bot.maps_position', mock_maps_position)
    monkeypatch.setattr('app.grandpy_bot.wiki_infos', mock_wiki_infos)

    mock_maps_position.called = False
    mock_wiki_infos.called = False

    assert gpy.try_original_key_words("original key words") == {
        "key_words": "wiki key words",
        "map_resp": True,
        "wiki_resp": True
    }
    assert mock_maps_position.called
    assert mock_wiki_infos.called
    assert mock_wiki_infos.params["kw"] == "wiki_key_words"


def test_try_original_key_words_when_both_api_succeed_using_original_key_words(monkeypatch):
    def mock_maps_position(key_word):
        mock_maps_position.called = True
        return {
            "key_words": None,
            "map_resp": True}

    def mock_wiki_infos(key_word):
        mock_wiki_infos.called = True
        mock_wiki_infos.params = {"kw": key_word}
        return {"wiki_resp": True}

    monkeypatch.setattr('app.grandpy_bot.maps_position', mock_maps_position)
    monkeypatch.setattr('app.grandpy_bot.wiki_infos', mock_wiki_infos)

    mock_maps_position.called = False
    mock_wiki_infos.called = False

    assert gpy.try_original_key_words("original key words") == {
        "key_words": None,
        "map_resp": True,
        "wiki_resp": True
    }
    assert mock_maps_position.called
    assert mock_wiki_infos.called
    assert mock_wiki_infos.params["kw"]


def test_try_original_key_words_when_map_api_fails(monkeypatch):
    def mock_maps_position(key_word):
        mock_maps_position.called = True
        return {
            "map_resp": False}

    monkeypatch.setattr('app.grandpy_bot.maps_position', mock_maps_position)

    mock_maps_position.called = False

    assert gpy.try_original_key_words("original key words") == {"map_resp": False}
    assert mock_maps_position.called


def test_try_original_key_words_when_wiki_api_fails(monkeypatch):
    def mock_maps_position(key_word):
        mock_maps_position.called = True
        return {
            "key_words": "wiki key words",
            "map_resp": True}

    def mock_wiki_infos(key_word):
        mock_wiki_infos.called = True
        return {"wiki_resp": False}

    monkeypatch.setattr('app.grandpy_bot.maps_position', mock_maps_position)
    monkeypatch.setattr('app.grandpy_bot.wiki_infos', mock_wiki_infos)

    mock_maps_position.called = False
    mock_wiki_infos.called = False

    assert gpy.try_original_key_words("original key words") == {
        "key_words": 'wiki key words',
        "map_resp": True,
        "wiki_resp": False
    }
    assert mock_maps_position.called
    assert mock_wiki_infos.called


def test_try_singled_key_words_for_all_api_which_succeed(monkeypatch):
    singled_key_words = (("kw1", "KW1"), ("kw2", "KW2"))

    def mock_maps_position(key_word):
        mock_maps_position.called = True
        return {"map_resp": True}

    def mock_wiki_infos(key_word):
        mock_wiki_infos.called = True
        return {"wiki_resp": True}

    monkeypatch.setattr('app.grandpy_bot.maps_position', mock_maps_position)
    monkeypatch.setattr('app.grandpy_bot.wiki_infos', mock_wiki_infos)

    mock_maps_position.called = False
    mock_wiki_infos.called = False

    assert gpy.try_singled_key_words(singled_key_words) == {"map_resp": True, "wiki_resp": True}
    assert mock_maps_position.called
    assert mock_wiki_infos.called


def test_try_singled_key_words_for_ball_api_but_map_api_fails(monkeypatch):
    singled_key_words = (("kw1", "KW1"), ("kw2", "KW2"))

    def mock_maps_position(key_word):
        mock_maps_position.called = True
        return {"map_resp": False}

    monkeypatch.setattr('app.grandpy_bot.maps_position', mock_maps_position)

    mock_maps_position.called = False

    assert gpy.try_singled_key_words(singled_key_words) == {"map_resp": False}
    assert mock_maps_position.called


def test_try_singled_key_words_for_all_api_but_wiki_api_fails(monkeypatch):
    singled_key_words = (("kw1", "KW1"), ("kw2", "KW2"))

    def mock_maps_position(key_word):
        mock_maps_position.called = True
        return {"map_resp": True}

    def mock_wiki_infos(key_word):
        mock_wiki_infos.called = True
        return {"wiki_resp": False}

    monkeypatch.setattr('app.grandpy_bot.maps_position', mock_maps_position)
    monkeypatch.setattr('app.grandpy_bot.wiki_infos', mock_wiki_infos)

    mock_maps_position.called = False
    mock_wiki_infos.called = False

    assert gpy.try_singled_key_words(singled_key_words) == {"map_resp": True}
    assert mock_maps_position.called
    assert mock_wiki_infos.called


def test_try_singled_key_words_only_for_wiki_api_which_fails(monkeypatch):
    singled_key_words = (("kw1", "KW1"), ("kw2", "KW2"))

    def mock_wiki_infos(key_word):
        mock_wiki_infos.called = True
        return {"wiki_resp": False}

    monkeypatch.setattr('app.grandpy_bot.wiki_infos', mock_wiki_infos)

    mock_wiki_infos.called = False

    assert gpy.try_singled_key_words(singled_key_words, map_ok=True) == {"wiki_resp": False}
    assert mock_wiki_infos.called


def test_try_singled_key_words_only_for_wiki_api_which_succeeds(monkeypatch):
    singled_key_words = (("kw1", "KW1"), ("kw2", "KW2"))

    def mock_wiki_infos(key_word):
        mock_wiki_infos.called = True
        return {"wiki_resp": True}

    monkeypatch.setattr('app.grandpy_bot.wiki_infos', mock_wiki_infos)

    mock_wiki_infos.called = False

    assert gpy.try_singled_key_words(singled_key_words, map_ok=True) == {"wiki_resp": True}
    assert mock_wiki_infos.called


def test_answer_if_parser_succeeds_and_both_api_succeeds_with_original_key_words(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return {"formated_original_key_words": "fkw"}

    def mock_try_original_key_words(parsed_question_str):
        mock_try_original_key_words.called = True
        return {"map_resp": True, "wiki_resp": True}

    def mock_try_singled_key_words(key_words_tuple):
        mock_try_singled_key_words.called = True
        return {"map_resp": True, "wiki_resp": True}

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)
    monkeypatch.setattr('app.grandpy_bot.try_original_key_words', mock_try_original_key_words)
    monkeypatch.setattr('app.grandpy_bot.try_singled_key_words', mock_try_singled_key_words)

    mock_parse_question.called = False
    mock_try_original_key_words.called = False
    mock_try_singled_key_words.called = False

    assert gpy.answer("whole_question") == {"map_resp": True, "wiki_resp": True}
    assert mock_parse_question.called
    assert mock_try_original_key_words.called
    assert not mock_try_singled_key_words.called


def test_answer_if_parser_fails(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return None

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)

    mock_parse_question.called = False

    assert gpy.answer("whole_question") == {"error": "Parser failed..."}
    assert mock_parse_question.called


def test_answer_if_parser_succeeds_and_both_api_succeed_with_singled_key_words(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return {'formated_original_key_words': "fkw", 'singled_key_words': "skw"}

    def mock_try_original_key_words(parsed_question_str):
        mock_try_original_key_words.called = True
        return {"map_resp": False}

    def mock_try_singled_key_words(key_words_tuple):
        mock_try_singled_key_words.called = True
        return {"map_resp": True, "wiki_resp": True}

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)
    monkeypatch.setattr('app.grandpy_bot.try_original_key_words', mock_try_original_key_words)
    monkeypatch.setattr('app.grandpy_bot.try_singled_key_words', mock_try_singled_key_words)

    mock_parse_question.called = False
    mock_try_original_key_words.called = False
    mock_try_singled_key_words.called = False

    assert gpy.answer("whole_question") == {"map_resp": True, "wiki_resp": True}
    assert mock_parse_question.called
    assert mock_try_original_key_words.called
    assert mock_try_singled_key_words.called


def test_answer_if_parser_succeeds_but_both_api_fails_with_singled_key_words(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return {'formated_original_key_words': "fkw", 'singled_key_words': "skw"}

    def mock_try_original_key_words(parsed_question_str):
        mock_try_original_key_words.called = True
        return {"map_resp": False}

    def mock_try_singled_key_words(key_words_tuple):
        mock_try_singled_key_words.called = True
        return {"map_resp": False, "wiki_resp": False}

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)
    monkeypatch.setattr('app.grandpy_bot.try_original_key_words', mock_try_original_key_words)
    monkeypatch.setattr('app.grandpy_bot.try_singled_key_words', mock_try_singled_key_words)

    mock_parse_question.called = False
    mock_try_original_key_words.called = False
    mock_try_singled_key_words.called = False

    assert gpy.answer("whole_question") == {"error": "Failing map API requesting even last chance try..."}
    assert mock_parse_question.called
    assert mock_try_original_key_words.called
    assert mock_try_singled_key_words.called


def test_answer_if_parser_succeeds_but_only_map_api_succeeds_with_singled_key_words(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return {'formated_original_key_words': "fkw", 'singled_key_words': "skw"}

    def mock_try_original_key_words(parsed_question_str):
        mock_try_original_key_words.called = True
        return {"map_resp": False}

    def mock_try_singled_key_words(key_words_tuple):
        mock_try_singled_key_words.called = True
        return {"map_resp": True, "wiki_resp": False}

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)
    monkeypatch.setattr('app.grandpy_bot.try_original_key_words', mock_try_original_key_words)
    monkeypatch.setattr('app.grandpy_bot.try_singled_key_words', mock_try_singled_key_words)

    mock_parse_question.called = False
    mock_try_original_key_words.called = False
    mock_try_singled_key_words.called = False

    assert gpy.answer("whole_question") == {"error": "Failing wiki API requesting even last chance try... "
                                            "map API result is probably not pertinent..."}
    assert mock_parse_question.called
    assert mock_try_original_key_words.called
    assert mock_try_singled_key_words.called


def test_answer_if_parser_succeeds_and_only_wiki_api_with_singled_key_words_which_fails(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return {'formated_original_key_words': "fkw", 'singled_key_words': "skw"}

    def mock_try_original_key_words(parsed_question_str):
        mock_try_original_key_words.called = True
        return {"map_resp": True, "wiki_resp": False}

    def mock_try_singled_key_words(key_words_tuple, map_ok=True):
        mock_try_singled_key_words.called = True
        return {"wiki_resp": False}

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)
    monkeypatch.setattr('app.grandpy_bot.try_original_key_words', mock_try_original_key_words)
    monkeypatch.setattr('app.grandpy_bot.try_singled_key_words', mock_try_singled_key_words)

    mock_parse_question.called = False
    mock_try_original_key_words.called = False
    mock_try_singled_key_words.called = False

    assert gpy.answer("whole_question") == {"map_resp": True, "wiki_resp": False}
    assert mock_parse_question.called
    assert mock_try_original_key_words.called
    assert mock_try_singled_key_words.called


def test_answer_if_parser_succeeds_and_only_wiki_api_with_singled_key_words_which_succeeds(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return {'formated_original_key_words': "fkw", 'singled_key_words': "skw"}

    def mock_try_original_key_words(parsed_question_str):
        mock_try_original_key_words.called = True
        return {"map_resp": True, "wiki_resp": False}

    def mock_try_singled_key_words(key_words_tuple, map_ok=True):
        mock_try_singled_key_words.called = True
        return {"wiki_resp": True}

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)
    monkeypatch.setattr('app.grandpy_bot.try_original_key_words', mock_try_original_key_words)
    monkeypatch.setattr('app.grandpy_bot.try_singled_key_words', mock_try_singled_key_words)

    mock_parse_question.called = False
    mock_try_original_key_words.called = False
    mock_try_singled_key_words.called = False

    assert gpy.answer("whole_question") == {"map_resp": True, "wiki_resp": True}
    assert mock_parse_question.called
    assert mock_try_original_key_words.called
    assert mock_try_singled_key_words.called
