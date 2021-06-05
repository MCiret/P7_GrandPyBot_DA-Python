import requests
import config as cfg


def api_request_and_get_dict_resp(url, **params):
    request_resp = requests.get(url, params)
    return request_resp.json()


def resp_dict_to_location(here_api_resp_dict):
    if len(here_api_resp_dict['items']) > 0:
        return {
            "map_resp": True,
            "address": here_api_resp_dict['items'][0]['address']['label'],
            "lat": here_api_resp_dict['items'][0]['position']['lat'],
            "long": here_api_resp_dict['items'][0]['position']['lng'],
            "apikey": cfg.HERE_API_KEY,
        }
    else:
        return {
            "map_resp": False
        }


def resp_dict_to_wiki_infos(wiki_api_resp_dict):
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
