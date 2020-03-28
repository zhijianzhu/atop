import wget
import os

print("downloading confirmed case")
base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

data_file = 'time_series_19-covid-Confirmed.csv'
data_file_1 = 'time_series_covid19_confirmed_global.csv'
url = base_url + data_file_1
new_file = "data/" + data_file

if os.path.exists(new_file):
    os.remove(new_file)
wget.download(url, new_file)

data_file = 'time_series_19-covid-Deaths.csv'
data_file_1 = 'time_series_covid19_deaths_global.csv'

url = base_url + data_file_1
new_file = "data/" + data_file

if os.path.exists(new_file):
    os.remove(new_file)
wget.download(url, new_file)

data_file = 'time_series_19-covid-Recovered.csv'
data_file_1 = 'time_series_covid19_recovered_global.csv'

url = base_url + data_file_1
new_file = "data/" + data_file

if os.path.exists(new_file):
    os.remove(new_file)
wget.download(url, new_file)
