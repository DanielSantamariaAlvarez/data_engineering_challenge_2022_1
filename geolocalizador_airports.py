from geopy.geocoders import Nominatim
import json
import time 
import pandas as pd

geolocator = Nominatim(user_agent="airports")
airports = None
list_airports = []
airports = pd.read_csv('airports_w_wiki.csv')

def cargar_airports():

    for _, fila in airports.head(1000).iterrows():
        j = fila.to_dict()
        lati = float(j['latitude_deg'])
        long = float(j['longitude_deg'])
        lalo = f'{lati}, {long}'
        localization = geolocator.reverse(lalo)
        if localization == None:
            list_airports.append("none")
        else:
            try:
                list_airports.append(localization.raw['address']['country'])
            except:
                list_airports.append("none")


inicio = time.time()
cargar_airports()
with open('airports_country.json','w') as f:
        json.dump(list_airports, f, indent=4, ensure_ascii=False)
fin = time.time()
print(fin-inicio)