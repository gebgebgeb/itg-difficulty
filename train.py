import json
from pprint import pprint

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, RobustScaler

from features import vecify

def valid(song, difficulty):
    if not len(song['bpms']) == 1:
        return False
    if song['charts'][difficulty]['num_measures'] == 0:
        return False
    if song['charts'][difficulty]['num_notes'] == 0:
        return False
    if song['charts'][difficulty]['rating'] == 1:
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


raw_X = []
y = []
lost = 0
total = 0
all_charts = list(all_charts())
for song, difficulty in all_charts:
    raw_X.append(vecify(song, difficulty))
    y.append(song['charts'][difficulty]['rating'] + 0.5)

scaler = RobustScaler()
'''
poly = PolynomialFeatures(2, interaction_only=True, include_bias=False)
#poly = PolynomialFeatures(2, include_bias=False)
X = poly.fit_transform(
        scaler.fit_transform(
            raw_X
            )
        )
'''
X = scaler.fit_transform(raw_X)

reg = LinearRegression().fit(X, y)
print(reg.score(X, y))
#print(reg.coef_)
#print(reg.intercept_)
input()

for i, pred in enumerate(reg.predict(X)):
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
        print(raw_X[i])
        print('*'*80)

