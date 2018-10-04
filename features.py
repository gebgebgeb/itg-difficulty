def vecify(song, difficulty):
    chart_data = song['charts'][difficulty]

    bpm = list(song['bpms'].values())[0]
    out = [bpm
            , bpm**2
            , bpm**.5
            , float(chart_data['num_notes']) / chart_data['num_measures']
            , chart_data['num_notes']
            , chart_data['num_notes']**.5
            , chart_data['num_measures']
            , chart_data['num_measures']**.5
            , chart_data['num_measures_stream']
            , chart_data['num_measures_stream']**.5
            , chart_data['num_measures_rest']
            , chart_data['longest_stream']
            , chart_data['longest_stream']**.5
            ]
    return out
