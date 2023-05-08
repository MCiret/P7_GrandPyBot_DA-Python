import os

HERE_API_URL = 'https://geocode.search.hereapi.com/v1/geocode'
HERE_API_KEY = os.environ.get('HERE_API_KEY')

WIKI_API_URL = 'https://fr.wikipedia.org/w/api.php'
WIKI_API_PARAMS = {
    "action": "query",
    "prop": "extracts|info",
    "exchars": "500",
    "inprop": "url",
    "explaintext": "",
    "format": "json",
}
