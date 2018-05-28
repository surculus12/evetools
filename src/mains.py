from common import esi
import kb
from data.sl1de_chars import SL1DE_CHARS_IDS
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np


def get_month_stats(chars=SL1DE_CHARS_IDS):
    for i in range(len(chars)):
        if isinstance(chars[i], str):
            try:
                chars[i] = esi.get_char_id_from_name(chars[i])
            except KeyError:
                print(chars[i], 'not found in esi')

    stats = dict()
    for char in chars:
        stats[char] = kb.get_stats(characterID=str(char))

    months = pd.date_range(datetime.date.today()-datetime.timedelta(365),
                           datetime.date.today(), freq='1M')
    statistics = []
    for char, stat in stats.items():
        char_stat_items = []
        for m in months.union([months[-1]+1]):
            year = str(m.year)
            month = '%02d' % m.month
            try:
                stat_item = stat['months'][year+month]['shipsDestroyed']
                if stat_item > 500:
                    print(char, 'had', stat_item, 'kills in',year+month)
            except KeyError:
                stat_item = np.NaN
            char_stat_items.append(stat_item)
        statistics.append(char_stat_items)
    print(statistics)
    df = pd.DataFrame(statistics, columns=[d.strftime('%y-%b') for d in months.union([months[-1]+1])])
    df = df.dropna()
    df.plot.box()
    plt.show()
