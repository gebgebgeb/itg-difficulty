from pprint import pprint
from parse import parse_file

def has_step(line):
    return any([x in line for x in ['1','2','4']])

def is_stream(measure):
    if all([has_step(line) for line in measure]):
        if len(measure) >= 12:
            return True
    return False

def is_rest(measure):
    if sum([has_step(line) for line in measure]) <= 8:
        return True
    return False

def is_interesting(measure):
    if len(measure) - sum([has_step(line) for line in measure]) <= 2:
        return False
    if is_rest(measure):
        return False
    return True

def precompute_features(measures):
    output = {}
    num_measures = 0
    num_notes = 0
    for measure in measures:
        for line in measure:
            num_notes += sum([x in ['1', '2', '4'] for x in line])
        num_measures += 1
    output['num_notes'] = num_notes
    output['num_measures'] = num_measures

    num_measures_stream = 0
    num_measures_rest = 0
    num_measures_interesting = 0
    longest_stream = 0
    cur_stream = 0
    for measure in measures:
        if is_stream(measure):
            num_measures_stream += 1
            cur_stream += 1
        else:
            if cur_stream > longest_stream:
                longest_stream = cur_stream
            cur_stream = 0
        if is_rest(measure):
            num_measures_rest += 1
        if is_interesting(measure):
            num_measures_interesting += 1
    output['num_measures_stream'] = num_measures_stream
    output['num_measures_rest'] = num_measures_rest
    output['num_measures_interesting'] = num_measures_interesting
    output['longest_stream'] = longest_stream

    strm_res = {}
    for measure in measures:
        if is_stream(measure):
            strm_res[len(measure)] = strm_res.setdefault(len(measure), 0) + 1
    if strm_res:
        most_common_res = sorted(strm_res, key=strm_res.get)[-1]
    else:
        most_common_res = 0
    output['most_common_strm_res'] = most_common_res
    return output

def process(fname):
    song_data = parse_file(fname)
    if not 'charts' in song_data:
        return None
    for difficulty in song_data['charts']:
        chart_data = song_data['charts'][difficulty]
        chart_data['features'] = precompute_features(chart_data['notes'])
    return song_data
        

if __name__=='__main__':
    test_fn = 'res/Songs/ITG Helblinde 2016/Legacy of Kings - [Zaia]/Legacy of Kings.sm'
    pprint(process(fname))
    
