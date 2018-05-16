""" This fetches kills for some number of char ids and sees if
    any are multiboxed (assuming it's all one person's chars);
    then we try to print it in a berable manner.

    NOTE: This is part is a proof-of-concept and should be
          modularized before automatic use.
"""
import requests
from common.character import Character
from common import esi
zkill_headers = {'User-Agent': 'surculus12@gmail.com'}

def check_multibox(char_ids):
    characters = [Character(id_) for id_ in char_ids]
    char_kills = {c.id:c.get_killmail_ids() for c in characters}

    # This goes through all sets of kills. It takes a set, pops a value and
    # checks whether it's in any other set; if it finds it in another set,
    # it removes it from that set and adds the char ids it to the result dict.
    # TODO: Make this not spaghetti
    mboxed_kills = dict()
    for char_id in char_ids:
        kills = char_kills.pop(char_id)
        for kill in kills:
            if kill in mboxed_kills:
                mboxed_kills[kill].append(char_id)
            for other_char_id, other_kills in char_kills.items():
                if kill in other_kills:
                    char_kills[other_char_id].remove(kill)
                    if kill in mboxed_kills:
                        mboxed_kills[kill].append(other_char_id)
                    else:
                        mboxed_kills[kill] = [char_id, other_char_id]
    return mboxed_kills


def get_kill_info(kill, chars):
    ret = {'chars': dict()}
    kill = requests.get(''.join(['https://zkillboard.com/api/kills/no-items/killID/', str(kill), '/']), headers=zkill_headers).json()[0]
    kill_chars = [c for c in kill['attackers'] if 'character_id' in c and c['character_id'] in chars]
    ret['kill_type'] = esi.get_type_name(kill['victim']['ship_type_id'])
    for kc in kill_chars:
        try:
            ship = esi.get_type_name(kc['ship_type_id'])
        except KeyError:
            ship = "UNKNOWN"
        ret['chars'][kc['character_id']] = {'ship': ship}

    return ret

if __name__ == '__main__':
    chars_input = [95424317, 92019423, 96021112]
    mbox_res = check_multibox(chars_input)
    print(len(mbox_res), 'multiboxing kills')
    for i, chars in mbox_res.items():
        kill_infos = get_kill_info(i, chars)
        print('https://zkillboard.com/kill/'+str(i)+'/', '(', kill_infos['kill_type'], ')',
              str(len(chars)) + ' chars on kill:')
        for char, info in kill_infos['chars'].items():
            print('\t', str(char), 'in', info['ship'])
