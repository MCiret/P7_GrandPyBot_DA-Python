import requests

class ApiRequests:

    @staticmethod
    def run_get_request(url, **params):
        return requests.get(url, params)

    @staticmethod
    def json_resp_to_dict(json_resp):
        return json_resp.json()

    @staticmethod
    def resp_dict_to_position(resp_dict):
        return {
            "lat": resp_dict['items'][0]['position']['lat'],
            "long": resp_dict['items'][0]['position']['lng']
        }
