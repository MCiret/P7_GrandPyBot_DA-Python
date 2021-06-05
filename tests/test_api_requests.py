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
    mock_api_here_filled_resp_dict = {
        'items': [{
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
    assert api.resp_dict_to_location(mock_api_here_filled_resp_dict) == {
        'map_resp': True,
        'address': "add",
        'lat': "la",
        'long': "lo",
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
