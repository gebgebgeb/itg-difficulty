import os
import json
from tqdm import tqdm

from model import process
import cfg

all_songs = []

for root, dirs, files in tqdm(list(os.walk(cfg.SONGS_DIR))):
    if not('ITG' in root or 'YARK' in root):
        continue
    for name in files:
        if name.lower().endswith('.sm') or name.lower().endswith('.ssc'):
            with open(os.path.join(root, name), 'r') as f:
                try:
                    lines = f.readlines()
                except:
                    print(root, name)
                    continue
            song_data = process(lines)
            song_data['dirpath'] = root
            song_data['song_dir_name'] = name
            all_songs.append(song_data)


if not os.path.isdir('./res'):
    os.mkdir('res')
with open('res/all_songs.json','w') as f:
    json.dump(all_songs, f)
