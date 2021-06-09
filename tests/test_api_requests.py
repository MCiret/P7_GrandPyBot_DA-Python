import app.api_requests as api
import requests
import config as cfg


def test_api_request_and_get_dict_resp():

    class MockResponse:
        def json(self):
            return 1

    def mock_get(url, params):
        mock_get.called = True
        mock_get.params = {
            "url": url,
            "params": params
        }
        return MockResponse()

    bkup_get_request = requests.get
    requests.get = mock_get

    assert api.api_request_and_get_dict_resp('https://url/api', **{"param_a": 'a', "param_b": 'b'}) == 1
    assert mock_get.called
    assert mock_get.params['url'] == 'https://url/api'
    assert mock_get.params['params'] == {"param_a": 'a', "param_b": 'b'}

    requests.get = bkup_get_request


def test_parsing_of_resp_dict_to_location():
    mock_api_here_empty_resp_dict = {
        'items': []
    }
    mock_api_here_filled_resp_dict_form1 = {
        'items': [{
            'resultType': "xxxxx",
            'xxxxxType': "yyy",
            'address': {
                'label': "add",
                'yyy': "kw1"
            },
            'position': {
                    'lat': "la",
                    'lng': "lo",
            }
        }]
    }
    mock_api_here_filled_resp_dict_form2 = {
        'items': [{
            'resultType': "xxxxx",
            'address': {
                'label': "add",
                'xxxxx': "kw2"
            },
            'position': {
                    'lat': "la",
                    'lng': "lo",
            }
        }]
    }
    mock_api_here_filled_resp_dict_form3 = {
        'items': [{
            'resultType': "xxxxx",
            'address': {
                'label': "add",
            },
            'position': {
                    'lat': "la",
                    'lng': "lo",
            }
        }]
    }
    assert api.resp_dict_to_location(mock_api_here_empty_resp_dict) == {"map_resp": False}
    assert api.resp_dict_to_location(mock_api_here_filled_resp_dict_form1) == {
        'map_resp': True,
        'address': "add",
        'lat': "la",
        'long': "lo",
        'key_words': "kw1",
        'apikey': cfg.HERE_API_KEY
    }
    assert api.resp_dict_to_location(mock_api_here_filled_resp_dict_form2) == {
        'map_resp': True,
        'address': "add",
        'lat': "la",
        'long': "lo",
        'key_words': "kw2",
        'apikey': cfg.HERE_API_KEY
    }
    assert api.resp_dict_to_location(mock_api_here_filled_resp_dict_form3) == {
        'map_resp': True,
        'address': "add",
        'lat': "la",
        'long': "lo",
        'key_words': None,
        'apikey': cfg.HERE_API_KEY
    }


def test_parsing_of_resp_dict_to_wiki():
    mock_api_wiki_empty_resp_dict = {
        'query': {
            'pages': {
                    "-1": {}
            }
        }
    }
    mock_api_wiki_filled_resp_dict = {
        "query": {
            "pages": {
                "34407": {
                    'extract': "blablabla",
                    'fullurl': "www.wikipedia/blablabla.fr",
                }
            }
        }
    }

    assert api.resp_dict_to_wiki_infos(mock_api_wiki_empty_resp_dict) == {"wiki_resp": False}
    assert api.resp_dict_to_wiki_infos(mock_api_wiki_filled_resp_dict) == {
        'extract': "blablabla",
        'url': "www.wikipedia/blablabla.fr",
        'wiki_resp': True
    }
