import json
from pprint import pprint

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, RobustScaler
import sklearn.model_selection
import sklearn.metrics
from tqdm import tqdm
import json
import itertools

from features import vecify
import train_auto

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

raw_X = []
y = []
lost = 0
total = 0
all_charts = list(train_auto.all_charts())
for song, difficulty in all_charts:
    raw_X.append(vecify(song, difficulty))
    y.append(song['charts'][difficulty]['rating'] + 0.5)

scaler = RobustScaler()
X = scaler.fit_transform(raw_X)

X_train, X_test, y_train, y_test = \
        sklearn.model_selection.train_test_split(X, y, random_state=1)

results = []
for feature_indices in tqdm(list(powerset(range(X.shape[1])))):
    if not feature_indices:
        continue
    reg = LinearRegression().fit(X_train[:, feature_indices], y_train)
    predictions = reg.predict(X_test[:, feature_indices])
    r2_score =  sklearn.metrics.r2_score(y_test, predictions)
    results.append((feature_indices, r2_score))

results.sort(key=lambda x:x[1])
best_indices, best_r2 = results[-1]
print('Best feature indices')
print(best_indices)
print(best_r2)
with open('res/feature_selection.json', 'w') as f:
    json.dump(results, f)
with open('res/best_indices.json', 'w') as f:
    json.dump(best_indices, f)
