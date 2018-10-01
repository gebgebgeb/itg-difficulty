from pprint import pprint

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
    reading = False
    found = False
    notes_data = [] # list of lists, each sublist is a measure
    for line_idx, line in enumerate(lines):
        if line.startswith('#NOTES:'):
            difficulty = lines[line_idx + 3].strip().strip(':')
            if difficulty == target_difficulty:
                reading = True
                found = True
                dance_type = lines[line_idx + 1].strip().strip(':')
                rating = int(float(lines[line_idx + 4].strip().strip(':')))
                cur_measure = []
        if reading:
            if line == ';':
                reading = False
            if len(line.strip()) == 4:
                cur_measure.append(line.strip())
            if line.strip() == ',':
                notes_data.append(cur_measure)
                cur_measure = []
    if found:
        num_measures = 0
        num_notes = 0
        for measure in notes_data:
            for line in measure:
                num_notes += sum([x in ['1', '2', '4'] for x in line])
            num_measures += 1

        num_measures_stream = 0
        num_measures_rest = 0
        longest_stream = 0
        cur_stream = 0
        for measure in notes_data:
            if len(measure) >= 16 and all(['1' in line for line in measure]):
                num_measures_stream += 1
                cur_stream += 1
            else:
                if cur_stream > longest_stream:
                    longest_stream = cur_stream
                cur_stream = 0
            if sum([('1' in line or '2' in line or '4' in line) for line in measure]) <= 8:
                num_measures_rest += 1

        return {'num_notes': num_notes
                , 'num_measures': num_measures
                , 'rating': rating
                , 'difficulty': target_difficulty
                , 'dance_type': dance_type
                , 'num_measures_stream': num_measures_stream
                , 'num_measures_rest': num_measures_rest
                , 'longest_stream': longest_stream
                }
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
    
