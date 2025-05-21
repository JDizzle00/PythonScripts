import pandas as pd

file_path = 'ViewingActivity.csv'
df = pd.read_csv(file_path)
jakob = df[df['Profile Name'] == 'Gemeinsam']
jakob_subset = jakob[['Title', 'Start Time', 'Bookmark']]

films_filtered = ~jakob_subset['Title'].str.contains('Episode|Folge|hook|\(Trailer\)|Season|Staffel|Teaser|Trailer:|Clip')
films = jakob_subset[films_filtered]
films = films.sort_values(by='Start Time', ascending=True)
films['Start Time'] = pd.to_datetime(films['Start Time']).dt.strftime('%d.%m.%Y')
series_filtered = jakob_subset['Title'].str.contains('Episode') & ~jakob_subset['Title'].str.contains('hook|\(Trailer\)|Teaser|Trailer:|Clip')
series = jakob_subset[series_filtered]
series = series.sort_values(by='Title', ascending=True)
series['Start Time'] = pd.to_datetime(series['Start Time']).dt.strftime('%d.%m.%Y')

films.to_csv('netflix-watched-films.csv', index=False)
series.to_csv('netflix-watched-series.csv', index=False)