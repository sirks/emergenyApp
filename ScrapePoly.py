import requests
from bs4 import BeautifulSoup

#Get the newest open activations
url='https://emergency.copernicus.eu/mapping/activations-rapid/feed'
resp = requests.get(url)
soup=BeautifulSoup(resp.content, features='xml')

#search for activations
items =soup.findAll('item')
first = items[0].title.text

#Select only string values with activation Code
activation = first[1:8]
url='https://emergency.copernicus.eu/mapping/list-of-components/{}/aemfeed'.format(activation)
resp = requests.get(url)
soup=BeautifulSoup(resp.content, features='xml')
#Scrape Polygons
polygons =soup.findAll('georss:polygon')
