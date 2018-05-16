# TODO: Local cache
def get_type_name(type_id):
    return requests.get(''.join(['https://esi.evetech.net/latest/universe/types/',
                                 str(type_id), '/'])).json()['name']
