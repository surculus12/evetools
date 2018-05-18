import kb
import itertools

class Character(object):
    _base_kill_uri = 'https://zkillboard.com/api/kills/zkbOnly/'

    __slots__ = ['id']

    def __init__(self, id_):
        self.id = id_

    def get_killmail_ids(self):
        kills = set()
        for page in itertools.count(1):
            result = kb.get_kills(zkbOnly=True, characterID=str(self.id),
                                  page=str(page))
            if not result:  # zkill doesn't have a `next` or
                break       # other form of proper pagination.
            kills.update({r['killmail_id'] for r in result})
        return kills
