import re
from pprint import pprint

config_pattern = re.compile(r'#([A-Z0-9]+):(.*?);', re.DOTALL)
difficulties = ['Beginner', 'Easy', 'Medium', 'Hard', 'Challenge', 'Edit']

def remove_comment(line):
    return line.split('//')[0].strip()

def parse_measures(lines):
    measures = []
    cur_measure = []
    for line in lines:
        line = remove_comment(line)
        if line == ',':
            measures.append(cur_measure)
            cur_measure = []
        else:
            cur_measure.append(line)
    return measures


def parse_chart_sm(notesdata):
    out = {}
    segments = [x.strip() for x in notesdata.split(':')]
    if not segments[0]:
        segments = segments[1:]
    out['dance_type'] = segments[0]
    out['description'] = segments[1]
    out['difficulty'] = segments[2]
    out['rating'] = float(segments[3])
    out['meter'] = out['rating']
    out['groove_radar'] = [float(x) for x in segments[4].split(',')]
    out['notes'] = parse_measures(segments[-1].split('\n'))
    return out

def numify(s):
    try:
        return int(s)
    except:
        pass
    try:
        return float(s)
    except:
        pass
    raise ValueError("'%s' doesn't look like a number" % s)

def numify_if_possible(s):
    try:
        numify(s)
    except ValueError:
        return s


def multival_parse(data, split=',', force_numify=True):
    out = []
    changes = data.split(split)
    changes = [x.strip().split('=') for x in changes]
    changes = [x for x in changes if not all([not subx for subx in x])]
    changes = [x for x in changes if len(x) > 0]
    if force_numify:
        changes = [tuple(map(numify, x)) for x in changes]
    else:
        changes = [tuple(map(numify_if_possible, x)) for x in changes]
    return changes

def parse_file(filename):
    mode = filename.split('.')[-1].lower()
    with open(filename, 'r') as f:
        filedata = f.read()
    song_data = parse(filedata, mode=mode)
    song_data['filepath'] = filename
    return song_data

def parse(filedata, mode):
    song_data = {}
    if mode == 'sm':
        sections = config_pattern.findall(filedata)
        for key, value in sections:
            key = key.lower()
            if key == 'notes':
                continue
            elif key in ['offset', 'samplelength', 'samplestart']:
                song_data[key] = float(value)
            elif key in ['bpms', 'stops']:
                song_data[key] = multival_parse(value, force_numify=True)
            else:
                song_data[key] = value
        charts = [x[1] for x in sections if x[0] in ['NOTES', 'NOTES2']]
        song_data['charts'] = {}
        for chart in charts:
            parsed_chart = parse_chart_sm(chart)
            song_data['charts'][parsed_chart['difficulty']] = parsed_chart
    elif mode == 'ssc':
        segments = filedata.split('#NOTEDATA:;\n')
        song_tags = segments[0]
        charts = segments[1:]

        song_sections = config_pattern.findall(song_tags)
        for key, value in song_sections:
            key = key.lower()
            if key in ['offset', 'samplelength', 'samplestart']:
                song_data[key] = float(value)
            elif key in ['bpms', 'stops', 'delays', 'warps', 'combos', 'speeds', 'fakes', 'scrolls', 'tickcounts', 'timesignatures']:
                song_data[key] = multival_parse(value, split=',', force_numify=True)
            elif key in ['labels', 'bgchanges', 'fgchanges']:
                song_data[key] = multival_parse(value, split=',', force_numify=False)
            elif key == 'attacks':
                song_data[key] = multival_parse(value, split='  ', force_numify=False)
            else:
                song_data[key] = value
        song_data['charts'] = {}
        for chart in charts:
            parsed_chart = {}
            chart_sections = config_pattern.findall(chart)
            for key, value in chart_sections:
                key = key.lower()
                if key == 'radarvalues':
                    parsed_chart[key] = [float(x) for x in value.split(',')]
                elif key in ['notes', 'notes2']:
                    parsed_chart['notes'] = parse_measures(value.split('\n'))
                elif key == 'meter':
                    parsed_chart[key] = float(value)
                    parsed_chart['rating'] = parsed_chart['meter']
                else:
                    parsed_chart[key] = value
            song_data['charts'][parsed_chart['difficulty']] = parsed_chart
    else:
        raise ValueError('invalid mode! please use "sm" or "ssc"')
    return song_data

if __name__=='__main__':
    #test_fn = 'res/Songs/ITG Helblinde 2016/Legacy of Kings - [Zaia]/Legacy of Kings.sm'
    #test_fn = 'res/Songs/ITG U.P.S/wndrwll/wndrwll.ssc'
    test_fn = 'res/Songs/A NCPR\'s ITG Katsudou!/Barefoot Renaissance/Barefoot Renaissance.sm'

    pprint(parse(test_fn))
    
