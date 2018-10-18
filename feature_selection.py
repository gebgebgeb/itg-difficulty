import json
from pprint import pprint
import numpy as np
import collections
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, RobustScaler
import sklearn.model_selection
import sklearn.metrics
from tqdm import tqdm
import json
import itertools
import multiprocessing as mp
from sortedcontainers import SortedList 

from features import vecify
import train_auto
import utils


raw_X = []
y = []
lost = 0
total = 0
all_charts = list(train_auto.all_charts())
for song, difficulty in all_charts:
    raw_X.append(vecify(song, difficulty))
    y.append(song['charts'][difficulty]['rating'] + 0.5)

#scaler = RobustScaler()
#X = scaler.fit_transform(raw_X)
X = np.array(raw_X)

X_train, X_test, y_train, y_test = \
        sklearn.model_selection.train_test_split(X, y, random_state=1)

def score_fi(feature_indices):
    if not feature_indices:
        return(feature_indices, 0)
    reg = LinearRegression().fit(X_train[:, feature_indices], y_train)
    predictions = reg.predict(X_test[:, feature_indices])
    r2_score =  sklearn.metrics.r2_score(y_test, predictions)
    return (feature_indices, r2_score)

pool = mp.Pool(3)
results_generator = pool.imap_unordered(score_fi, tqdm(utils.powerset(range(X.shape[1]))), chunksize=10000)
results = SortedList(key=lambda x:abs(1-x[1]))
for i, result in enumerate(results_generator):
    results.add(result)
    if i % 10000 == 5000:
        results = SortedList(results[:5000], key=lambda x:abs(1-x[1]))
        best_indices, best_r2 = results[-1]
        print(results[0])
        with open('res/feature_selection.json', 'w') as f:
            json.dump(list(results), f)
        with open('res/best_indices.json', 'w') as f:
            json.dump(best_indices, f)

print('Best feature indices')
print(best_indices)
print(best_r2)
