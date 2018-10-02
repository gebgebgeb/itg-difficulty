import json
import pickle
import numpy as np
from pprint import pprint

from features import vecify
from model import process

SONG_FN = 'res/Songs/ITG Helblinde 2016/Legacy of Kings - [Zaia]/Legacy of Kings.sm'

with open('res/automl.pickle','rb') as f:
    automl = pickle.load(f)

X = []

with open(SONG_FN, 'r') as f:
    lines = f.readlines()

song = process(lines)
difficulties = sorted(song['charts'])
for difficulty in difficulties:
    X.append(vecify(song, difficulty))

X = np.array(X)
pprint(list(zip(
    difficulties # Easy, Medium, Hard, Challenge, Edit
    , automl.predict(X) # Predicted rating
    , [song['charts'][d]['rating'] for d in difficulties] # Old rating
    )))
