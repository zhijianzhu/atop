import wget
import os

print("downloading confirmed case")
base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

data_file = 'time_series_19-covid-Confirmed.csv'
url = base_url + data_file
new_file = "data/" + data_file

if os.path.exists(new_file):
    os.remove(new_file)
wget.download(url, new_file)

data_file = 'time_series_19-covid-Deaths.csv'
url = base_url + data_file
new_file = "data/" + data_file

if os.path.exists(new_file):
    os.remove(new_file)
wget.download(url, new_file)

data_file = 'time_series_19-covid-Recovered.csv'
url = base_url + data_file
new_file = "data/" + data_file

if os.path.exists(new_file):
    os.remove(new_file)
wget.download(url, new_file)
