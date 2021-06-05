import app.grandpy_bot as gpy


def test_parse_question_return_none_if_not_ok(monkeypatch):
    def mock_extract_interesting_tokens(parser):
        mock_extract_interesting_tokens.called = True
        parser.interesting_tokens = []

    monkeypatch.setattr('app.parser.Parser.extract_interesting_tokens', mock_extract_interesting_tokens)

    mock_extract_interesting_tokens.called = False
    gpy.parse_question("qu") is None

    assert mock_extract_interesting_tokens.called


def test_parse_question_return_dict_if_ok(monkeypatch):
    def mock_extract_interesting_tokens(parser):
        mock_extract_interesting_tokens.called = True
        parser.interesting_tokens = ["tokens"]

    def mock_capitalize(text):
        mock_capitalize.called = True
        return "capit"

    def mock_decapitalize(text):
        mock_decapitalize.called = True
        return "decapit"

    def mock_word_reverse_case_first_char(word):
        mock_word_reverse_case_first_char.called = True
        return "reversed_case"

    monkeypatch.setattr('app.parser.Parser.extract_interesting_tokens', mock_extract_interesting_tokens)
    monkeypatch.setattr('app.parser.Parser.capitalize_all_words', mock_capitalize)
    monkeypatch.setattr('app.parser.Parser.decapitalize_all_words', mock_decapitalize)
    monkeypatch.setattr('app.parser.Parser.word_reverse_case_first_char', mock_word_reverse_case_first_char)

    mock_extract_interesting_tokens.called = False
    mock_capitalize.called = False
    mock_decapitalize.called = False
    mock_word_reverse_case_first_char.called = False
    parse_question_result = {
        'formated': {
            'parsed_key_words': "tokens",
            'capitalized': "capit",
            'decapitalized': "decapit",
        },
        'singled': (("tokens", "Tokens"),)
    }

    gpy.parse_question("qu") == parse_question_result
    assert mock_extract_interesting_tokens.called
    assert mock_decapitalize.called
    assert mock_capitalize.called
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


def test_try_formated_key_words(monkeypatch):
    formated_key_words = {
        "parsed_key_words": "pkw",
        "capitalized": "capit",
        "decapitalized": "decapit",
    }

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

    assert gpy.try_formated_key_words(formated_key_words) == {"map_resp": True, "wiki_resp": True}
    assert mock_maps_position.called
    assert mock_wiki_infos.called


def test_try_singled_key_words_when_both_api_succeeds(monkeypatch):
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


def test_try_singled_key_words_when_wiki_api_fails(monkeypatch):
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


def test_answer_if_parser_succeeds_and_api_requesting_succeeds_with_formated_key_words(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return {"formated": "fkw"}

    def mock_try_formated_key_words(parsed_question_dict):
        mock_try_formated_key_words.called = True
        return {"map_resp": True}

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)
    monkeypatch.setattr('app.grandpy_bot.try_formated_key_words', mock_try_formated_key_words)

    mock_parse_question.called = False
    mock_try_formated_key_words.called = False

    assert gpy.answer("whole_question") == {"map_resp": True}
    assert mock_parse_question.called
    assert mock_try_formated_key_words.called


def test_answer_if_parser_fails(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return None

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)

    mock_parse_question.called = False

    assert gpy.answer("whole_question") == {"error": "Parser failed..."}
    assert mock_parse_question.called


def test_answer_if_parser_succeeds_and_api_requesting_succeeds_with_singled_key_words(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return {'formated': "fkw", 'singled': "skw"}

    def mock_try_formated_key_words(parsed_question_dict):
        mock_try_formated_key_words.called = True
        return {"map_resp": False}

    def mock_try_singled_key_words(parsed_question_dict):
        mock_try_singled_key_words.called = True
        return {"map_resp": True, "wiki_resp": True}

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)
    monkeypatch.setattr('app.grandpy_bot.try_formated_key_words', mock_try_formated_key_words)
    monkeypatch.setattr('app.grandpy_bot.try_singled_key_words', mock_try_singled_key_words)

    mock_parse_question.called = False
    mock_try_formated_key_words.called = False
    mock_try_singled_key_words.called = False

    assert gpy.answer("whole_question") == {"map_resp": True, "wiki_resp": True}
    assert mock_parse_question.called
    assert mock_try_formated_key_words.called
    assert mock_try_singled_key_words.called


def test_answer_if_parser_succeeds_but_api_requesting_fails_even_last_chance_try(monkeypatch):
    def mock_parse_question(quest):
        mock_parse_question.called = True
        return {'formated': "fkw", 'singled': "skw"}

    def mock_try_formated_key_words(parsed_question_dict):
        mock_try_formated_key_words.called = True
        return {"map_resp": False}

    def mock_try_singled_key_words(parsed_question_dict):
        mock_try_singled_key_words.called = True
        return {"map_resp": True, "wiki_resp": False}

    monkeypatch.setattr('app.grandpy_bot.parse_question', mock_parse_question)
    monkeypatch.setattr('app.grandpy_bot.try_formated_key_words', mock_try_formated_key_words)
    monkeypatch.setattr('app.grandpy_bot.try_singled_key_words', mock_try_singled_key_words)

    mock_parse_question.called = False
    mock_try_formated_key_words.called = False
    mock_try_singled_key_words.called = False

    assert gpy.answer("whole_question") == {"error": "Failing wiki API requesting..."}
    assert mock_parse_question.called
    assert mock_try_formated_key_words.called
    assert mock_try_singled_key_words.called
