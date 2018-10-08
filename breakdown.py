import json
import pickle
import numpy as np
from pprint import pprint
import os
import cfg

import model

PACK_DIR = os.path.join(cfg.SONGS_DIR
        , "A NCPR's ITG Katsudou!"
        )

def get_breakdown(chart_data):
    breakdown = []
    measures = chart_data['measures']
    cur_streaming = model.is_stream(measures[0])
    cur_segment = 0
    for measure in measures:
        if model.is_stream(measure):
            if cur_streaming:
                cur_segment += 1
            else:
                breakdown.append('(%d)' % cur_segment)
                cur_segment = 1
                cur_streaming = True
        else:
            if cur_streaming:
                breakdown.append(str(cur_segment))
                cur_segment = 1
                cur_streaming = False
            else:
                cur_segment += 1
    return ' '.join(breakdown)



for root, dirs, files in sorted(os.walk(PACK_DIR)):
    for fn in files:
        if fn.endswith('.sm'):
            song_fn = os.path.join(root, fn)
            print(song_fn)

            X = []

            with open(song_fn, 'r') as f:
                lines = f.readlines()

            song = model.process(lines)
            difficulties = sorted(song['charts'])
            for difficulty in difficulties:
                chart_data = song['charts'][difficulty]
                breakdown = get_breakdown(chart_data)
                print(difficulty)
                print(breakdown)
            print('*'*80)
