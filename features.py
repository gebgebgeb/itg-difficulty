def vecify(song, difficulty):
    chart_data = song['charts'][difficulty]

    bpm = list(song['bpms'].values())[0]
    out = [bpm
            , float(chart_data['num_notes']) / chart_data['num_measures']
            , chart_data['num_notes']
            , chart_data['num_measures']
            , chart_data['num_measures_stream']
            , chart_data['num_measures_rest']
            , chart_data['longest_stream']
            ]
    return out
