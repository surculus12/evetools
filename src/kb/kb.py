import requests

HEADERS =  {'User-Agent': 'surculus12@gmail.com'}
VALID_KWARGS = ['characterID', 'zkbOnly', 'page']
BASE_URL = 'https://zkillboard.com/api/'

def strip_invalid_args(kwargs):
    """ Mostly for the convenience of catching typos...
    """
    for key in kwargs.keys():
        assert key in VALID_KWARGS, "Invalid arg: " + key
    return kwargs


def get_kills(**kwargs):
    url = BASE_URL + 'kills/'
    kwargs = strip_invalid_args(kwargs)
    # We don't care much about concat optimization here so v0v
    for key, value in kwargs.items():
        if value is not True:
            url = ''.join([url, key, '/', value, '/'])
        else:
            url = ''.join([url, key, '/'])
    return requests.get(url, headers=HEADERS).json()

