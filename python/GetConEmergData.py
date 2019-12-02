import json
from time import sleep

import requests
from bs4 import BeautifulSoup

#List of Diaster possilbe from emergency.copernicus.eu/mapping/list-of-activations (Note dont know if it all)
dislist=["Tsunami","fire","Fire","Wildfires","Forest fire","Floods","Flooding","Severe Flooding","Tropical Cyclone","Earthquake"]

def fetch_active():
    # Get the  active emergency code from copernicus
    active_url = 'https://emergency.copernicus.eu/mapping/list-of-activations-rapid'
    resp = requests.get(active_url)
    soup = BeautifulSoup(resp.content, features='xml')
    # search for activations
    items = soup.findAll('tr')
    Activelist = []
    for item in items:
        if 'background-color:#75b127' in str(item):
            found = str(item).find('EMS')
            active = str(item)[found:found + 7]
            Activelist.append(active)
    print(Activelist)

    # Get the newest open activations
    url = 'https://emergency.copernicus.eu/mapping/activations-rapid/feed'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, features='xml')
    # search for activations
    items = soup.findAll('item')
    jsondata = {}
    for number, item in enumerate(items):
        # print(number)
        first = item.title.text
        # Select only string values with activation Code
        activation = first[1:8]  # code
        if activation not in Activelist:
            continue
        
        Info = first[10:len(first)]
        Event=""
        for event in dislist:
            if event in Info:
                Event=event
        url = f'https://emergency.copernicus.eu/mapping/list-of-components/{activation}/aemfeed'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features='xml')
        # Scrape Polygons
        polygons = soup.findAll('georss:polygon')
        # m=fm.Map([46.90814465,14.3134518],zoom_start=10,tiles='OpenStreetMap')
        poldata = []
        for pol in polygons:
            newpoly = []
            #  print(str(pol)[16:len(pol)-18])
            polraw = str(pol)[16:len(pol) - 18]
          #  print(type(polraw))
            polsplit = polraw.split(" ")
            a = 0
            # print(len(polsplit)/2)
            for i in range(0, int(len(polsplit) / 2)):
                newpoly.append(polsplit[a:a + 2])
                a = a + 2
            poldata.append(newpoly)

        #  print(activation)
        jsondata[activation] = {
            'code': activation,
            'type': Event,
            'info': Info,
            'poldata': poldata
        }
    return jsondata


while True:
    active_enmergencies = fetch_active()
    with open('emergency.json', 'w') as outfile:
        json.dump(active_enmergencies, outfile)
    print('save done')
    sleep(3600)
