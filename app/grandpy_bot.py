import config as cfg
from app.request_api import ApiRequests

class GrandpyBot:

    @staticmethod
    def question_parser(question):
        # return location_str (i.e question parsed)
        return question

    @staticmethod
    def maps_position(location_str):
        return ApiRequests.resp_dict_to_position(
                           ApiRequests.json_resp_to_dict(
                                       ApiRequests.run_get_request(
                                                   cfg.HERE_API_URL,apikey=cfg.HERE_API_KEY, q=location_str)))

    @staticmethod
    def answer(whole_question):
        return GrandpyBot.maps_position(GrandpyBot.question_parser(whole_question))
