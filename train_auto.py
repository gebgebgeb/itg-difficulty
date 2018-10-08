import json
from pprint import pprint
import numpy as np
import pickle

import sklearn.model_selection
import sklearn.metrics

import autosklearn.regression

from features import vecify

def valid(song, difficulty):
    if not len(song['bpms']) == 1:
        return False
    if song['charts'][difficulty]['features']['num_measures'] == 0:
        return False
    if song['charts'][difficulty]['features']['num_notes'] == 0:
        return False
    difficulty = song['charts'][difficulty]['rating']
    if difficulty == 1 or difficulty > 20:
        return False
    return True


def all_charts():
    with open('res/all_songs.json', 'r') as f:
        all_songs = json.load(f)
    for song in all_songs:
        for difficulty in song['charts']:
            if not valid(song, difficulty):
                continue
            yield song, difficulty


X = []
y = []
all_charts = list(all_charts())
for song, difficulty in all_charts:
    X.append(vecify(song, difficulty))
    y.append(song['charts'][difficulty]['rating'] + 0.5)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = \
        sklearn.model_selection.train_test_split(X, y, random_state=1)

automl = autosklearn.regression.AutoSklearnRegressor(
    #time_left_for_this_task=6*60
    #, per_run_time_limit=30
    time_left_for_this_task=6*60*60
    , per_run_time_limit=360
    , tmp_folder='autosktmp'
    , output_folder='autoskout'
)
automl.fit(X_train, y_train, dataset_name='sm',
           feat_type=['numerical']*len(X_train[0]))

with open('res/automl.pickle','wb') as f:
    pickle.dump(automl, f)
'''
with open('res/automl.pickle','rb') as f:
    automl = pickle.load(f)
'''

print('*'*80)
print(automl.show_models())
predictions = automl.predict(X_test)
print("R2 score:", sklearn.metrics.r2_score(y_test, predictions))
print("Mean Absolute Error:", sklearn.metrics.mean_absolute_error(y_test, predictions))
print("Median Absolute Error:", sklearn.metrics.median_absolute_error(y_test, predictions))
input()

for i, pred in enumerate(automl.predict(X)):
    true = y[i]
    if abs(pred - true) > 0.5:
    #if True:
        song, difficulty = all_charts[i]
        #if not 'YARKSFA - Qual' in song['dirpath']:
            #continue
        print(song['title'])
        print(difficulty)
        print(song['charts'][difficulty]['rating'])
        print(pred)
        print(song['dirpath'])
        print('*'*80)

