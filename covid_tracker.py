import pandas as pd
import requests
import folium
from selenium import webdriver
import time
import os

myurl = "https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Europe"

def create_dataset(url):
    req = requests.get(url)
    data_list = pd.read_html(req.text)
    df = data_list[3]
    df.columns = ['Country', 'Cases', 'Deaths', 'Recoveries', 'Col0']
    df = df[['Country', 'Cases', 'Deaths', 'Recoveries']]
    df = df.drop([53])
    df['Country'] = df['Country'].str.replace('\[.*\]', '')
    df['Deaths'] = df['Deaths'].str.replace('no data', '0')
    df['Recoveries'] = df['Recoveries'].str.replace('no data', '0')
    df['Cases'] = pd.to_numeric(df['Cases'])
    df['Deaths'] = pd.to_numeric(df['Deaths'])
    df['Recoveries'] = pd.to_numeric(df['Recoveries'])

    return df

def save_dataset(file_loc, dataframe):
    dataframe.to_csv(file_loc)

def create_map(geo_data, data, columns, legend_name):
    mymap = folium.Map(location=[53, 9], zoom_start=4)

    folium.Choropleth(
        geo_data=geo_data,
        name="choropleth",
        data=data,
        columns=columns,
        key_on='feature.properties.sovereignt',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend_name,
        nan_fill_color="white",
        bins=9,
        reset=True
    ).add_to(mymap)

    folium.LayerControl().add_to(mymap)

    return mymap

def save_map(mapfile, mymap):
    url = "{path}\{mapfile}".format(path=os.getcwd(), mapfile=mapfile)
    mymap.save(outfile=mapfile)

def screenshot_map(mapfile, f_dest):
    browser = webdriver.Firefox(executable_path=r"C:\StefanosFardellas\covid_eu\geckodriver\geckodriver.exe")
    map_url = "file://{path}/{mapfile}".format(path=os.getcwd(), mapfile=mapfile)
    browser.get(map_url)
    time.sleep(5)
    browser.save_screenshot(f_dest)
    browser.quit()


df = create_dataset(myurl)
fl = 'datasets/datas.csv'
save_dataset(fl, df)

states = os.path.join('geojson', 'countries.geo.json')
country_covid = os.path.join('geojson', 'datas.csv')
covid_data = pd.read_csv(country_covid)

datas = {
    'Total Covid-19 Cases' : ['Country', 'Cases'],
    'Total Covid-19 Deaths' : ['Country', 'Deaths'],
    'Total Covid-19 Recoveries' : ['Country', 'Recoveries']
}

maps = []

for data in datas:
    m = create_map(states, covid_data, datas[data], data)
    maps.append(m)

mapfiles = [
    'maps/cases.html',
    'maps/deaths.html',
    'maps/recoveries.html'
]

for i in range(len(mapfiles)):
    save_map(mapfiles[i], maps[i])

photos = [
    'maps/photos/cases.png',
    'maps/photos/deaths.png',
    'maps/photos/recoveries.png'
]

for i in range(len(mapfiles)):
    screenshot_map(mapfiles[i], photos[i])