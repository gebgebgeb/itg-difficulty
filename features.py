def vecify(song, difficulty):
    chart_data = song['charts'][difficulty]['features']

    bpm = list(song['bpms'].values())[0]
    effective_bpm = bpm*chart_data['most_common_strm_res']
    out = [bpm
            , effective_bpm
            , effective_bpm**.5
            , effective_bpm**2
            , float(chart_data['num_notes']) / chart_data['num_measures']
            , chart_data['num_notes']
            , chart_data['num_notes']**.5
            , chart_data['num_measures']
            , chart_data['num_measures']**.5
            , chart_data['num_measures_stream']
            , chart_data['num_measures_stream']**.5
            , chart_data['num_measures_rest']
            , chart_data['num_measures_interesting']
            , chart_data['longest_stream']
            , chart_data['longest_stream']**.5
            ]
    return out