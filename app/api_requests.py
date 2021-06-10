import requests
import config as cfg


def api_request_and_get_dict_resp(url, **params) -> dict:
    request_resp = requests.get(url, params)
    return request_resp.json()


def resp_dict_to_location(here_api_resp_dict: dict) -> dict:
    """
    Keeps interesting data from here.com API response.
    Ideally also key words then used to request Wikipedia API
    """

    if len(here_api_resp_dict['items']) > 0:
        res_type = here_api_resp_dict['items'][0]["resultType"]
        if (res_type + "Type") in here_api_resp_dict['items'][0].keys():
            return {
                "map_resp": True,
                "address": here_api_resp_dict['items'][0]['address']['label'],
                "lat": here_api_resp_dict['items'][0]['position']['lat'],
                "long": here_api_resp_dict['items'][0]['position']['lng'],
                "key_words": here_api_resp_dict['items'][0]['address']
                [here_api_resp_dict['items'][0][res_type + "Type"]],
                "apikey": cfg.HERE_API_KEY,
            }
        elif res_type in here_api_resp_dict['items'][0]['address'].keys():
            return {
                "map_resp": True,
                "address": here_api_resp_dict['items'][0]['address']['label'],
                "lat": here_api_resp_dict['items'][0]['position']['lat'],
                "long": here_api_resp_dict['items'][0]['position']['lng'],
                "key_words": here_api_resp_dict['items'][0]['address'][res_type],
                "apikey": cfg.HERE_API_KEY,
            }
        else:
            return {
                "map_resp": True,
                "address": here_api_resp_dict['items'][0]['address']['label'],
                "lat": here_api_resp_dict['items'][0]['position']['lat'],
                "long": here_api_resp_dict['items'][0]['position']['lng'],
                "key_words": None,
                "apikey": cfg.HERE_API_KEY,
            }
    else:
        return {
            "map_resp": False
        }


def resp_dict_to_wiki_infos(wiki_api_resp_dict: dict) -> dict:
    """ Keeps interesting data from Wikipedia API response. """

    if "-1" in wiki_api_resp_dict['query']['pages'].keys():
        return {
            "wiki_resp": False
        }
    else:
        for key in wiki_api_resp_dict['query']['pages']:
            id = key
        return {
            "extract": wiki_api_resp_dict['query']['pages'][id]['extract'],
            "url": wiki_api_resp_dict['query']['pages'][id]['fullurl'],
            "wiki_resp": True
        }
