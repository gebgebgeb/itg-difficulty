from pprint import pprint

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


def read_metadata(lines):
    credit = ''
    title = ''
    for line_idx, line in enumerate(lines):
        ls = line.strip()
        if ls.startswith('#TITLE:'):
            title = ls.split(':',1)[1].strip().strip(';')
        if ls.startswith('#ARTIST:'):
            artist = ls.split(':',1)[1].strip().strip(';')
        if ls.startswith('#CREDIT:'):
            credit = ls.split(':',1)[1].strip().strip(';')
        if ls.startswith('#BPMS:'):
            bpm_lines = []
            for i in range(line_idx, len(lines)):
                bpm_lines.append(lines[i].strip())
                if ';' in lines[i]:
                    break
                if lines[i+1].startswith('#'):
                    break
            raw_bpms = ''.join(bpm_lines)
            raw_bpms = raw_bpms.split(':',1)[1].strip().strip(';').split(',')
            bpms = {}
            for raw_bpm in raw_bpms:
                beat, bpm = raw_bpm.split('=')
                try:
                    bpms[float(beat)] = float(bpm)
                except:
                    continue
    return {'title': title
            , 'artist': artist
            , 'credit': credit
            , 'bpms': bpms
            , 'dirpath': ''
            , 'song_dir_name': ''
            }

def read_chart(lines, target_difficulty):
    output = {}

    reading = False
    measures = [] # list of lists, each sublist is a measure
    for line_idx, line in enumerate(lines):
        if line.startswith('#NOTES:'):
            difficulty = lines[line_idx + 3].strip().strip(':')
            if difficulty == target_difficulty:
                reading = True
                dance_type = lines[line_idx + 1].strip().strip(':')
                rating = int(float(lines[line_idx + 4].strip().strip(':')))
                cur_measure = []
        if reading:
            if line.strip() == ';':
                reading = False
            if len(line.strip()) == 4:
                cur_measure.append(line.strip())
            if line.startswith(','):
                measures.append(cur_measure)
                cur_measure = []
    if measures:
        output['rating'] = rating
        output['dance_type'] = dance_type
        output['difficulty'] = target_difficulty
        output['measures'] = measures

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
    else:
        return None

def process(lines):
    out = read_metadata(lines)
    charts = {}
    for difficulty in ['Beginner', 'Easy', 'Medium', 'Hard', 'Challenge', 'Edit']:
        chart_data = read_chart(lines, difficulty)
        if chart_data:
            charts[difficulty] = chart_data
    out['charts'] = charts
    return out
        

if __name__=='__main__':
    test_fn = 'res/Songs/ITG Helblinde 2016/Legacy of Kings - [Zaia]/Legacy of Kings.sm'
    with open(test_fn, 'r') as f:
        lines = f.readlines()

    pprint(process(lines))
    
