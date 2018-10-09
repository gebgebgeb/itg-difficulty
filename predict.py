import json
import pickle
import numpy as np
from pprint import pprint
import os
import cfg

from features import vecify
from augment import process

PACK_DIR = os.path.join(cfg.SONGS_DIR
        , "A NCPR's ITG Katsudou!"
        )

with open('res/automl.pickle','rb') as f:
    automl = pickle.load(f)

with open('res/best_indices.json', 'r') as f:
    best_indices = json.load(f)

for root, dirs, files in sorted(os.walk(PACK_DIR)):
    for fn in files:
        if fn.endswith('.sm'):
            song_fn = os.path.join(root, fn)
            print(song_fn)

            X = []

            song = process(song_fn)
            difficulties = sorted(song['charts'])
            for difficulty in difficulties:
                X.append(vecify(song, difficulty, feature_indices=best_indices))
            if not X:
                continue

            X = np.array(X)
            pprint(list(zip(
                difficulties # Easy, Medium, Hard, Challenge, Edit
                , automl.predict(X) # Predicted rating
                , [song['charts'][d]['rating'] for d in difficulties] # Old rating
                )))
            print('*'*80)
