import pandas as pd
from sankey import make_sankey


#1
artists = pd.read_json('artists.json')
print(artists)

artists['BeginDate'] = ((artists['BeginDate'] // 10) * 10).astype(int)

#2
grouped_artist = artists.groupby(['Nationality', 'BeginDate']).size().reset_index(name='Count')

#3 and 4
filtered_artists = grouped_artist.dropna()
filtered_artists = filtered_artists[filtered_artists['BeginDate'] != 0]
filtered_artists = filtered_artists[filtered_artists['Count'] < 20]
pd.set_option('display.max_columns', None)
print(filtered_artists)

#5
grouped_artist = artists.groupby(['Nationality', 'Gender', 'BeginDate']).size().reset_index(name='Count')

filtered_artists = grouped_artist.dropna()
filtered_artists = filtered_artists[filtered_artists['BeginDate'] != 0]
filtered_artists = filtered_artists[filtered_artists['Count'] < 20]
print(filtered_artists)

fig = make_sankey(filtered_artists, 'Nationality', 'Gender', 'BeginDate', vals='Count')
fig.update_layout(title_text="Artist Nationality, Gender, and Decade Sankey Diagram")
fig.show()