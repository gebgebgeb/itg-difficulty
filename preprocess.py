import os
import json
from tqdm import tqdm

from augment import process
import cfg

all_songs = []

for root, dirs, files in tqdm(list(os.walk(cfg.SONGS_DIR))):
    if not('ITG' in root or 'YARK' in root):
        continue
    found_sm = None
    found_ssc = None
    for name in files:
        if name.lower().endswith('.sm'):
            found_sm = os.path.join(root, name)
        if name.lower().endswith('.ssc'):
            found_ssc = os.path.join(root, name)
    if not (found_ssc is None):
        full_fname = found_ssc
    elif not (found_sm is None):
        full_fname = found_sm
    else:
        continue
    try:
        song_data = process(full_fname)
    except (UnicodeDecodeError, ValueError):
        print('invalid file: %s' % full_fname)
    all_songs.append(song_data)


if not os.path.isdir('./res'):
    os.mkdir('res')
with open('res/all_songs.json','w') as f:
    json.dump(all_songs, f)
