import pandas as pd

def convert_to_datetime_or_original(value):
    try:
        return pd.to_datetime(value).strftime('%d.%m.%Y')
    except ValueError:
        return value

file_path = 'PrimeVideo.ViewingHistory.csv'
title_name = 'Title'
starttime_name = 'Playback Start Datetime (UTC)'
viewtime_name = 'Seconds Viewed'

df = pd.read_csv(file_path)
user_subset = df[[title_name, starttime_name, viewtime_name]]

films_filtered = ~user_subset[title_name].str.contains('Episode|hook|\(Trailer\)|Season|SEASON|Staffel|STAFFEL|Teaser|Trailer:|Clip|Coverage: ')
films = user_subset[films_filtered]
films = films.sort_values(by=title_name, ascending=True)

films[title_name] = films[title_name].str.replace('"', '')
films[starttime_name] = films[starttime_name].apply(convert_to_datetime_or_original)
films = films.groupby(title_name).agg({viewtime_name: 'sum', starttime_name: 'max'}).reset_index()
films['Viewtime'] = pd.to_datetime(films[viewtime_name], unit='s').dt.strftime('%H:%M')


series_filtered = user_subset[title_name].str.contains('Episode') & ~user_subset[title_name].str.contains('hook|\(Trailer\)|Teaser|Trailer:|Clip')
series = user_subset[series_filtered]
series = series.sort_values(by=title_name, ascending=True)

series[title_name] = series[title_name].str.replace('"', '')
series[starttime_name] = series[starttime_name].apply(convert_to_datetime_or_original)
series['Viewtime'] = pd.to_datetime(series[viewtime_name], unit='s').dt.strftime('%H:%M')


films.to_csv('primevideo-watched-films.csv', index=False)
series.to_csv('primevideo-watched-series.csv', index=False)