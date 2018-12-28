import pandas as pd

files = ['../../data/GL2017.TXT','../data/GL2018.txt']

for file in files:
    data = pd.read_csv(file, header=None)
    data['year'] = data[0].astype(str).str[0:4]
    data['month'] = data[0].astype(str).str[4:6]

    gb = data.groupby(['year','month'])
    
    for group in gb.groups:
        partition = gb.get_group(group)
        year = group[0]
        month = group[1]
        partition.to_csv(f'../../data/GL1718/game_log_{year}_{month}.csv', header=False, index=False)
