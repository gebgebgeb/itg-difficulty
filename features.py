def vecify(song, difficulty, feature_indices=None):
    chart_data = song['charts'][difficulty]['features']

    bpm = song['bpms'][0][1]
    effective_bpm = bpm*chart_data['most_common_strm_res']
    out = [bpm
            , bpm**2
            , bpm**.5
            , effective_bpm
            , effective_bpm**.5
            , effective_bpm**2
            , float(chart_data['num_notes']) / chart_data['num_measures']
            , (float(chart_data['num_notes']) / chart_data['num_measures'])**.5
            , (float(chart_data['num_notes']) / chart_data['num_measures'])**.2
            , chart_data['num_notes']
            , chart_data['num_notes']**.5
            , chart_data['num_notes']**2
            , chart_data['num_measures']
            , chart_data['num_measures']**.5
            , chart_data['num_measures']**2
            , chart_data['num_measures_stream']
            , chart_data['num_measures_stream']**.5
            , chart_data['num_measures_stream']**2
            , chart_data['num_measures_rest']
            , chart_data['num_measures_rest']**.5
            , chart_data['num_measures_rest']**2
            , chart_data['num_measures_interesting']
            , chart_data['num_measures_interesting']**.5
            , chart_data['num_measures_interesting']**2
            , chart_data['longest_stream']
            , chart_data['longest_stream']**.5
            , chart_data['longest_stream']**2
            ]
    if feature_indices:
        return [x for i,x in enumerate(out) if i in feature_indices]
    else:
        return out
